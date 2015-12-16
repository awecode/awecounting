from django.http import JsonResponse


def zero_for_none(obj):
    if obj is None:
        return 0
    else:
        return obj


def none_for_zero(obj):
    if not obj:
        return None
    else:
        return obj


def json_from_object(obj):
    data = {
        'id': obj.id
    }
    if hasattr(obj, 'name'):
        data['name'] = obj.name
    elif hasattr(obj, 'title'):
        data['name'] = obj.title
    else:
        data['name'] = str(obj)
    return JsonResponse(data)
