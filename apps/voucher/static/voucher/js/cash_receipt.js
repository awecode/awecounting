$(document).ready(function () {
    vm = new CashReceiptVM(ko_data);
    ko.applyBindings(vm);
});


function CashReceiptVM(data) {
    var self = this;

    $.ajax({
        url: '/ledger/api/parties_with_balance.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.parties = ko.observableArray(data);
        }
    });

    self.id = ko.observable('');
    self.message = ko.observable();
    self.state = ko.observable('standby');
    self.party_id = ko.observable();
    self.party = ko.observable();
    self.date = ko.observable();
    self.party_address = ko.observable();
    self.reference = ko.observable();
    self.current_balance = ko.observable();
    self.amount = ko.observable();
    self.voucher_no = ko.observable();
    self.rows = ko.observableArray();
    self.table_vm = ko.observable({
        'rows': function () {
        }, 'get_total': function () {
        }
    });

    for (var k in data) {
        self[k] = ko.observable(data[k]);
    }

    self.party.subscribe(function (party) {
        self.party_address(party.address);
        self.current_balance(party.balance);
    });

    self.load_related_invoices = function () {
        if (self.party()) {
            var receipt_id = self.id() || 0;
            $.ajax({

                url: '/voucher/api/sale/' + self.party_id() + '/' + receipt_id + '.json',
                dataType: 'json',
                async: false,
                success: function (data) {
                    if (data.length) {
                        self.invoices = data;
                        for (k in self.rows()) {
                            var row = self.rows()[k];
                            $.each(self.invoices, function (i, o) {
                                if (o.id == row.invoice) {
                                    o.payment = row.receipt;
                                    //o.discount = row.discount;
                                }
                            });
                        }
                        var options = {
                            rows: self.invoices
                        };
                        self.table_vm(new TableViewModel(options, CashReceiptRowVM));
                        bsalert.success('Invoices loaded!');
                        self.state('success');
                    }
                    else {
                        bsalert.info('No pending invoices found for the customer!');
                        self.state('error');
                    }
                }
            });
        }
    }


    self.total_payment = ko.computed(function () {
        return self.table_vm().get_total('payment');
    }, self);

    self.total_discount = ko.computed(function () {
        return self.table_vm().get_total('discount');
    }, self);

    self.row_total_amount = function () {
        var sum = 0;
        if (typeof(self.table_vm().rows()) != 'undefined') {
            self.table_vm().rows().forEach(function (i) {
                if (i.total_amount()) {
                    sum += parseFloat(i.total_amount());
                }
            });
            return round2(sum);

        }
    }

    self.row_pending_amount = function () {
        var sum = 0;
        if (typeof(self.table_vm().rows()) != 'undefined') {
            self.table_vm().rows().forEach(function (i) {
                if (i.pending_amount()) {
                    sum += parseFloat(i.pending_amount());
                }
            });
            return round2(sum);

        }
    }

    self.validate = function () {
        if (!self.party()) {
            bsalert.error('"Party" field is required!');
            self.state('error');
            return false;
        }
        return true;
    }

    self.save = function (item, event) {
        if (!self.validate())
            return false;
        if (get_form(event).checkValidity()) {
            if ($(get_target(event)).data('continue')) {
                self.continue = true;
            }
            var data = ko.toJSON(self);
            $.ajax({
                type: "POST",
                url: '/voucher/cash-receipt/save/',
                data: data,
                success: function (msg) {
                    if (typeof (msg.error_message) != 'undefined') {
                        bsalert.error(msg.error_message);
                    }
                    else {
                        bsalert.success('Saved!');
                        if (msg.id) {
                            if (!self.id())
                                update_url_with_id(msg.id);
                            self.id(msg.id);
                        }
                        if (msg.redirect_to) {
                            window.location = msg.redirect_to;
                        }
                    }
                }
            });
        }
        else
            return true;
    }


    self.approve = function (item, event) {
        if (!self.validate())
            return false;
        if (get_form(event).checkValidity()) {
            $.ajax({
                type: "POST",
                url: '/voucher/cash-receipt/approve/',
                data: ko.toJSON(self),
                success: function (msg) {
                    if (typeof (msg.error_message) != 'undefined') {
                        bs_alert.error(msg.error_message);
                        self.state('error');
                    }
                    else {
                        bsalert.success('Approved!');
                        self.status('Approved');
                        self.state('success');
                        if (msg.id)
                            self.id(msg.id);
                    }
                }
            });
        }
        else
            return true;
    }

    if (self.rows().length) {
        setTimeout(self.load_related_invoices, 500);
    }
}


function CashReceiptRowVM(row) {
    var self = this;

    self.payment = ko.observable();
    self.discount = ko.observable();

    for (var k in row) {
        self[k] = ko.observable(row[k]);
    }

    self.actual_pending_amount = self.pending_amount()

    self.payment.subscribe(function () {
        if (typeof(self.payment()) == 'undefined' || self.payment() == '') {
            self.pending_amount(self.actual_pending_amount);
        } else {
            self.pending_amount(self.actual_pending_amount - self.payment())
        }
        ;
    });

    self.overdue_days = function () {
        if (self.due_date()) {
            var diff = days_between(new Date(self.due_date()), new Date());
            if (diff >= 0)
                return diff;
        }
        return '';
    }

}