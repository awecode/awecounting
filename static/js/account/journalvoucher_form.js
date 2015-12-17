$(document).ready(function () {
    vm = new JournalVoucherViewModel(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});

function JournalVoucherViewModel(){
	
}