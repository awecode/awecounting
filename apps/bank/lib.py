def get_next_voucher_no(cls, company):
    from django.db.models import Max
    setting = company.voucher_settings
    start_date = setting.voucher_number_start_date
    restart_years = setting.voucher_number_restart_years
    restart_months = setting.voucher_number_restart_months
    restart_days = setting.voucher_number_restart_days
    end_date = date(start_date.year + restart_years, start_date.month + restart_months, start_date.day + restart_days )


def invalid(row, required_fields):
    invalid_attrs = []
    for attr in required_fields:
        # if one of the required attributes isn't received or is an empty string
        if not attr in row or row.get(attr) == "":
            invalid_attrs.append(attr)
    if len(invalid_attrs) is 0:
        return False
    return invalid_attrs


def save_model(model, values):
    for key, value in values.items():
        setattr(model, key, value)
    model.save()
    return model
