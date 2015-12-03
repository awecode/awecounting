def get_next_voucher_no(cls, company):
    from django.db.models import Max
    setting = company.voucher_settings
    #import pdb
    #pdb.set_trace()
    start_date = setting.voucher_number_start_date
    restart_years = setting.voucher_number_restart_years
    restart_months = setting.voucher_number_restart_months
    restart_days = setting.voucher_number_restart_days
    end_date = date(start_date.year + restart_years, start_date.month + restart_months, start_date.day + restart_days )