from django import template

register = template.Library()

from apps.inventory.templatetags.filters import *


def _setup_macros_dict(parser):
    ## Metadata of each macro are stored in a new attribute
    ## of 'parser' class. That way we can access it later
    ## in the template when procesifsing 'usemacro' tags.
    try:
        ## Only try to access it to eventually trigger an exception
        parser._macros
    except AttributeError:
        parser._macros = {}


class DefineMacroNode(template.Node):
    def __init__(self, name, nodelist, args):

        self.name = name
        self.nodelist = nodelist
        self.args = []
        self.kwargs = {}
        for a in args:
            if "=" not in a:
                self.args.append(a)
            else:
                name, value = a.split("=")
                self.kwargs[name] = value

    def render(self, context):
        ## empty string - {% macro %} tag does no output
        return ''


# @register.simple_tag(takes_context=True)
# def get_related_party(context, accessible_company):
#     request = context['request']
#     related_party = request.company.parties.filter(related_company=accessible_company)
#     return related_party

@register.tag(name="kwacro")
def do_macro(parser, token):
    try:
        args = token.split_contents()
        tag_name, macro_name, args = args[0], args[1], args[2:]
    except IndexError:
        m = ("'%s' tag requires at least one argument (macro name)"
             % token.contents.split()[0])
        raise template.TemplateSyntaxError(m)
    # TODO: could do some validations here,
    # for now, "blow your head clean off"
    nodelist = parser.parse(('endkwacro',))
    parser.delete_first_token()

    ## Metadata of each macro are stored in a new attribute
    ## of 'parser' class. That way we can access it later
    ## in the template when processing 'usemacro' tags.
    _setup_macros_dict(parser)
    parser._macros[macro_name] = DefineMacroNode(macro_name, nodelist, args)
    return parser._macros[macro_name]


class LoadMacrosNode(template.Node):
    def render(self, context):
        ## empty string - {% loadmacros %} tag does no output
        return ''


@register.tag(name="loadkwacros")
def do_loadmacros(parser, token):
    try:
        tag_name, filename = token.split_contents()
    except IndexError:
        m = ("'%s' tag requires at least one argument (macro name)"
             % token.contents.split()[0])
        raise template.TemplateSyntaxError(m)
    if filename[0] in ('"', "'") and filename[-1] == filename[0]:
        filename = filename[1:-1]
    t = get_template(filename)
    macros = t.nodelist.get_nodes_by_type(DefineMacroNode)
    ## Metadata of each macro are stored in a new attribute
    ## of 'parser' class. That way we can access it later
    ## in the template when processing 'usemacro' tags.
    _setup_macros_dict(parser)
    for macro in macros:
        parser._macros[macro.name] = macro
    return LoadMacrosNode()


class UseMacroNode(template.Node):
    def __init__(self, macro, fe_args, fe_kwargs):
        self.macro = macro
        self.fe_args = fe_args
        self.fe_kwargs = fe_kwargs

    def render(self, context):

        for i, arg in enumerate(self.macro.args):
            try:
                fe = self.fe_args[i]
                context[arg] = fe.resolve(context)
            except IndexError:
                context[arg] = ""

        for name, default in iter(self.macro.kwargs.items()):
            if name in self.fe_kwargs:
                context[name] = self.fe_kwargs[name].resolve(context)
            else:
                context[name] = FilterExpression(default,
                                                 self.macro.parser
                                                 ).resolve(context)

        return self.macro.nodelist.render(context)


@register.tag(name="usekwacro")
def do_usemacro(parser, token):
    try:
        args = token.split_contents()
        tag_name, macro_name, values = args[0], args[1], args[2:]
    except IndexError:
        m = ("'%s' tag requires at least one argument (macro name)"
             % token.contents.split()[0])
        raise template.TemplateSyntaxError(m)
    try:
        macro = parser._macros[macro_name]
    except (AttributeError, KeyError):
        m = "Macro '%s' is not defined" % macro_name
        raise template.TemplateSyntaxError(m)

    fe_kwargs = {}
    fe_args = []

    for val in values:
        if "=" in val:
            # kwarg
            name, value = val.split("=")
            fe_kwargs[name] = FilterExpression(value, parser)
        else:  # arg
            # no validation, go for it ...
            fe_args.append(FilterExpression(val, parser))

    macro.parser = parser
    return UseMacroNode(macro, fe_args, fe_kwargs)


@register.filter
def format_search_string(string):
    string = string.replace('/', '')
    return string.strip()


@register.filter
def fy(year):
    return str(year) + '-' + str(year + 1)[-2:]


@register.simple_tag(takes_context=True)
def print_view(context, string):
    request = context['request']
    if not getattr(request.company.settings, string):
        return 'hidden-print'
    return ''


@register.assignment_tag
def issuperuser(user):
    return 'SuperOwner' not in user.roles.all().values_list('group__name', flat=True)

#
# @register.simple_tag(takes_context=True)
# def issuperowner(context, user_id):
#     request = context['request']
#     import ipdb
#     ipdb.set_trace()
#     _bool = False
#     if request.session.role:
#         group = Group.objects.get(pk=request.session.role)
#         if group.name == 'SuperOwner':
#             _bool = True
#     return _bool

#
# @register.simple_tag(takes_context=True)
# def colspan(context):
#     request = context['request']
#     if context['obj'].__class__.__name__ == 'PurchaseVoucher':
#         colspan = 4
#         attr_list = ['show_purchase_voucher_sn', 'show_purchase_voucher_code', 'show_purchase_voucher_oem_number',
#                  'show_purchase_voucher_discount', 'show_purchase_voucher_tax_scheme']
#         if request.company.settings.show_lot:
#             colspan += 1
#
#     if context['obj'].__class__.__name__ == 'Sale':
#         colspan = 4
#         attr_list = ['show_sale_voucher_sn', 'show_sale_voucher_code', 'show_sale_voucher_oem_number',
#                  'show_sale_voucher_discount', 'show_sale_voucher_tax_scheme']
#
#     if request.company.settings.show_locations:
#         colspan += 1
#
#     for field in request.company.settings._meta.get_fields():
#         if field.name in attr_list:
#             if getattr(request.company.settings, field.name):
#                 colspan = colspan + 1
#
#     return colspan
