from django.contrib import admin

from subscribes.models import Subscribe

from .models import Account

admin.site.register(Account, admin.ModelAdmin)
admin.site.register(Subscribe, admin.ModelAdmin)
