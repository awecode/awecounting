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
            self.accounts = ko.observableArray(data['results']);
        }
    });

    self.table_view = new TableViewModel({rows: data.rows}, FixedAssetRowViewModel);
    self.additional_detail = new TableViewModel({rows: data.additional_details}, AdditionalDetailViewModel);


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

        if ( !self.from_account() ) {
            bsalert.error('From Account field is required');
            return false;
        }

        form_data.append('fixed_asset', ko.toJSON(self));
        $.ajax({
            type: "POST",
            url: '/voucher/fixed_asset/save/',
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
                    self.table_view.deleted_rows([]);
                    if (msg.id)
                        self.id(msg.id);
                    $("tbody > tr").each(function (i) {
                        $($("tbody > tr:not(.total, .file)")[i]).addClass('invalid-row');
                    });

                    for (var i in msg.rows) {
                        self.table_view.rows()[i].id = msg.rows[i];
                        $($("tbody.fixed_asset_row > tr")[i]).removeClass('invalid-row');
                    }
                    for (var i in msg.additional_detail) {
                        self.additional_detail.rows()[i].id = msg.additional_detail[i];
                        $($("tbody.additional_details > tr")[i]).removeClass('invalid-row');
                    }
                }
            }
        });
    };

    self.id.subscribe(function (id) {
        update_url_with_id(id);
    });



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