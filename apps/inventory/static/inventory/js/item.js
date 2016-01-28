$(document).ready(function () {
    if (typeof(item_data) == "undefined") {
        item = new ItemVM();
    } else {
        item = new ItemVM(item_data, item_unit_id);
    }
    var item_form = document.getElementById("other-properties");
    ko.applyBindings(item, item_form);
    $('.change-on-ready').trigger('change');
    $("table tr #item_instance_properties").each(function (i) {
        value = $(this).text().slice(1, -1);
        $(this).html(value);
    });


    if ($('.selectize').length) {
        var $select = $('.selectize').selectize();
        $($select).each(function () {
            init_selectize(this.selectize);
            selectize_validation_fix(this.selectize);
        });
    }


});

function ItemVM(data, unit_id) {
    var self = this;
    self.other_properties = ko.observableArray([]);
    //if (unit_id) {
    //    self.unit_id = ko.observable(unit_id)
    //} else {
    //    self.unit_id = ko.observable();
    //};

    if (data != null) {
        for (var item_property in data) {
            var property_name = item_property
            var property = data[item_property]
            self.other_properties.push(new OtherPropertiesVM().property_name(property_name).property(property))
        }
    } else {
        self.other_properties.push(new OtherPropertiesVM())
    }

    self.addOtherProperty = function () {
        self.other_properties.push(new OtherPropertiesVM());
        $('#id_other_properties div.property-row:last input:first').focus();
    };

    self.removeOtherProperty = function (property) {
        self.other_properties.remove(property);
    };

}

function OtherPropertiesVM() {
    var self = this;
    self.property_name = ko.observable();
    self.property = ko.observable();
}
