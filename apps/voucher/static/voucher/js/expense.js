$(document).ready(function () {
    vm = new ExpenseViewModel(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});

function ExpenseViewModel(data) {
    var self = this;

    self.id = ko.observable();
    self.voucher_no = ko.observable();
    self.date = ko.observable();
    
    //$.ajax({
    //    url: '/ledger/api/account.json',
    //    dataType: 'json',
    //    data: "categories=direct_expenses,indirect_expenses",
    //    async: false,
    //    success: function (data) {
    //        self.expense_accounts = ko.observableArray(data);
    //    }
    //});

    self.expense_accounts = ko.observableArray(data.expense_accounts);


    //$.ajax({
    //    url: '/ledger/api/bank_cash_account.json',
    //    dataType: 'json',
    //    async: false,
    //    success: function (data) {
    //    self.pay_head_accounts = ko.observableArray(data);
    //    }
    //});

    self.pay_head_accounts = ko.observableArray(data.pay_head_accounts);

    self.table_view = new TableViewModel({rows: data.rows}, ExpenseRowViewModel);


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
        var form_data = new FormData();


        form_data.append('expense', ko.toJSON(self));
        $.ajax({
            type: "POST",
            url: '/voucher/expense/save/',
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
                        $($("tbody.expense_row > tr")[i]).removeClass('invalid-row');
                    }
                }
            }
        });
    };

    self.id.subscribe(function (id) {
        update_url_with_id(id);
    });



}

function ExpenseRowViewModel(row) {
    var self = this;
    self.id = ko.observable();
    self.expense_id = ko.observable(1);
    self.pay_head_id = ko.observable(2);
    self.amount = ko.observable();


    for (var k in row)
        self[k] = ko.observable(row[k]);
}

