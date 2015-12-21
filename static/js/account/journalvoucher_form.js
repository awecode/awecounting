$(document).ready(function () {
    vm = new JournalVoucherViewModel(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});

function JournalVoucherViewModel(data){
	var self = this;

	self.id =  ko.observable();
	self.voucher_no = ko.observable();
	self.date = ko.observable();
	self.narration = ko.observable();
	self.status = ko.observable();

    $.ajax({
        url: '/ledger/api/account/?format=json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.accounts = ko.observableArray(data);
        }
    });

    self.table_view = new TableViewModel({rows: data.rows}, JournalVoucherRowViewModel);

    for (var k in data)
        self[k] = ko.observable(data[k]);

    self.total_dr_amount = ko.computed(function() {
        total = 0;
        for (o in self.table_view.rows()) {
            if (self.table_view.rows()[o].dr_amount()) {
                total += parseInt(self.table_view.rows()[o].dr_amount());
            };
        }
        return total;
    });

    self.total_cr_amount = ko.computed(function() {
        total = 0;
        for (o in self.table_view.rows()) {
            if (self.table_view.rows()[o].cr_amount()) {
                total += parseInt(self.table_view.rows()[o].cr_amount());
            };
        }
        return total;
    });

    self.add_row = function (element, viewModel) {
        $(element).blur();
        var type;
        var dr_amount;
        var cr_amount;
        debugger;
        var diff = self.total_dr_amount() - self.total_cr_amount()
        if (diff > 0) {
            type = 'Cr';
            dr_amount = 0;
            cr_amount = diff;
        } else {
            type = 'Dr';
            cr_amount = 0;
            dr_amount = (-1) * diff;
        }

        if ($(element).closest("tr").is(":nth-last-child(2)") && self.total_dr_amount() != self.total_cr_amount())
            self.table_view.rows.push(new JournalVoucherRowViewModel({type: type, cr_amount: cr_amount, dr_amount: dr_amount}));
    }


}

function JournalVoucherRowViewModel(row) {
	var self = this;

    self.account_type = ko.observableArray(['Dr','Cr']);
	self.id = ko.observable();
	self.type = ko.observable();
	self.description = ko.observable();
	self.cr_amount = ko.observable();
	self.dr_amount = ko.observable();
	self.account = ko.observable();

    for (var k in row)
        self[k] = ko.observable(row[k]);

    self.is_dr = ko.computed(function() {
        if(self.type() == "Dr")
            return true
        return false
    });

    self.is_cr = ko.computed(function() {
        if(self.type() == "Cr")
            return true
        return false
    });

    self.type.subscribe(function(type) {
        self.dr_amount('');
        self.cr_amount('');
    }); 
}