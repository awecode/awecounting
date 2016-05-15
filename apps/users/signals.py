from django.dispatch import Signal

company_creation = Signal(providing_args=["company"])
# branch_creation = Signal(providing_args=["name", "company"])
