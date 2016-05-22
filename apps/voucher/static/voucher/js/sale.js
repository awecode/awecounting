$(document).ready(function () {
    vm = new SaleViewModel(ko_data);
    ko.applyBindings(vm);
});


function TaxViewModel(tax, tax_scheme){
    var self = this;
    var choices = [
        {
            'id': 'inclusive',
            'value' : 'Tax Inclusive',
        },
        {
            'id': 'exclusive',
            'value' : 'Tax Exclusive',
        },
        {
            'id' : 'no',
            'value' : 'No Tax',
        },
    ]

    self.tax = ko.observable(tax);
    self.tax_scheme = ko.observable();
    self.tax_choices = ko.observableArray(choices);
    self.tax_scheme_visibility = ko.observable(true);
  
    if (tax_scheme) {
        self.tax_scheme(tax_scheme);
    };

    if (self.tax() == 'no') {
        self.tax_scheme_visibility(false);
    };

    self.tax.subscribe(function() {
        if (self.tax() == 'no') {
            self.tax_scheme_visibility(false);
        };
        if (self.tax() != 'no' && self.tax_scheme_visibility() == false ){
            self.tax_scheme_visibility(true);
        }
    });

    self.get_scheme = function() {
        var bool;
        if (self.tax_scheme() == '' ) {
            bool = true;
        };  
        $( "tr.total td:first-child" ).each(function() {
            if (self.tax_scheme_visibility() && bool) {
              $( this ).attr( "colspan", colspan + 1 );
            } else {
              $( this ).attr( "colspan", colspan );
            }
        });
        return self.tax_scheme_visibility() && bool;
    };
}


function SaleViewModel(data) {
    var self = this;

    
    self.tax = ko.observable();
    self.tax_scheme = ko.observable();

    self.voucher_discount = ko.observable(0);
    for (var k in data) {
        if ( k == 'discount' ) {
            self.voucher_discount(data[k])
        };
        self[k] = ko.observable(data[k]);
    }

    $.ajax({
        url: '/tax/api/tax_schemes.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.tax_schemes = ko.observableArray(data);
        }
    });

    self.tax_vm = new TaxViewModel(self.tax(), self.tax_scheme());

    self.tax_vm.tax_scheme.subscribe( self.tax_vm.get_scheme );

    self.party = ko.observable();
    self.status = ko.observable();

    $.ajax({
        url: '/inventory/api/items.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.items = ko.observableArray(data);
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

    $.ajax({
        url: '/inventory/api/units.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.units = ko.observableArray(data);
        }
    });

    self.party_balance = ko.computed(function () {
        if (self.party())
            return self.party().balance;
    });

    self.table_view = new TableViewModel({rows: data.rows, argument: self}, SaleRow);

    self.sub_total = function () {
        var sum = 0;
        self.table_view.rows().forEach(function (i) {
            if (i.total()) {
                sum += parseFloat(i.total());
            }
        });
        return round2(sum);
    }

    self.discount = function () {
        var sum = 0;
        self.table_view.rows().forEach(function (i) {
            if (String(i.discount()).indexOf('%') !== -1 ) {
                var total = i.rate() * i.quantity();
                var amount = ( parseFloat(i.discount()) / 100 ) * total
                sum += parseFloat(amount);
            } else if (i.discount()) {
                sum += parseFloat(i.discount());
            }
        });
        return r2z(round2(sum));
    }


    self.tax_amount = function () {
        var sum = 0;
        if (self.tax_vm.get_scheme()) {
            self.table_view.rows().forEach(function (i) {
                if (i.tax_amount()) {
                    sum += parseFloat(i.tax_amount());
                }
            });
        } 
        if (self.tax_vm.tax_scheme() != '') {
            tax_percent = $.grep(self.tax_schemes(), function(e){ return e.id == self.tax_vm.tax_scheme(); })[0].percent;
            if (self.tax_vm.tax() == 'inclusive') {
                _sum = self.sub_total() * (tax_percent / (100 + tax_percent))
            } else if (self.tax_vm.tax() == 'exclusive') {
                _sum = self.sub_total() * ( tax_percent / 100 );
            } else {
                _sum = 0
            }
            return r2z(round2(_sum));
        } 
        return r2z(round2(sum));
    }

    self.total_amount = 0;

    self.grand_total = function () {
        self.total_amount = rnum(self.sub_total());
        if (vm.tax_vm.tax() == 'exclusive') {
            self.total_amount = self.sub_total() + self.tax_amount();
        }
        if (self.voucher_discount() > 0 ) {
            self.total_amount = self.total_amount - self.voucher_discount()
        } else if (String(self.voucher_discount()).indexOf('%') !== -1 ) {
            self.total_amount = self.total_amount - ( ( parseFloat(self.voucher_discount()) / 100 ) * self.total_amount )
        }
        return r2z(self.total_amount);
    }

    self.save = function (item, event) {
        if (self.credit() && !self.party()) {
            bsalert.error('Party is required for credit sale!');
            return false;
        }

        var check_discount;
        self.table_view.rows().forEach(function (i) {
            var discount_as_string = String(i.discount());
            if (discount_as_string.indexOf('%') !== -1) {
                if (typeof(discount_as_string[ discount_as_string.indexOf('%') + 1]) != 'undefined' ) {
                    bsalert.error("Discount '%' not in correct order");
                    check_discount = true;
                };
            };
        });

        if (check_discount) {
            return false;
        };

        if (String(self.voucher_discount()).indexOf('%') !== -1 ) {
            bsalert.error("Discount '%' not in correct order");
            return false;        
        };

        $.ajax({
            type: "POST",
            url: '/voucher/sale/save/',
            data: ko.toJSON(self),
            success: function (msg) {
                if (msg.id)
                    self.id(msg.id);
                if (typeof (msg.error_message) != 'undefined') {
                    bsalert.error(msg.error_message);
                    self.status('errorlist');
                }
                else {
                    bsalert.success('Saved!');
                    self.table_view.deleted_rows([]);
                    $("tbody > tr:not(.total)").each(function (i, el) {
                        $(el).addClass('invalid-row');
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

    self.id.subscribe(function (id) {
        update_url_with_id(id);
    });

    self.sub_total = function () {
        var sum = 0;
        self.table_view.rows().forEach(function (i) {
            if (i.total()) {
                sum += parseFloat(i.total());
            }
        });
        return round2(sum);
    }
}


function SaleRow(row, sale_vm) {
    var self = this;

    self.item = ko.observable();
    self.item_id = ko.observable();
    self.quantity = ko.observable();
    self.rate = ko.observable();
    self.discount = ko.observable(0);
    self.unit = ko.observable();
    self.unit_id = ko.observable();
    self.tax = ko.observable();
    self.tax_scheme = ko.observable();

    for (var k in row)
        self[k] = ko.observable(row[k]);

    self.item.subscribe(function (item) {
        if (item.unit) {
            var unit = get_by_id(sale_vm.units(), item.unit.id);
            if (!self.unit_id())
                self.unit_id(unit.id);
            if (!self.rate()) {
                self.rate(item.selling_rate);
            }
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

    self.total = ko.computed(function () {
        if (self.discount() > 0) {
            var total = self.quantity() * self.rate();
            return round2(total - self.discount());
        } else {
            return round2(self.quantity() * self.rate());
        }
    });

    self.row_tax_vm = new TaxViewModel(self.tax(), self.tax_scheme());

    self.tax_amount = ko.observable();

    self.calculate_tax_amount = function() {
        var tax_total = 0;
        if (self.row_tax_vm.tax_scheme() != '') {
            tax_percent = $.grep(sale_vm.tax_schemes(), function(e){ return e.id == self.row_tax_vm.tax_scheme(); })[0].percent;
        if (vm.tax_vm.tax() == 'inclusive') {
            tax_total = self.total() * (tax_percent / (100 + tax_percent))
        } else if (vm.tax_vm.tax() == 'exclusive') {
            tax_total = self.total() * ( tax_percent / 100 );
        } 
        } else {
            tax_total = 0
        };
        self.tax_amount(tax_total);
    };

    self.row_tax_vm.tax_scheme.subscribe( self.calculate_tax_amount );
    self.total.subscribe( self.calculate_tax_amount );
    sale_vm.tax_vm.tax.subscribe( self.calculate_tax_amount );
    //self.render_selected_unit = function (data) {
    //    var obj = get_by_id(sale_vm.units(), data.id);
    //    return '<div>' + obj.name + '</div>';
    //}

    self.render_unit_options = function (data) {
        var obj = get_by_id(sale_vm.units(), data.id);
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
        var obj = get_by_id(sale_vm.items(), data.id);
        return '<div>' + obj.full_name + '</div>';
    }

}