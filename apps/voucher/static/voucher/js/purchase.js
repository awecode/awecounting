$(document).ready(function () {
    vm = new PurchaseViewModel(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});

function TaxViewModel(tax, tax_scheme, tax_schemes){
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
    self.tax_choices = ko.observableArray(choices);
    self.tax_scheme_visibility = ko.observable(true);

    self.tax_scheme = new TaxSchemeViewModel(tax_scheme, tax_schemes);

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
}

function TaxSchemeViewModel(tax_scheme, tax_schemes) {
    var self = this;
    self.tax_scheme = ko.observable();
    if (tax_scheme) {
        self.tax_scheme(tax_scheme);
    };

    self.tax_schemes = ko.observableArray(tax_schemes);

}

function PurchaseViewModel(data) {
    var self = this;
    
    self.tax = ko.observable();
    self.tax_scheme = ko.observable();

    for (var k in data)
        self[k] = ko.observable(data[k]);

    self.status = ko.observable();
    
    

    $.ajax({
        url: '/tax/api/tax_schemes.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.tax_schemes = ko.observableArray(data);
        }
    });

    self.tax_vm = new TaxViewModel(self.tax(), self.tax_scheme(), self.tax_schemes());

    self.get_scheme = function() {
        var bool;
        if (self.tax_vm.tax_scheme.tax_scheme() == '' || self.tax_vm.tax_scheme.tax_scheme() == 0 ) {
            bool = true;
        };
        return self.tax_vm.tax_scheme_visibility() && bool;
    };

    self.tax_vm.tax_scheme.tax_scheme.subscribe( self.get_scheme );

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

    self.party = ko.observable();

    self.party_balance = ko.computed(function () {
        if (self.party())
            return -1 * self.party().balance;
    });

    self.table_view = new TableViewModel({rows: data.rows, argument: self}, PurchaseRow);

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

    self.tax_amount = function () {
        var sum = 0;
        if (self.get_scheme()) {
            self.table_view.rows().forEach(function (i) {
                if (i.tax_amount()) {
                    sum += parseFloat(i.tax_amount());
                }
            });
        } 
        if (self.tax_vm.tax_scheme.tax_scheme() != '') {
            tax_percent = $.grep(vm.tax_schemes(), function(e){ return e.id == self.tax_vm.tax_scheme.tax_scheme(); })[0].percent;
            if (self.tax_vm.tax() == 'inclusive') {
                _sum = self.sub_total() * (tax_percent / (100 + tax_percent))
            } else if (self.tax_vm.tax() == 'exclusive') {
                _sum = self.sub_total() * ( tax_percent / 100 );
            } else {
                sum = 0
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
        return self.total_amount;
    }

    self.save = function (item, event) {
        if (!self.party()) {
            bsalert.error('Party is required!');
            return false;
        }
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
                    if (msg.tax == 'no'){
                        for (var i in msg.rows) {
                            self.table_view.rows()[i].row_tax_vm.tax_scheme.tax_scheme(0);
                        }
                    }
                    if (msg.tax_scheme_id != "" && msg.tax_scheme_id != null){
                    for (var i in msg.rows) {
                        self.table_view.rows()[i].row_tax_vm.tax_scheme.tax_scheme(0);
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
    self.discount = ko.observable(0);
    self.unit = ko.observable();
    self.unit_id = ko.observable();
    self.tax_scheme = ko.observable();
    self.tax = ko.observable();

    for (var k in row)
        self[k] = ko.observable(row[k]);

    self.item.subscribe(function (item) {
        // TODO
        var unit = get_by_id(purchase_vm.units(), item.unit.id);
        if (unit && !self.unit_id())
            self.unit_id(unit.id);
    });

    self.total = ko.computed(function () {
        if (self.discount() > 0) {
            var total = self.quantity() * self.rate()
            return round2(total - self.discount());
        } else {
            return round2(self.quantity() * self.rate());
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


    self.row_tax_vm = new TaxViewModel(self.tax(), self.tax_scheme(), purchase_vm.tax_schemes());

    self.tax_amount = ko.observable();

    self.calculate_tax_amount = function() {
        var tax_total = 0;
        if (self.row_tax_vm.tax_scheme.tax_scheme() != '') {
            tax_percent = $.grep(vm.tax_schemes(), function(e){ return e.id == self.row_tax_vm.tax_scheme.tax_scheme(); })[0].percent;
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


    self.row_tax_vm.tax_scheme.tax_scheme.subscribe( self.calculate_tax_amount );
    self.total.subscribe( self.calculate_tax_amount );
    purchase_vm.tax_vm.tax.subscribe( self.calculate_tax_amount );

    self.render_option = function (data) {
        var obj = get_by_id(purchase_vm.items(), data.id);
        return '<div>' + obj.full_name + '</div>';
    }

}