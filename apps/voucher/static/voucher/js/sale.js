$(document).ready(function () {
    vm = new SaleViewModel(ko_data, voucher_settings);
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
function SaleRowLocation(data){
    var self = this;
    self.location_id = ko.observable(data.location_id);
    self.location_name = ko.observable(data.location_name);
    self.qty = ko.observable(data.qty);
    if (data.selected_qty){
        self.selected_qty = ko.observable(data.selected_qty);
    }else{
        self.selected_qty = ko.observable(0);
    };
    self.adjust_selected_qty = ko.computed(function(){
        if (self.selected_qty() > self.qty()){
            self.selected_qty(self.qty());
        };
    });

};


function SaleViewModel(data, settings) {
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
    self.tax_scheme_id = ko.observable();

    self.voucher_discount = ko.observable(0);

    for (var k in data) {
        if (k == 'discount') {
            self.voucher_discount(data[k]);
        }
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

    $.ajax({
        url: '/inventory/api/sale/items.json',
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

    self.party = ko.observable();

    self.party_id.subscribe(function (id) {
        var selected_party = ko.utils.arrayFirst(self.parties(), function (p) {
            return p.id == id;
        });
        if (selected_party) {
            if (selected_party.tax_preference != null) {
                self.tax_vm.tax_scheme(selected_party.tax_preference.tax_scheme);
                if (selected_party.tax_preference.default_tax_application_type != 'no-peference' && selected_party.tax_preference.default_tax_application_type != null) {
                    self.tax_vm.tax(selected_party.tax_preference.default_tax_application_type);
                }
            }
        }
    });

    self.party_balance = ko.computed(function () {
        if (self.party())
            return -1 * self.party().balance;
    });

    self.render_party_options = function (data) {
        var obj = get_by_id(vm.parties(), data.id);
        var klass = '';
        if (obj.related_company != null) {
            klass = 'green';
        }
        return '<div class="' + klass + '">' + obj.name + '</div>';
    }
    self.table_view = new TableViewModel({rows: data.rows, argument: self}, SaleRow);

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
                var amount = ( parseFloat(i.discount()) / 100 ) * total;
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
    }

    self.total_amount = 0;

    self.grand_total = function () {
        return r2z(self.taxable_amount() + self.tax_amount());
    }

    self.save = function (item, event) {
        if (!self.party()) {
            bsalert.error('Party is required!');
            return false;
        }
        for(var row of vm.table_view.rows()){
          if(row.sale_row_location_error()){
              bsalert.error('Error in location Selection');
              return false;
          };
        };

        var check_discount;
        self.table_view.rows().forEach(function (i) {
            var discount_as_string = String(i.discount());
            if (discount_as_string.indexOf('%') !== -1) {
                if (typeof(discount_as_string[discount_as_string.indexOf('%') + 1]) != 'undefined') {
                    bsalert.error("Invalid format for discount %");
                    check_discount = true;
                }
            }
        });

        if (check_discount) {
            return false;
        }

        if (String(self.voucher_discount()).indexOf('%') !== -1) {
            bsalert.error("Invalid format for discount %");
            return false;
        }

        $.ajax({
            type: "POST",
            url: '/voucher/sale/save/',
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

    if (settings.sale_suggest_by_party_item) {
        self.party.subscribe(function (party) {
            $.ajax({
                url: '/voucher/api/sale/party/' + party.id + '/rates.json',
                dataType: 'json',
                async: false,
                success: function (data) {
                    ko.utils.arrayForEach(data, function (rate_item) {
                        var item = ko.utils.arrayFirst(self.items(), function (itm) {
                            return itm.id == rate_item.id;
                        });
                        item.last_sale_price = rate_item.last_sale_price;
                    });
                }
            });
        })
    }
}


function SaleRow(row, sale_vm) {
    var self = this;

    self.item = ko.observable();
    self.code = ko.observable();
    self.oem_number = ko.observable();
    self.item_id = ko.observable();
    self.quantity = ko.observable();
    self.rate = ko.observable();
    self.discount = ko.observable(0);
    self.unit = ko.observable();
    self.unit_id = ko.observable();
    self.tax = ko.observable();
    self.tax_scheme_id = ko.observable();
    self.tax_scheme = ko.observable();

    for (var k in row)
        self[k] = ko.observable(row[k]);

    self.item.subscribe(function (item) {
        self.code(item.code);
        self.oem_number(item.oem_no);
        // TODO
        var unit = get_by_id(sale_vm.units(), item.unit.id);
        if (!unit) {
            //    if unit not found, the unit is newly added from item form, add
            sale_vm.units.push(item.unit);
            unit = item.unit;
            self.unit_id(unit.id);
        }
        if (unit && !self.unit_id())
            self.unit_id(unit.id);
        if (item.last_sale_price && !self.rate()) {
            self.rate(item.last_sale_price);
        }
    });

    self.tax_rate = ko.computed(function () {
        var percent = 0;
        if (sale_vm.tax() != 'exclusive') {
            if (sale_vm.tax_scheme()) {
                percent = sale_vm.tax_scheme().percent;
            }
            if (self.tax_scheme()) {
                percent = self.tax_scheme().percent;
            }
        }
        return 1 + parseFloat(percent) / 100; // percent to rate
    });

    self.tax_percent = ko.computed(function () {
        if (sale_vm.tax() == 'no') {
            return 0;
        }
        else if (sale_vm.tax_scheme()) {
            return parseFloat(sale_vm.tax_scheme().percent);
        }
        else if (self.tax_scheme()) {
            return parseFloat(self.tax_scheme().percent);
        }
        return 0;

    });


    self.total = ko.computed(function () {
        if (sale_vm.tax() == 'no' || sale_vm.tax_scheme()) {
            return r2z(parseFloat(self.quantity()) * parseFloat(self.rate()) - parseFloat(self.discount()));
        }
        else if (sale_vm.tax() == 'exclusive') {
            return r2z(parseFloat((self.quantity()) * parseFloat(self.rate()) - parseFloat(self.discount())) * (1 + self.tax_percent() / 100));
        }
        else if (sale_vm.tax() == 'inclusive') {
            return r2z(parseFloat(self.quantity()) * parseFloat(self.rate()) - parseFloat(self.discount()));
        }
    });

    self.total_without_tax = ko.computed(function () {
        if (sale_vm.tax() == 'no' || sale_vm.tax() == 'exclusive') {
            return r2z(parseFloat(self.quantity()) * parseFloat(self.rate()) - parseFloat(self.discount()));
        }
        else if (sale_vm.tax() == 'inclusive') {
            return r2z((100 / (100 + self.tax_percent())) * (parseFloat(self.quantity()) * parseFloat(self.rate()) - parseFloat(self.discount())));
        }
    });

    self.tax_amount = ko.computed(function () {
        if (sale_vm.tax() == 'no' || sale_vm.tax_scheme()) {
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
        //sale_vm
        var obj = get_by_id(sale_vm.items(), data.id);
        return '<div>' + obj.full_name + '</div>';
    }

    // Location Logic Start
    self.sale_row_locations = ko.observableArray();
    self.sale_row_location_error = ko.observable();
    self.get_item_locations = ko.computed(function(){
        // console.log(self.id());
        // console.log('hey', self.item_id(), self.quantity());
        if(self.item_id()){
            if(typeof(self.id) != 'undefined'){
                 $.ajax({
                    url: '/voucher/sale_row_onedit_location_item_details/' + parseInt(self.id()) + '/' + parseInt(self.item_id()),
                    dataType: 'json',
                    async: false,
                    success: function (res1) {
                        self.sale_row_locations(ko.utils.arrayMap(res1.data, function(obj) {
                            return new SaleRowLocation(obj)
                        }));
                    }
                 });
            }else{

                $.ajax({
                    url: '/voucher/get_item_locations/' + parseInt(self.item_id()),
                    dataType: 'json',
                    async: false,
                    success: function (res) {
                        // var remain_qty = self.quantity();
                        // self.sale_row_locations([]);
                        //
                        // for(var obj of res.data){
                        //     if(remain_qty-obj.qty > 0){
                        //         obj.selected_qty = obj.qty;
                        //         remain_qty -= obj.selected_qty;
                        //     }else{
                        //         obj.selected_qty = remain_qty;
                        //         remain_qty -= obj.selected_qty;
                        //     };
                        // };
                        self.sale_row_locations(ko.utils.arrayMap(res.data, function(obj) {
                            return new SaleRowLocation(obj)
                        }));
                    }
                });
            };
        };

    });
    self.total_out4mloc = ko.computed(function(){
        var total = 0;
        for(var object of self.sale_row_locations()){
            if(object.selected_qty()){
                total += parseInt(object.selected_qty());
            };
        };
        if (self.quantity()){
            if (total > parseInt(self.quantity())){
                self.sale_row_location_error('Quantity in locations exceeds required quantity');
                // console.log('set');
            }else if (total < parseInt(self.quantity())){
                self.sale_row_location_error('Quantity in locations is less than required quantity');
                // console.log('unset', total, self.quantity());
            }else{
                self.sale_row_location_error(null);
            };
        };
    });

    self.suggest_qty_4m_location = ko.computed(function(){
        if(self.quantity()){
            var remain_qty = self.quantity();
            // self.sale_row_locations([]);
            //
            for(var obj of self.sale_row_locations()){
                if(remain_qty-obj.qty > 0){
                    obj.selected_qty(obj.qty());
                    remain_qty -= obj.qty();
                }else{
                    obj.selected_qty(remain_qty);
                    remain_qty -= remain_qty;
                };
            };
        };
    });
    // Location logic end

}