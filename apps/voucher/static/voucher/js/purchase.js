$(document).ready(function () {
    vm = new PurchaseViewModel(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
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
    self.tax_choices = ko.observableArray(choices);
    self.tax_scheme = ko.observable();
    self.tax_scheme_visibility = ko.observable(true);

    if (self.tax() == 'no') {
        self.tax_scheme_visibility(false);
    };

    $.ajax({
        url: '/tax/api/tax_schemes.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.tax_schemes = ko.observableArray(data);
        }
    });

    if (tax_scheme) {
        self.tax_scheme(tax_scheme);
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

function PurchaseViewModel(data) {
    var self = this;

    for (var k in data)
        self[k] = ko.observable(data[k]);

    self.status = ko.observable();

    self.tax_vm = new TaxViewModel(self.tax(), self.tax_scheme());

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

    for (var k in row)
        self[k] = ko.observable(row[k]);

    self.item.subscribe(function (item) {
        //debugger;
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
    })

    self.render_option = function (data) {
        var obj = get_by_id(purchase_vm.items(), data.id);
        return '<div>' + obj.full_name + '</div>';
    }

}