$(document).ready(function () {
    vm = new InventoryAccountVM(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});

function InventoryAccountVM(data) {

    var self = this;
    arr = []

    for ( d in data ) {
      var value = data[d].income_quantity;
      for ( var i=0 ; i< value ; i++){
        arr.push(data[d].income_rate)
        }

    }

    self.table_vm = new TableViewModel({rows: data, auto_add_first: false}, InventoryAccountRow);

    self.save = function (item, event) {
        $.ajax({
            type: "POST",
            url: '/inventory/save/account/',
            data: ko.toJSON(self),
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    alert.error(msg.error_message);
                }
                else {
                    alert.success('Saved!');
                }
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                alert.error(textStatus);
            }
        });
    }

}

function InventoryAccountRow(data){
    var self = this;
    self.expense_rate = ko.observable()
    
    // counts = {}
    // for (var i = 0; i < arr.length; i++) {
    // counts[arr[i]] = 1 + (counts[arr[i]] || 0);
    // }

    self.e1 = ko.observable()
    self.e2 = ko.observable()
    self.r1 = ko.observable()
    self.r2 = ko.observable()
    self.expense_flag = ko.observable(false)

    for (var i in data){
        self[i] = ko.observable(data[i]);
    }

    self.income_total = ko.computed(function() {
        if ( self.income_quantity() ) {
            return self.income_quantity() * self.income_rate()
        } else {
            return ''
        }
    });

    if ( self.expense_quantity() ) {
        var arry = arr
        var count = 0
        for ( var i = 0; i < self.expense_quantity(); i++ ) {
            if (arry[0] != arry[1]) {
                expense_second_value = 0
                if ((count+1) != self.expense_quantity()){
                    var diff = self.expense_quantity() - (count+1)
                    self.e1(count+1)
                    self.r1(arry[0])
                    expense_first_value = count + 1
                    for ( var i = 0; i < diff ; i++ ){
                        self.r2(arry.shift())
                        self.e2(diff)
                        expense_second_value++
                        if ( (i+1) == diff ) {
                            break;
                        }
                    }
                    if (expense_first_value + expense_second_value == self.expense_quantity()) {
                        arry.shift()
                        self.expense_flag(true)
                        count=0
                        break;
                    };
                }
            }
            if( typeof(expense_first_value) != 'undefined' && typeof(expense_second_value) != 'undefined') {
                delete expense_first_value
                delete expense_second_value 
            }
            self.expense_rate(arry.shift())
            count++;
        }    
    }

    self.expense_total = ko.computed(function() {
        if ( self.expense_quantity() ) {
            if (self.expense_flag()) {
                return (self.e1() * self.r1()) + (self.e2() * self.r2())
            } else {
                return self.expense_quantity() * self.expense_rate()
            };
        } else {
            return ''
        }
    });

}