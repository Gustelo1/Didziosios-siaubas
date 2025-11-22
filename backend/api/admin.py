from django.contrib import admin

from api.models import Expense, Contribution

# Register your models here.
admin.site.register(Expense)
admin.site.register(Contribution)
