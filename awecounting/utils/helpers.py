from django.http import JsonResponse

def save_model(model, values):
    for key, value in values.items():
        setattr(model, key, value)
    model.save()
    return model

def invalid(row, required_fields):
    invalid_attrs = []
    for attr in required_fields:
        # if one of the required attributes isn't received or is an empty string
        if not attr in row or row.get(attr) == "":
            invalid_attrs.append(attr)
    if len(invalid_attrs) is 0:
        return False
    return invalid_attrs

def empty_to_none(o):
    if o == '':
        return None
    return o

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

def get_next_voucher_no(cls, attr):
    from django.db.models import Max

    max_voucher_no = cls.objects.all().aggregate(Max(attr))[attr + '__max']
    if max_voucher_no:
        return max_voucher_no + 1
    else:
        return 1

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


def get_next_voucher_no(cls, company_id=None, attr='voucher_no'):
    from django.db.models import Max

    qs = cls.objects.all()
    if company_id:
        qs = qs.filter(company_id=company_id)
    max_voucher_no = qs.aggregate(Max(attr))[attr + '__max']
    if max_voucher_no:
        return max_voucher_no + 1
    else:
        return 1


def delete_rows(rows, model):
    for row in rows:
        if row.get('id'):
            instance = model.objects.get(id=row.get('id'))
            # TODO is journalentry deleted on row deletion?
            # JournalEntry.objects.get(content_type=ContentType.objects.get_for_model(model),
            #                         model_id=instance.id).delete()
            instance.delete()


def save_model(model, values):
    for key, value in values.items():
        setattr(model, key, value)
    model.clean()
    model.save()
    return model

def invalid(row, required_fields):
    invalid_attrs = []
    for attr in required_fields:
        # if one of the required attributes isn't received or is an empty string
        if not attr in row or row.get(attr) == "":
            invalid_attrs.append(attr)
    if len(invalid_attrs) is 0:
        return False
    return invalid_attrs
