from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Product, IncomeSale

@admin.register(Product)
class ProductAdmin(SimpleHistoryAdmin):
    list_display = ('meat_code', 'meat_name', 'meat_in_price', 'meat_sell_price', 'create_user', 'created_at')
    search_fields = ('meat_code', 'meat_name')

@admin.register(IncomeSale)
class IncomeSaleAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "meat",
        "action_type",
        "quantity",
        "quantity_unit",
        "in_price",
        "sell_price",
        "total_in_price",
        "total_sell_price",
        "operation_date",
        "is_perexod",
    ]
    list_filter = ["action_type", "quantity_unit", "is_perexod"]
    search_fields = ["meat__meat_name", "meat__meat_code"]

