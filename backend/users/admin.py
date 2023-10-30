from django.contrib import admin

from .models import Account
from subscribes.models import Subscribe

admin.site.register(Account, admin.ModelAdmin)
admin.site.register(Subscribe, admin.ModelAdmin)
