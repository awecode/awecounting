$(document).ready(function () {
    vm = new ChequeDepositViewModel(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});

function ChequeDepositViewModel(data) {
    var self = this;

    self.id = ko.observable();
    self.voucher_no = ko.observable();
    self.date = ko.observable();
    self.narration = ko.observable();
    self.status = ko.observable();
    self.benefactor = ko.observable();
    self.bank_account = ko.observable()
    $.ajax({
        url: '/ledger/api/bank_account/account.json/',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.bank_account_array = ko.observableArray(data);
        }
    });

    $.ajax({
        url: '/ledger/api/account.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.benefactor_array = ko.observableArray(data);
        }
    });

    self.table_view = new TableViewModel({rows: data.rows}, ChequeDepositRowViewModel);

    for (var k in data)
        self[k] = ko.observable(data[k]);

    self.save = function (item, event) {
        if (self.total_cr_amount() !== self.total_dr_amount()) {
            bsalert.error('Total Dr and Cr amounts don\'t tally!');
            return false;
        }

        //if (self.check_description()){
        //    bsalert.error('Description isn\'t provided!');
        //    return false;
        //}

        $.ajax({
            type: "POST",
            url: '/ledger/save/journal_voucher/',
            data: ko.toJSON(self),
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    bsalert.error(msg.error_message);
                    self.status('errorlist');
                }
                else {
                    bsalert.success('Saved!');
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

function ChequeDepositRowViewModel(row) {
    var self = this;

    self.id = ko.observable();
    self.cheque_number = ko.observable();
    self.cheque_date = ko.observable();
    self.drawee_bank = ko.observable();
    self.drawee_bank_address = ko.observable();
    self.amount = ko.observable();

    for (var k in row)
        self[k] = ko.observable(row[k]);

}