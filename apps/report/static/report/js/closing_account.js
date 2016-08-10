$(document).ready(function () {
    vm = new ClosingAccountVM();
    var closing_account_form = document.getElementById("closing_account");
    ko.applyBindings(vm, closing_account_form);
});

function ClosingAccountVM() {
    var self = this;

    self.fiscal_year = ko.observable();

    self.next_fiscal_year = ko.computed(function() {
        if(self.fiscal_year() >= 1000) {
            return parseInt(self.fiscal_year()) + 1;
        }
    });

}
