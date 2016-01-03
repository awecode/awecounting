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
    self.bank_account = ko.observable();
    self.attachment_name = ko.observable();
    self.attach_file = ko.observable()
    self.file = ko.observableArray();

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

    if(self.attachment()) {
        var attachment_name = self.attachment().split('/').pop();
        self.attachment_name(attachment_name);
    }

    self.id.subscribe(function (id) {
        update_url_with_id(id);
    });

    self.total = function() {
        var sum = 0;
        self.table_view.rows().forEach(function (i) {
            if (i.amount())
                sum += i.amount();
        });
        return round2(sum);
    };

    self.save = function (item, event) {
        var form_data = new FormData()
        if (typeof(self.attach_file()) != 'undefined') {
            form_data.append('attachment', self.attach_file());
        };
        form_data.append('cheque_deposit', ko.toJSON(self));
        $.ajax({
            type: "POST",
            url: '/bank/save/cheque_deposit/',
            data: form_data,
            // data: ko.toJSON(self),
            processData: false,
            contentType: false,
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    bsalert.error(msg.error_message);
                    self.status('errorlist');
                }
                else {
                    bsalert.success('Saved!');
                    if (msg.id)
                        self.id(msg.id);
                    $("tbody > tr").each(function (i) {
                        $($("tbody > tr:not(.total)")[i]).addClass('invalid-row');
                    });

                    if(typeof(msg.attachment) != "undefined") {
                        self.attachment(msg.attachment.url);
                        var attachment_name = self.attachment().split('/').pop()
                        self.attachment_name(attachment_name)
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


function FileViewModel(){
    var self = this;

    self.file = ko.observable();
    self.attachment_url = ko.observable();
    self.attachment_name = ko.observable();
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