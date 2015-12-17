$(document).ready(function () {
    vm = new JournalVoucherViewModel(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});

function JournalVoucherViewModel(){
	var self = this

	self.id =  ko.observable();
	self.voucher_no = ko.observable();
	self.date = ko.observable();
	self.narration = ko.observable();
	self.status = ko.observable();

    self.table_view = new TableViewModel({rows: data.rows}, JournalVoucherRowViewModel);

}

function JournalVoucherRowViewModel(rows) {
	var self = this;

	self.id = ko.observable();
	self.type = ko.observable();
	self.description = ko.observable();
	self.cr_amount = ko.observable();
	self.dr_amount = ko.observable();
	self.account = ko.observable();

}