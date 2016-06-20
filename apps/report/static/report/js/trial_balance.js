var NodeModel = function (data, settings) {
    var self = this;

    self.settings = settings;
    self.isExpanded = ko.observable(true);
    self.name = ko.observable();
    self.nodes = ko.observableArray([]);
    self.type = ko.observable();
    self.depth = ko.observable();

    self.mapOptions = {
        nodes: {
            create: function (args) {
                return new NodeModel(args.data, settings);
            }
        }
    };

    ko.mapping.fromJS(data, self.mapOptions, self);

    self.get_style = ko.computed(function () {
        var padding;
        if (self.type() == 'Account' && self.settings.show_ledgers_only()) {
            padding = 0;
        } else {
            padding = (self.depth() + 1) * 15;
        }
        return {'padding-left': padding + 'px'};
    });

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
        if (self.depth() > 0 && self.settings.show_root_categories_only()) {
            return false;
        }
        //if (self.type() == 'Account' && self.settings.hide_all_ledgers()) {
        //    return false;
        //}

        if (self.type() == 'Category' && !self.settings.show_zero_balance_categories() && self.dr() == 0 && self.cr() == 0) {
            return false;
        }
        if (self.type() == 'Account' && !self.settings.show_zero_balance_ledgers() && self.dr() == 0 && self.cr() == 0) {
            return false;
        }

        return true;

    }

    self.is_row_visible = function () {
        if (self.type() == 'Category' && self.settings.show_ledgers_only()) {
            return false;
        }
        return true;
    }
};

var TreeModel = function () {

    var self = this;

    self.tree_data = ko.observable();
    self.total_dr = ko.observable();
    self.total_cr = ko.observable();

    self.load_data = function (data) {
        console.log(data);
        self.settings = ko.mapping.fromJS(data.settings);
        self.model = data.model;
        self.settings_save_url = data.settings_save_url;
        self.tree_data(new NodeModel(data, self.settings));
        self.total_dr(data.total_dr);
        self.total_cr(data.total_cr);
    };

    self.save_settings = function () {
        self.settings['model'] = data.model;
        ajax_save(self.settings_save_url, ko.toJSON(self.settings));
        $('.dropdown.mega-dropdown.open .dropdown-toggle').dropdown('toggle');
    }
}


$(function () {
    vm = new TreeModel();
    vm.load_data(trial_balance_data);
    ko.applyBindings(vm);

    $('.dropdown-menu.mega-dropdown-menu').click(function (e) {
        e.stopPropagation();
    });
});
