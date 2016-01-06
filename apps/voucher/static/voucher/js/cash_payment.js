$(document).ready(function () {
    vm = new CashPaymentVM(ko_data);
    ko.applyBindings(vm);
});


function CashPaymentVM(data) {
    var self = this;

    $.ajax({
        url: '/ledger/api/parties_with_balance.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.parties = data;
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
        self.current_balance(-1 * party.balance);
    });


//    self.party_changed = function (vm) {
//        var selected_obj = $.grep(self.parties, function (i) {
//            return i.id == self.party();
//        })[0];
//        self.party_address(selected_obj.address);
//        self.current_balance(selected_obj.customer_balance);
////        if (self.table_vm()){
////            self.table_vm().rows(null);
////        }
//    }

    //self.party.subscribe(self.party_changed);

    self.load_related_invoices = function () {
        if (self.party()) {
            var payment_id = self.id() || 0;
            $.ajax({

                url: '/voucher/api/purchase/' + self.party_id() + '/' + payment_id + '.json',
                dataType: 'json',
                async: false,
                success: function (data) {
                    if (data.length) {
                        self.invoices = data;
                        for (k in self.rows()) {
                            var row = self.rows()[k];
                            $.each(self.invoices, function (i, o) {
                                if (o.id == row.invoice) {
                                    o.payment = row.payment;
                                    // o.discount = row.discount;
                                }
                            });
                        }
                        var options = {
                            rows: self.invoices
                        };
                        self.table_vm(new TableViewModel(options, CashPaymentRowVM));
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

    self.validate = function () {
        if (!self.party()) {
            bsalert.error('"Party" field is required!')
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
                url: '/voucher/cash_payment/save/',
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


    // self.approve = function (item, event) {
    //     if (!self.validate())
    //         return false;
    //     if (get_form(event).checkValidity()) {
    //         $.ajax({
    //             type: "POST",
    //             url: '/voucher/cash_payment/approve/',
    //             data: ko.toJSON(self),
    //             success: function (msg) {
    //                 if (typeof (msg.error_message) != 'undefined') {
    //                     bs_alert.error(msg.error_message);
    //                     self.state('error');
    //                 }
    //                 else {
    //                     bsalert.success('Approved!');
    //                     self.status('Approved');
    //                     self.state('success');
    //                     if (msg.id)
    //                         self.id(msg.id);
    //                 }
    //             }
    //         });
    //     }
    //     else
    //         return true;
    // }

    if (self.rows().length) {
        setTimeout(self.load_related_invoices, 500);
    }
}


function CashPaymentRowVM(row) {
    var self = this;

    self.payment = ko.observable();
    self.discount = ko.observable();

    for (var k in row) {
        self[k] = ko.observable(row[k]);
    }

    self.overdue_days = function () {
        if (self.due_date()) {
            var diff = days_between(new Date(self.due_date()), new Date());
            if (diff >= 0)
                return diff;
        }
        return '';
    }

}