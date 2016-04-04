$(document).ready(function () {
    vm = new TreeModel(trial_balance_data);
    ko.applyBindings(vm);
});

function TreeModel(data) {
    var self = this;
    self.nodes = ko.mapping.fromJS(data);
    console.log(data);
}