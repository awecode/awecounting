$(document).ready(function () {
    vm = new JournalVoucherViewModel(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});

function JournalVoucherViewModel(data) {
    var self = this;

    self.id = ko.observable();
    self.voucher_no = ko.observable();
    self.date = ko.observable();
    self.narration = ko.observable();
    self.status = ko.observable();

    //$.ajax({
    //    url: '/ledger/api/account.json',
    //    dataType: 'json',
    //    async: false,
    //    success: function (data) {
    //        self.accounts = ko.observableArray(data);
    //    }
    //});

    self.accounts = ko.observableArray(data.accounts);

    self.table_view = new TableViewModel({rows: data.rows}, JournalVoucherRowViewModel);

    for (var k in data)
        self[k] = ko.observable(data[k]);

    self.total_dr_amount = ko.computed(function () {
        total = 0;
        for (o in self.table_view.rows()) {
            if (self.table_view.rows()[o].dr_amount()) {
                total += parseInt(self.table_view.rows()[o].dr_amount());
            }
            ;
        }
        return total;
    });

    self.total_cr_amount = ko.computed(function () {
        total = 0;
        for (o in self.table_view.rows()) {
            if (self.table_view.rows()[o].cr_amount()) {
                total += parseInt(self.table_view.rows()[o].cr_amount());
            }
            ;
        }
        return total;
    });

    self.id.subscribe(function (id) {
        update_url_with_id(id);
    });

    self.check_description = function () {
        arr = [];
        for (i in self.table_view.rows()) {
            arr.push(self.table_view.rows()[i].description());
        }
        if ($.inArray("", arr) >= 0 || $.inArray(undefined, arr) >= 0)
            return true
        return false
    }

    self.add_row = function (element, viewModel) {
        $(element).blur();
        var type;
        var dr_amount;
        var cr_amount;
        var diff = self.total_dr_amount() - self.total_cr_amount();
        if (diff > 0) {
            type = 'Cr';
            dr_amount = 0;
            cr_amount = diff;
        } else {
            type = 'Dr';
            cr_amount = 0;
            dr_amount = (-1) * diff;
        }

        if ($(element).closest("tr").is(":nth-last-child(2)") && self.total_dr_amount() != self.total_cr_amount())
            self.table_view.rows.push(new JournalVoucherRowViewModel({type: type, cr_amount: cr_amount, dr_amount: dr_amount}));

        //focus on account selectize of next row
        $(element).closest('tr').next('tr').find('td.account .selectize-control input').click();
    }

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
            url: '/voucher/journal/save/',
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
                    $("tbody > tr").each(function (i) {
                        $($("tbody > tr:not(.total)")[i]).addClass('invalid-row');
                    });
                    for (var i in msg.rows) {
                        self.table_view.rows()[i].id = msg.rows[i];
                        $($("tbody > tr")[i]).removeClass('invalid-row');
                    }
                }
            }
        });
    }

}

function JournalVoucherRowViewModel(row) {
    var self = this;

    self.account_type = ko.observableArray(['Dr', 'Cr']);
    self.id = ko.observable();
    self.type = ko.observable();
    self.description = ko.observable();
    self.cr_amount = ko.observable();
    self.dr_amount = ko.observable();
    self.account = ko.observable();

    for (var k in row)
        self[k] = ko.observable(row[k]);

    self.is_dr = ko.computed(function () {
        if (self.type() == "Dr")
            return true
        return false
    });

    self.is_cr = ko.computed(function () {
        if (self.type() == "Cr")
            return true
        return false
    });

    self.type.subscribe(function (type) {
        self.dr_amount(0);
        self.cr_amount(0);
    });
}