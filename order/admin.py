from django.contrib import admin
from .models import Order, OrderItem


class OrderInline(admin.TabularInline):
    model = OrderItem
    fields = ('course', 'price')
    readonly_fields = ('course', 'price')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'total', 'user', 'created', 'paid']
    list_filter = ['id', 'created']
    list_per_page = 10
    inlines = (OrderInline,)
