$(document).ready(function () {
    vm = new InventoryAccountVM(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});

function InventoryAccountVM(data) {

    var self = this;

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

    for (var i in data){
        self[i] = ko.observable(data[i]);
    }

    self.remaining_quantity= function(){
        return 12;
    }

}