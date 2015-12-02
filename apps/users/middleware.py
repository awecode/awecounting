from apps.users.models import Role
from apps.users.models import Company


class RoleMiddleware(object):
    def process_request(self, request):
        if not request.user.is_anonymous():
            roles = Role.objects.filter(user=request.user)
            if not request.session.get('company') and len(roles):
                request.session['company'] = roles[0].company.id
            if len(roles):
                request.__class__.company = Company.objects.get(id=request.session['company'])
                request.__class__.roles = Role.objects.filter(user=request.user, company = request.session['company'])
                #request.__class__.role = Role.objects.get(user=request.user, company = request.session['company'])
                groups = []
                for role in request.roles:
                    groups.append(role.group)
                request.__class__.groups = groups
            else:
                request.__class__.groups = []
                request.__class__.roles = []
                request.__class__.company = None
                #request.__class__.role = None
