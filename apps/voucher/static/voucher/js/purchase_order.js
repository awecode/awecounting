$(document).ready(function () {
    vm = new PurchaseViewModel(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});

function PurchaseViewModel(data) {
    var self = this;

    var company_items = []
    self.items_of_current_company = ko.observable();

    self.purchase_agent_id = ko.observable();
    self.agent = ko.observable();

    for (var k in data) {
        self[k] = ko.observable(data[k]);
    }

    self.status = ko.observable();
    
    self.grand_total_obs = ko.observable(0);

    $.ajax({
        url: '/inventory/api/items.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.items = ko.observableArray(data);
            if (self.items().length > 0) {
                self.items_of_current_company(self.items()[0].company);
                company_items.push({'id': self.items_of_current_company(), 'items': self.items()});
            }
        }
    });

    $.ajax({
        url: '/ledger/api/parties_with_balance.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.parties = ko.observableArray(data);
        }
    });


    self.party_id.subscribe(function (party_id) {
        if (party_id) {
            var party = get_by_id(vm.parties, party_id);
            var company = get_by_id(company_items, party.related_company);
            if (party.related_company != null && typeof(company) == 'undefined') {
                $.ajax({
                    url: '/inventory/api/items/' + party.related_company + '/?format=json',
                    dataType: 'json',
                    async: false,
                    success: function (data) {
                        if (data.length >= 1) {
                            self.items(data);
                            self.items_of_current_company(data[0].company);
                            company_items.push({'id': data[0].company, 'items': self.items()});
                        } else {
                            bsalert.error('Requested company has no item');
                        }
                    }
                });
            } else if (party.related_company == null && party.company != self.items_of_current_company()) {
                var company_item = get_by_id(company_items, party.company);
                if (company_item) {
                    self.items(company_item.items);
                }
                self.items_of_current_company(party.company);
            } else if (party.related_company != null && typeof(company) != 'undefined') {
                company_item = get_by_id(company_items, party.related_company);
                self.items(company_item.items);
                self.items_of_current_company(party.related_company);
            }
        }
    });

    self.render_party_options = function (data) {
        var obj = get_by_id(vm.parties(), data.id);
        var klass = '';
        if (obj.related_company != null) {
            klass = 'green';
        }
        return '<div class="' + klass + '">' + obj.name + '</div>';
    }

    $.ajax({
        url: '/inventory/api/units.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.units = ko.observableArray(data);
        }
    });

    self.party = ko.observable();

    self.party_balance = ko.computed(function () {
        if (self.party())
            return -1 * self.party().balance;
    });

    self.expense_view = new TableViewModel({rows: data.trade_expense}, ExpenseRow);

    self.table_view = new TableViewModel({rows: data.rows, argument: self}, PurchaseRow);

    $.ajax({
        url: '/ledger/api/account.json',
        dataType: 'json',
        data: "categories=purchase_expenses",
        async: false,
        success: function (data) {
            self.expense_accounts = ko.observableArray(data);
        }
    });


    self.id.subscribe(function (id) {
        update_url_with_id(id);
    });

    self.total_amount = 0;

    self.grand_total = function () {
        var sum = 0;
        self.table_view.rows().forEach(function (i) {
            if (i.total_amount()) {
                sum += parseFloat(i.total_amount());
            }
        });
        self.grand_total_obs(sum);
        return r2z(sum);
    };
    
    self.grand_total_including_expenses = function () {
        var sum = 0;
        self.table_view.rows().forEach(function (i) {
            if (i.including_expenses()) {
                sum += parseFloat(i.including_expenses());
            }
        });
        return r2z(sum);
    };

    self.save = function (item, event) {
        if (!self.party()) {
            bsalert.error('Party is required!');
            return false;
        }

        $.ajax({
            type: "POST",
            url: '/voucher/purchase_order/save/',
            data: ko.toJSON(self),
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    bsalert.error(msg.error_message);
                    self.status('errorlist');
                }
                else {
                    bsalert.success('Saved!');
                    self.table_view.deleted_rows([]);
                    if (msg.id)
                        self.id(msg.id);
                    $("#tbody > tr").each(function (i) {
                        $($("#tbody > tr:not(.total)")[i]).addClass('invalid-row');
                    });
                    $("#tbody-expense > tr").each(function (i) {
                        $($("#tbody-expense > tr:not(.total)")[i]).addClass('invalid-row');
                    });
                    if (msg.tax == 'no') {
                        for (var i in msg.rows) {
                            self.table_view.rows()[i].row_tax_vm.tax_scheme(0);
                        }
                    }
                    if (msg.tax_scheme_id != "" && msg.tax_scheme_id != null) {
                        for (var i in msg.rows) {
                            self.table_view.rows()[i].row_tax_vm.tax_scheme(0);
                        }
                    }
                    for (var i in msg.rows) {
                        self.table_view.rows()[i].id = msg.rows[i];
                        $($("#tbody > tr")[i]).removeClass('invalid-row');
                    }
                    for (var i in msg.expense) {
                        self.expense_view.rows()[i].id = msg.expense[i];
                        $($("#tbody-expense > tr")[i]).removeClass('invalid-row');
                    }
                }
            }
        });
    }


}

function ExpenseRow(row) {
    var self = this;

    self.id = ko.observable();
    self.amount = ko.observable();
    self.expense_id = ko.observable();

    for (var k in row)
        self[k] = ko.observable(row[k]);
}

function PurchaseRow(row, purchase_vm) {
    var self = this;

    self.item = ko.observable();
    self.item_id = ko.observable();
    self.quantity = ko.observable();
    self.rate = ko.observable();
    self.discount = ko.observable();
    self.unit = ko.observable();
    self.unit_id = ko.observable();
    self.specification = ko.observable();
    // self.vattable = ko.observable();
    self.fulfilled = ko.observable(false);
    self.remarks = ko.observable();

    for (var k in row)
        self[k] = ko.observable(row[k]);

    self.item.subscribe(function (item) {
        // TODO
        var unit = get_by_id(purchase_vm.units(), item.unit.id);
        if (unit && !self.unit_id())
            self.unit_id(unit.id);
    });

    // self.total = ko.computed(function () {
    //     var total = self.quantity() * self.rate()
    //     if (self.discount() > 0) {
    //         return round2(total - self.discount());
    //     } else if (String(self.discount()).indexOf('%') !== -1){
    //         var discount_amount = ( parseFloat(self.discount()) / 100 ) * total;
    //         return r2z(round2(total - discount_amount))
    //     } else {
    //         return round2(total);
    //     }
    // });

    self.unit.subscription_changed(function (new_val, old_val) {
        if (old_val && old_val != new_val) {
            var conversion_rate = old_val.convertible_units[new_val.id];
            if (conversion_rate) {
                if (self.quantity()) {
                    self.quantity(self.quantity() * conversion_rate);
                }
                if (self.rate()) {
                    self.rate(self.rate() / conversion_rate);
                }
            }
        }
    });

    self.total_amount = function () {
        return round2(self.rate() * self.quantity());
    }

    self.including_expenses = ko.computed(function () {
        var total_expenses = purchase_vm.expense_view.get_total('amount');
        var grand_total = purchase_vm.grand_total_obs();
        return r2z((self.total_amount() / grand_total) * (grand_total + total_expenses));
    });


    self.render_unit_options = function (data) {
        var obj = get_by_id(purchase_vm.units(), data.id);
        var klass = '';
        if (self.unit_id() && obj.id != self.unit_id()) {
            if (obj.convertible_units[self.unit_id()])
                klass = 'green';
            else
                klass = 'red';
        }
        return '<div class="' + klass + '">' + obj.name + '</div>';
    }


    self.render_option = function (data) {
        //purchase_vm
        var obj = get_by_id(purchase_vm.items(), data.id);
        return '<div>' + obj.full_name + '</div>';
    }

}