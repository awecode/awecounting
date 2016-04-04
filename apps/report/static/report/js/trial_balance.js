ko.bindingHandlers.tooltip = {
    init: function (element, valueAccessor) {
        var local = ko.utils.unwrapObservable(valueAccessor()),
            options = {};

        ko.utils.extend(options, local);

        $(element).tooltip(options);

        ko.utils.domNodeDisposal.addDisposeCallback(element, function () {
            $(element).tooltip("destroy");
        });
    }
};

var NodeModel = function (data) {

    var self = this;

    self.isExpanded = ko.observable(true);
    self.name = ko.observable();
    self.nodes = ko.observableArray([]);

    self.toggleVisibility = function () {
        self.isExpanded(!self.isExpanded());
    };


    ko.mapping.fromJS(data, self.mapOptions, self);

    self.get_style = function () {
        var padding = (self.depth() + 1) * 15;
        return {'padding-left': padding + 'px'};
    }

};

NodeModel.prototype.mapOptions = {
    nodes: {
        create: function (args) {
            return new NodeModel(args.data);
        }
    }
};


var TreeModel = function () {

    var self = this;

    self.tree_data = ko.observable();
    self.total_dr = ko.observable();
    self.total_cr = ko.observable();

    self.loadData = function (data) {
        self.tree_data(new NodeModel(data));
        self.total_dr(data.total_dr);
        self.total_cr(data.total_cr);
    };
}


$(document).ready(function () {
    vm = new TreeModel();
    vm.loadData(trial_balance_data);
    ko.applyBindings(vm);

});