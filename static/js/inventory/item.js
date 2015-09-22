$(document).ready(function () {
    if (typeof(item_data) == "undefined") {
        vm = new ItemVM();
    } else {
        vm = new ItemVM(item_data, item_unit_id);
    }
    var item_form = document.getElementById("other-properties");
    ko.applyBindings(vm, item_form);
    $('.change-on-ready').trigger('change');
    $("table tr #item_instance_properties").each(function(i) {
        value = $(this).text().slice(1,-1);
        $(this).html(value);
    });
    
});

function ItemVM(data, unit_id) {
    var self = this;
    self.other_properties = ko.observableArray([]);
    if (unit_id) {
        self.unit_id = ko.observable(unit_id)
    } else {
        self.unit_id = ko.observable();
    };
    
    if (data != null) {
        for (item_property in data) {
            var property_name = item_property
            var property = data[item_property]
            self.other_properties.push(new OtherPropertiesVM().property_name(property_name).property(property))
        }
    } else {
        self.other_properties.push(new OtherPropertiesVM())
    }
    
    self.addOtherProperty = function () {
            self.other_properties.push(new OtherPropertiesVM());
        };

    self.removeOtherProperty = function(property){
        self.other_properties.remove(property);
    };

    $.ajax({
        url: '/inventory/api/units.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.units = ko.observableArray(data);
        }
    });

    self.unit_changed = function (row) {
        var selected_item = $.grep(self.units(), function (i) {
            return i.id == self.unit_id();
        })[0];
        if (!selected_item) return;
    }

}

function OtherPropertiesVM() {
    var self = this;
    self.property_name = ko.observable();
    self.property = ko.observable();
}
