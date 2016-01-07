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
    
    self.file = ko.observableArray();
    self.deleted_file = ko.observableArray();

    self.upload_file = ko.observableArray([ new UploadFileVM() ]);

    self.add_upload_file = function() {
        self.upload_file.push( new UploadFileVM() );
    }

    self.remove_upload_file = function(file){
        self.upload_file.remove(file);
    };

    self.remove_file = function(file) {
        self.file.remove(file)
        self.deleted_file.push(file)
    };

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

    for (var k in data){
        if ( k == 'file') {
            for ( i in data[k]) {
                self.file.push( new FileViewModel( data[k][i] ));
            };
        } else {
            self[k] = ko.observable(data[k]);
        }
    };


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

        for ( index in self.upload_file()){
            if (typeof(self.upload_file()[index].upload_file()) != 'undefined') {
                form_data.append('file', self.upload_file()[index].upload_file())
            };
        };

        if ( !self.bank_account() ) {
            bsalert.error('Bank account field is required');
            return false;
        }

        if ( !self.benefactor() ) {
            bsalert.error('Benefactor field is required');
            return false;
        }

        form_data.append('cheque_deposit', ko.toJSON(self));
        $.ajax({
            type: "POST",
            url: '/bank/save/cheque_deposit/',
            data: form_data,
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
                        for ( i in msg.attachment ) {
                            self.file.push( new FileViewModel( msg.attachment[i] ));
                        };
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


function UploadFileVM(){
    var self = this;

    self.upload_file = ko.observable(); 
};

function FileViewModel(data){
    var self = this;

    self.id = ko.observable();
    self.attachment = ko.observable();
    self.attachment_name = ko.observable();

    for (var k in data)
        self[k] = ko.observable(data[k]);

    if(self.attachment()) {
        var attachment_name = self.attachment().split('/').pop();
        self.attachment_name(attachment_name);
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