from django.contrib import admin
from .models import Faq


class FaqAdmin(admin.ModelAdmin):
    list_display = ['id', 'question']


admin.site.register(Faq, FaqAdmin)
