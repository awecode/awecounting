from django.db import models

class JournalVoucher(models.Model):
    #voucher_no = models.CharField(max_length=10)
    voucher_no = models.IntegerField()
    date = models.DateField()
    company = models.ForeignKey(Company)
    narration = models.TextField()
    statuses = [('Cancelled', 'Cancelled'), ('Approved', 'Approved'), ('Unapproved', 'Unapproved')]
    status = models.CharField(max_length=10, choices=statuses, default='Unapproved')

    def get_voucher_no(self):
        return self.voucher_no

    def __init__(self, *args, **kwargs):
        super(JournalVoucher, self).__init__(*args, **kwargs)
        if not self.pk and not self.voucher_no:
            self.voucher_no = get_next_voucher_no(JournalVoucher, self.company)


class JournalVoucherRow(models.Model):
    types = [('Dr', 'Dr'), ('Cr', 'Dr')]
    type = models.CharField(choices=types, default='Dr', max_length=2)
    account = models.ForeignKey(Account, related_name='account_rows')
    description = models.TextField()
    dr_amount = models.FloatField(null=True, blank=True)
    cr_amount = models.FloatField(null=True, blank=True)
    journal_voucher = models.ForeignKey(JournalVoucher, related_name='rows')

    def get_absolute_url(self):
        return '/voucher/journal/' + str(self.journal_voucher_id)

    def get_voucher_no(self):
        return self.journal_voucher.voucher_no

# Create your models here.
