$(document).ready(function () {
    vm = new FixedAssetViewModel(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});

function FixedAssetViewModel(data) {
    var self = this;

    self.id = ko.observable();
    self.voucher_no = ko.observable();
    self.date = ko.observable();
    self.from_account = ko.observable();
    self.accounts = ko.observable();
    self.description = ko.observable();

    $.ajax({
        url: '/ledger/api/account.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.accounts = ko.observableArray(data);
        }
    });

    self.table_view = new TableViewModel({rows: data.rows}, FixedAssetRowViewModel);
    self.addition_detail = new TableViewModel({rows: data.additional_details}, AdditionalDetailViewModel);


    self.id.subscribe(function (id) {
        update_url_with_id(id);
    });

    self.total = function() {
        var sum = 0;
        self.table_view.rows().forEach(function (i) {
            if (i.amount())
                sum += parseInt(i.amount());
        });
        return round2(sum);
    };

    for (var k in data){
            self[k] = ko.observable(data[k]);
    };

    self.save = function (item, event) {
        var form_data = new FormData()

        for ( index in self.upload_file()){
            if (typeof(self.upload_file()[index].upload_file()) != 'undefined') {
                var description;
                form_data.append('file', self.upload_file()[index].upload_file());
                if (typeof(self.upload_file()[index].description()) == 'undefined') {
                    description = '';
                } else {
                    description = self.upload_file()[index].description();
                };
                form_data.append('file_description', description);
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
                        $($("tbody > tr:not(.total, .file)")[i]).addClass('invalid-row');
                    });

                    if(typeof(msg.attachment) != "undefined") {
                        for ( i in msg.attachment ) {
                            self.file.push( new FileViewModel( msg.attachment[i] ));
                        };
                        self.upload_file([ new UploadFileVM() ])
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

function FixedAssetRowViewModel(row) {
    var self = this;

    self.id = ko.observable();
    self.asset_ledger = ko.observable();
    self.description = ko.observable();
    self.amount = ko.observable();

    for (var k in row)
        self[k] = ko.observable(row[k]);

}

function AdditionalDetailViewModel(row) {
    var self = this;
    self.id = ko.observable();
    self.assets_code = ko.observable();
    self.assets_type = ko.observable();
    self.vendor_name = ko.observable();
    self.vendor_address = ko.observable();
    self.amount = ko.observable();
    self.useful_life = ko.observable();
    self.description = ko.observable();
    self.warranty_period = ko.observable();
    self.maintenance = ko.observable();


    for (var k in row)
        self[k] = ko.observable(row[k]);

}