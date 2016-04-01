$(document).ready(function () {
    vm = new EntryViewModel(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});

function EntryViewModel(data) {
    var self = this;

    self.id = ko.observable();
    self.entry_no = ko.observable();
    self.status = ko.observable();

    $.ajax({
        url: '/ledger/api/account.json',
        dataType: 'json',
        data: "categories=bank_account,cash_account",
        async: false,
        success: function (data) {
            self.pay_headings = ko.observableArray(data['results']);
        }
    });

    $.ajax({
        url: '/ledger/api/employee/account.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.employees = ko.observableArray(data['results']);
        }
    });

    self.table_view = new TableViewModel({rows: data.rows}, EntryRowViewModel);

    for (var k in data) {
        self[k] = ko.observable(data[k]);
    }

    self.id.subscribe(function (id) {
        update_url_with_id(id);
    });

    self.sub_total = function () {
        var sum = 0;
        self.table_view.rows().forEach(function (i) {
            if (i.amount()) {
                sum += parseFloat(i.amount());
            }
        });
        return sum;
    }

    self.save = function (item, event) {
        var form_data = new FormData()

        form_data.append('entry', ko.toJSON(self));
        $.ajax({
            type: "POST",
            url: '/payroll/entry/save/',
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
                        $($("tbody > tr")[i]).removeClass('invalid-row');
                    }

                    if (typeof(msg.attachment) != "undefined") {
                        for (i in msg.attachment) {
                            self.file.push(new FileViewModel(msg.attachment[i]));
                        }
                        ;
                        self.upload.files([new File()])
                    }
                }
            }
        });
    }

}


function EntryRowViewModel(row) {
    var self = this;

    self.id = ko.observable();
    self.amount = ko.observable();
    self.hours = ko.observable();
    self.employee_id = ko.observable();
    self.employee = ko.observable();
    self.pay_heading_id = ko.observable();
    self.pay_heading = ko.observable();
    self.tax = ko.observable();
    self.remarks = ko.observable();

    for (var k in row)
        self[k] = ko.observable(row[k]);

}