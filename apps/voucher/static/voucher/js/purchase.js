$(document).ready(function () {
    vm = new PurchaseViewModel(ko_data, voucher_settings);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});

//function TaxViewModel(tax, tax_scheme){
//    var self = this;
//    
//
//    self.tax = ko.observable(tax);
//    self.tax_scheme = ko.observable();
//    self.tax_choices = ko.observableArray(choices);
//  
//    if (tax_scheme) {
//        self.tax_scheme(tax_scheme);
//    };
//
//    if (self.tax() == 'no') {
//        self.tax_scheme_visibility(false);
//    };
//
//    self.get_scheme = function() {
//        var bool;
//        if (self.tax_scheme() == '' ) {
//            bool = true;
//        };  
//        $( "tr.total td:first-child" ).each(function() {
//            if (self.tax_scheme_visibility() && bool) {
//              $( this ).attr( "colspan", colspan + 1 );
//            } else {
//              $( this ).attr( "colspan", colspan );
//            }
//        });
//        return self.tax_scheme_visibility() && bool;
//    };
//}


function PurchaseViewModel(data, settings) {
    var self = this;

    self.tax_types = [
        {
            'id': 'inclusive',
            'value': 'Tax Inclusive',
        },
        {
            'id': 'exclusive',
            'value': 'Tax Exclusive',
        },
        {
            'id': 'no',
            'value': 'No Tax',
        },
    ]
    self.tax = ko.observable();
    self.tax_scheme = ko.observable();

    self.voucher_discount = ko.observable(0);

    for (var k in data) {
        if (k == 'discount') {
            self.voucher_discount(data[k])
        }
        ;
        self[k] = ko.observable(data[k]);
    }

    self.status = ko.observable();

    $.ajax({
        url: '/tax/api/tax_schemes.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.tax_schemes = ko.observableArray(data);
        }
    });

    var company_items = []
    $.ajax({
        url: '/inventory/api/purchase/items.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.items = ko.observableArray(data);
            self.items_of_current_company(self.items()[0].company);
            company_items.push({'id': self.items_of_current_company(), 'items': self.items()})
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

    self.party_id.subscribe(function(party_id) {
        if (party_id) {
            party = get_by_id(vm.parties, party_id);
            company = get_by_id(company_items, party.related_company);
            if (party.related_company != null && typeof(company) == 'undefined' ) {
                $.ajax({
                    url: '/inventory/api/items/' + party.related_company + '/?format=json',
                    dataType: 'json',
                    async: false,
                    success: function (data) {
                        if (data.length >= 1) {
                            self.items(data)
                            self.items_of_current_company(data[0].company);
                            company_items.push({'id': data[0].company, 'items': self.items()})
                        } else {
                            bsalert.error('Requested company has no item');
                        };
                    }
                });
            } else if (party.related_company == null && party.company != self.items_of_current_company()) {
                company_item = get_by_id(company_items, party.company);
                self.items(company_item.items);
                self.items_of_current_company(party.company)
            } else if (party.related_company != null && typeof(company) != 'undefined' ){
                company_item = get_by_id(company_items, party.related_company);
                self.items(company_item.items);
                self.items_of_current_company(party.related_company)
            };
        };
    });

    self.render_party_options = function (data) {
        var obj = get_by_id(vm.parties(), data.id);
        var klass = '';
        if (obj.related_company != null) {
            klass = 'green'
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

    self.party_id.subscribe(function (id) {
        var selected_party = ko.utils.arrayFirst(self.parties(), function (p) {
            return p.id == id;
        });
        if (selected_party) {
            if (selected_party.tax_preference != null) {
                self.tax_vm.tax_scheme(selected_party.tax_preference.tax_scheme)
                if (selected_party.tax_preference.default_tax_application_type != 'no-peference' && selected_party.tax_preference.default_tax_application_type != null) {
                    self.tax_vm.tax(selected_party.tax_preference.default_tax_application_type)
                }
                ;
            }
        }
        ;
    });

    self.party_balance = ko.computed(function () {
        if (self.party())
            return -1 * self.party().balance;
    });

    self.table_view = new TableViewModel({rows: data.rows, argument: self}, PurchaseRow);

    self.id.subscribe(function (id) {
        update_url_with_id(id);
    });

    //self.has_common_tax = function () {
    //    if (self.tax() == 'no' || self.tax_scheme())
    //        return true;
    //    else
    //        return false;
    //};

    self.sub_total = function () {
        var sum = 0;
        self.table_view.rows().forEach(function (i) {
            if (i.total()) {
                sum += parseFloat(i.total());
            }
        });
        return round2(sum);
    }

    self.total_discount = function () {
        var sum = 0;
        self.table_view.rows().forEach(function (i) {
            if (String(i.discount()).indexOf('%') !== -1) {
                var total = i.rate() * i.quantity();
                var amount = ( parseFloat(i.discount()) / 100 ) * total
                sum += parseFloat(amount);
            } else if (i.discount()) {
                sum += parseFloat(i.discount());
            }
        });
        return r2z(round2(sum));
    }

    self.taxable_amount = ko.computed(function () {
        var amt = 0;
        ko.utils.arrayForEach(self.table_view.rows(), function (row) {
            amt += row.total_without_tax();
        });
        if (self.voucher_discount()) {
            amt -= parseFloat(self.voucher_discount());
        }
        return r2z(amt);
    });


    self.tax_amount = function () {
        if (self.tax() == 'no') {
            return 0;
        }
        if (self.tax_scheme()) {
            return r2z(self.sub_total() * self.tax_scheme().percent / 100);
        }
        var total = 0;
        ko.utils.arrayForEach(self.table_view.rows(), function (row) {
            total += row.tax_amount();
        });
        return r2z(total);
    };

    self.total_amount = 0;

    self.grand_total = function () {
        return r2z(self.taxable_amount() + self.tax_amount());
    };

    if (settings.purchase_suggest_by_party_item) {
        self.party.subscribe(function (party) {
            $.ajax({
                url: '/voucher/api/purchase/party/' + party.id + '/rates.json',
                dataType: 'json',
                async: false,
                success: function (data) {
                    ko.utils.arrayForEach(data, function (rate_item) {
                        var item = ko.utils.arrayFirst(self.items(), function (itm) {
                            return itm.id == rate_item.id;
                        });
                        item.last_purchase_price = rate_item.last_purchase_price;
                    });
                }
            });
        })
    }

    self.save = function (item, event) {
        if (!self.party()) {
            bsalert.error('Party is required!');
            return false;
        }

        var check_discount;
        self.table_view.rows().forEach(function (i) {
            var discount_as_string = String(i.discount());
            if (discount_as_string.indexOf('%') !== -1) {
                if (typeof(discount_as_string[discount_as_string.indexOf('%') + 1]) != 'undefined') {
                    bsalert.error("Invalid format for discount %");
                    check_discount = true;
                }
                ;
            }
            ;
        });

        if (check_discount) {
            return false;
        }
        ;

        if (String(self.voucher_discount()).indexOf('%') !== -1) {
            bsalert.error("Invalid format for discount %");
            return false;
        }
        ;

        $.ajax({
            type: "POST",
            url: '/voucher/purchase/save/',
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
    self.discount = ko.observable(0);
    self.unit = ko.observable();
    self.unit_id = ko.observable();
    self.tax = ko.observable();
    self.tax_scheme_id = ko.observable();
    self.tax_scheme = ko.observable();
    self.lot_number = ko.observable();

    for (var k in row)
        self[k] = ko.observable(row[k]);

    self.item.subscribe(function (item) {
        // TODO
        var unit = get_by_id(purchase_vm.units(), item.unit.id);
        if (unit && !self.unit_id())
            self.unit_id(unit.id);
        if (item.last_purchase_price && !self.rate()) {
            self.rate(item.last_purchase_price);
        }
    });

    self.tax_rate = ko.computed(function () {
        var percent = 0;
        if (purchase_vm.tax() != 'exclusive') {
            if (purchase_vm.tax_scheme()) {
                percent = purchase_vm.tax_scheme().percent;
            }
            if (self.tax_scheme()) {
                percent = self.tax_scheme().percent;
            }
        }
        return 1 + parseFloat(percent) / 100; // percent to rate
    });

    self.tax_percent = ko.computed(function () {
        if (purchase_vm.tax() == 'no') {
            return 0;
        }
        else if (purchase_vm.tax_scheme()) {
            return parseFloat(purchase_vm.tax_scheme().percent);
        }
        else if (self.tax_scheme()) {
            return parseFloat(self.tax_scheme().percent);
        }
        return 0;

    });


    self.total = ko.computed(function () {
        if (purchase_vm.tax() == 'no' || purchase_vm.tax_scheme()) {
            return r2z(parseFloat(self.quantity()) * parseFloat(self.rate()) - parseFloat(self.discount()));
        }
        else if (purchase_vm.tax() == 'exclusive') {
            return r2z(parseFloat((self.quantity()) * parseFloat(self.rate()) - parseFloat(self.discount())) * (1 + self.tax_percent() / 100));
        }
        else if (purchase_vm.tax() == 'inclusive') {
            return r2z(parseFloat(self.quantity()) * parseFloat(self.rate()) - parseFloat(self.discount()));
        }
    });

    self.total_without_tax = ko.computed(function () {
        if (purchase_vm.tax() == 'no' || purchase_vm.tax() == 'exclusive') {
            return r2z(parseFloat(self.quantity()) * parseFloat(self.rate()) - parseFloat(self.discount()));
        }
        else if (purchase_vm.tax() == 'inclusive') {
            return r2z((100 / (100 + self.tax_percent())) * (parseFloat(self.quantity()) * parseFloat(self.rate()) - parseFloat(self.discount())));
        }
    });

    self.tax_amount = ko.computed(function () {
        if (purchase_vm.tax() == 'no' || purchase_vm.tax_scheme()) {
            return 0;
        }
        else {
            return self.tax_percent() * self.total_without_tax() / 100;
        }
    });

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
        purchase_vm
        var obj = get_by_id(purchase_vm.items(), data.id);
        return '<div>' + obj.full_name + '</div>';
    }

}