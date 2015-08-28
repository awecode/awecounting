$(document).ready(function () {
    vm = new SaleViewModel(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});

function SaleViewModel(data) {
	var self = this;

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
        if (!selected_item) return;
    }

    $.ajax({
        url: '/inventory/api/parties.json',
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

    self.table_view = new TableViewModel({rows: data.rows}, SaleRow);


    for (var k in data)
        self[k] = ko.observable(data[k]);

    self.save = function (item, event) {
        $.ajax({
            type: "POST",
            url: '/inventory/save/sale/',
            data: ko.toJSON(self),
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    alert.error(msg.error_message);
                    self.status('errorlist');
                }
                else {
                    alert.success('Saved!');
                    if (msg.id)
                        self.id(msg.id);
                    $("#tbody > tr").each(function (i) {
                        $($("#tbody > tr")[i]).addClass('invalid-row');
                    });
                    for (var i in msg.rows) {
                        self.table_view.rows()[i].id = msg.rows[i];
                        $($("#tbody > tr")[i]).removeClass('invalid-row');
                    }
                }
            }
        });
    }
}


function SaleRow(row) {
	var self = this;

	self.item_id = ko.observable()
	self.quantity = ko.observable()
	self.rate = ko.observable()

    $.ajax({
        url: '/inventory/api/units.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.units = ko.observableArray(data);
        }
    });

	self.unit_id = ko.observable()

    for (var k in row)
        self[k] = ko.observable(row[k]);

}