from apps.users.models import Role
from apps.users.models import Company
from rest_framework.authtoken.models import Token


def clear_roles(request):
    request.__class__.role = None
    request.__class__.company = None
    request.__class__.group = None
    request.__class__.roles = []
    request.__class__.is_owner = False
    # request.__class__.groups = []
    return request


class RoleMiddleware(object):
    def process_request(self, request):
        role = None

        if request.META.get('HTTP_AUTHORIZATION'):
            token_key = request.META.get('HTTP_AUTHORIZATION').split(' ')[-1]
            request.user = Token.objects.get(key=token_key).user

        if not request.user.is_anonymous():

            if request.session.get('role'):
                try:
                    role = Role.objects.select_related('group', 'company').get(pk=request.session.get('role'), user=request.user)
                except Role.DoesNotExist:
                    pass

            if not role:
                roles = Role.objects.filter(user=request.user).select_related('group', 'company')
                if roles:
                    role = roles[0]
                    request.session['role'] = role.id
            if role:
                request.__class__.role = role
                request.__class__.company = role.company
                request.__class__.group = role.group
                request.__class__.roles = Role.objects.filter(user=request.user, company=role.company)
                request.__class__.is_owner = request.group.name in ('Owner', 'SuperOwner')
                #     for role in request.roles:
                #         groups.append(role.group)
                #     request.__class__.groups = groups
            else:
                request = clear_roles(request)
        else:
            request = clear_roles(request)

    def authenticate(self, request):
        pass
