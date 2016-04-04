var NodeModel = function (data, settings) {
    var self = this;

    self.settings = settings;
    self.isExpanded = ko.observable(true);
    self.name = ko.observable();
    self.nodes = ko.observableArray([]);

    self.mapOptions = {
        nodes: {
            create: function (args) {

                return new NodeModel(args.data, settings);
            }
        }
    };

    ko.mapping.fromJS(data, self.mapOptions, self);

    self.get_style = function () {
        var padding = (self.depth() + 1) * 15;
        return {'padding-left': padding + 'px'};
    }

    self.toggleVisibility = function () {
        if (self.url()) {
            return true;
        } else {
            self.isExpanded(!self.isExpanded());
        }
    };

    self.get_url = function () {
        if (self.url()) {
            return self.url();
        } else {
            return 'javascript: void()';
        }
    }

    self.is_visible = function () {
        return true;
    }

};

//NodeModel.prototype.mapOptions = {
//    nodes: {
//        create: function (args) {
//            return new NodeModel(args.data);
//        }
//    }
//};

var Setting = function (settings) {
    var self = this;
    self.show_root_categories_only = ko.observable(settings.show_root_categories_only);
    //ko.mapping.fromJS(settings, self);
}


var TreeModel = function () {

    var self = this;

    self.tree_data = ko.observable();
    self.total_dr = ko.observable();
    self.total_cr = ko.observable();

    self.loadData = function (data) {
        self.settings = new Setting(data.settings);
        console.log(self.settings);
        self.tree_data(new NodeModel(data, self.settings));
        self.total_dr(data.total_dr);
        self.total_cr(data.total_cr);
    };
}


$(function () {
    vm = new TreeModel();
    vm.loadData(trial_balance_data);
    ko.applyBindings(vm);
    $('li.dropdown.mega-dropdown a').on('click', function (event) {
        $(this).parent().toggleClass("open");
    });

    $('body').on('click', function (e) {
        if (!$('li.dropdown.mega-dropdown').is(e.target) && $('li.dropdown.mega-dropdown').has(e.target).length === 0 && $('.open').has(e.target).length === 0) {
            $('li.dropdown.mega-dropdown').removeClass('open');
        }
    });

});
