$(document).ready(function () {
    vm = new SaleViewModel(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});

function SaleViewModel(data) {
    var self = this;

    self.status = ko.observable();

    $.ajax({
        url: '/inventory/api/items.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.items = ko.observableArray(data);

        }
    });

    self.item_changed = function (row) {
        var selected_item = $.grep(self.items(), function (i) {
            return i.id == row.item_id();
        })[0];
        if (selected_item.selling_rate)
            row.rate(selected_item.selling_rate)
        else
            row.rate('')
        row.unit_id(selected_item.unit_id)
        if (!selected_item) return;
    }

    $.ajax({
        url: '/ledger/api/parties.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.parties = ko.observableArray(data);
        }
    });
    self.party = ko.observable()
    self.party_name = ko.observable();
    self.party_address = ko.observable();
    self.party_pan_no = ko.observable();

    self.party_changed = function (obj) {
        if (typeof(obj.party()) == 'undefined')
            return false;
        var selected_obj = $.grep(self.parties(), function (i) {
            return i.id == obj.party();
        })[0];
        if (!selected_obj) return;
        obj.party_address(selected_obj.address);
        obj.party_name(selected_obj.name);
        obj.party_pan_no(selected_obj.pan_no);
    }

    $.ajax({
        url: '/inventory/api/units.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.units = ko.observableArray(data);
        }
    });

    //self.unit_changed = function (row) {
    //    var selected_item = $.grep(self.units(), function (i) {
    //        return i.id == row.unit_id();
    //    })[0];
    //    if (!selected_item) return;
    //}

    self.table_view = new TableViewModel({rows: data.rows, argument: self}, SaleRow);

    for (var k in data)
        self[k] = ko.observable(data[k]);

    self.save = function (item, event) {
        if (self.credit() && !self.party()) {
            bsalert.error('Party is required for credit sale!');
            return false;
        }
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

    self.id.subscribe(function (id) {
        history.pushState(id, id, window.location.href + id + '/');
    });

    self.sub_total = function () {
        var sum = 0;
        self.table_view.rows().forEach(function (i) {
            sum += i.total();
        });
        return sum;
    }
}


function SaleRow(row, sale_vm) {
    var self = this;

    self.item = ko.observable();
    self.item_id = ko.observable();
    self.quantity = ko.observable();
    self.rate = ko.observable();
    self.discount = ko.observable(0);

    self.unit_id = ko.observable();

    for (var k in row)
        self[k] = ko.observable(row[k]);

    self.item.subscribe(function (item) {
        var unit = get_by_id(sale_vm.units(), item.unit.id);
        if (unit) {
            self.unit_id(unit.id);
        } else {
            purchase_vm.units.push(unit);
            self.unit_id(unit.id);
        }
    });


    self.total = ko.computed(function () {
        if (self.discount() > 0) {
            var total = self.quantity() * self.rate();
            return round2(total - self.discount());
        } else {
            return round2(self.quantity() * self.rate());
        }
    })

    self.render_option = function (data) {
        var obj = get_by_id(sale_vm.items(), data.id);
        return '<div>' + obj.full_name + '</div>';
    }

}