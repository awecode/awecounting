$(document).ready(function () {
    vm = new PurchaseViewModel(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});

function PurchaseViewModel(data) {
    var self = this;

    for (var k in data) {
        self[k] = ko.observable(data[k]);
    }

    self.status = ko.observable();

    $.ajax({
        url: '/inventory/api/items.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.items = ko.observableArray(data['results']);
        }
    });

    $.ajax({
        url: '/ledger/api/parties_with_balance.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.parties = ko.observableArray(data['results']);
        }
    });

    $.ajax({
        url: '/inventory/api/units.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.units = ko.observableArray(data['results']);
        }
    });

    self.party = ko.observable();

    self.party_balance = ko.computed(function () {
        if (self.party())
            return -1 * self.party().balance;
    });

    self.table_view = new TableViewModel({rows: data.rows, argument: self}, PurchaseRow);

    self.id.subscribe(function (id) {
        update_url_with_id(id);
    });


    // self.vat_amount = function () {
    //     var sum = 0;
    //     self.table_view.rows().forEach(function (i) {
    //         if (i.vattable())
    //             sum += 0.13 * i.total_amount();
    //     });
    //     return round2(sum);
    // }

    self.sub_total = function () {
        var sum = 0;
        self.table_view.rows().forEach(function (i) {
            if (i.total_amount()) {
                sum += parseFloat(i.total_amount());
            }
        });
        return round2(sum);
    }

    // self.discount = function () {
    //     var sum = 0;
    //     self.table_view.rows().forEach(function (i) {
    //         if (String(i.discount()).indexOf('%') !== -1 ) {
    //             var total = i.rate() * i.quantity();
    //             var amount = ( parseFloat(i.discount()) / 100 ) * total
    //             sum += parseFloat(amount);
    //         } else if (i.discount()) {
    //             sum += parseFloat(i.discount());
    //         }
    //     });
    //     return r2z(round2(sum));
    // }

    self.total_amount = 0;

    self.grand_total = function () {
        self.total_amount = rnum(self.sub_total());
        return r2z(self.total_amount);
    }

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
                    $("tbody > tr").each(function (i) {
                        $($("tbody > tr:not(.total)")[i]).addClass('invalid-row');
                    });
                    if (msg.tax == 'no'){
                        for (var i in msg.rows) {
                            self.table_view.rows()[i].row_tax_vm.tax_scheme(0);
                        }
                    }
                    if (msg.tax_scheme_id != "" && msg.tax_scheme_id != null){
                    for (var i in msg.rows) {
                        self.table_view.rows()[i].row_tax_vm.tax_scheme(0);
                    }
                    }
                    for (var i in msg.rows) {
                        self.table_view.rows()[i].id = msg.rows[i];
                        $($("tbody > tr")[i]).removeClass('invalid-row');
                    }
                }
            }
        });
    }


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


    self.render_option = function (data) {purchase_vm
        var obj = get_by_id(purchase_vm.items(), data.id);
        return '<div>' + obj.full_name + '</div>';
    }

}