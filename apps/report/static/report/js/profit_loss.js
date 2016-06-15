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

    self.net_dr = function () {
        return parseFloat(self.dr()) - parseFloat(self.cr());
    };

    self.net_cr = function () {
        return parseFloat(self.cr()) - parseFloat(self.dr());
    }

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
        income_node
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
    self.income_node = ko.observable();
    self.indirect_income_node = ko.observable();
    self.expense_node = ko.observable();
    self.indirect_expense_node = ko.observable();

    self.load_data = function (data) {
        self.settings = ko.mapping.fromJS(data.settings);
        self.settings_save_url = data.settings_save_url;
        self.tree_data(new NodeModel(data, self.settings));
        self.total_dr(data.total_dr);
        self.total_cr(data.total_cr);
        self.income_node(get_by_name(self.tree_data().nodes(), 'Income'));

        if (self.income_node()) {
            self.income_node()['balance'] = 'cr';
            self.indirect_income_node(get_by_name(self.income_node().nodes(), 'Indirect Income'));
            self.indirect_income_node()['balance'] = 'cr';
            self.income_node().nodes.remove(self.indirect_income_node())
        }

        self.expense_node(get_by_name(self.tree_data().nodes(), 'Expenses'));

        if (self.expense_node()) {
            self.expense_node()['balance'] = 'dr';
            self.indirect_expense_node(get_by_name(self.expense_node().nodes(), 'Indirect Expenses'));
            self.indirect_expense_node()['balance'] = 'dr';
            self.expense_node().nodes.remove(self.indirect_expense_node())
        }
    };

    self.gross_profit = ko.computed(function () {
        var gross = 0;
        if (self.income_node() && self.income_node().nodes()) {
            ko.utils.arrayForEach(self.income_node().nodes(), function (node) {
                gross += node.net_cr();
            });
        }
        if (self.expense_node() && self.expense_node().nodes()) {
            ko.utils.arrayForEach(self.expense_node().nodes(), function (node) {
                gross -= node.net_dr();
            });
        }
        return gross;
    });

    self.net_profit = ko.computed(function () {
        var net = self.gross_profit();
        if (self.indirect_income_node() && self.indirect_income_node().nodes()) {
            ko.utils.arrayForEach(self.indirect_income_node().nodes(), function (node) {
                net += node.net_cr();
            });
        }
        if (self.indirect_expense_node() && self.indirect_expense_node().nodes()) {
            ko.utils.arrayForEach(self.indirect_expense_node().nodes(), function (node) {
                net -= node.net_dr();
            });
        }
        return net;
    });

    self.save_settings = function () {
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
