from django.contrib import admin
from .models import ShopProfile, Product, Invoice, WholesalerProfile

@admin.register(WholesalerProfile)
class WholesalerProfileAdmin(admin.ModelAdmin):
    list_display = ('wholesaler_name', 'user', 'phone', 'gst_number', 'approval_status')
    list_filter = ('approval_status',)
    search_fields = ('wholesaler_name', 'gst_number', 'phone')

@admin.register(ShopProfile)
class ShopProfileAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'wholesaler', 'user', 'phone', 'gst_number', 'approval_status')
    list_filter = ('approval_status', 'wholesaler')
    search_fields = ('shop_name', 'gst_number', 'phone')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('Invoice_number', 'customer_name', 'shop', 'total_amount', 'created_at')
    list_filter = ('created_at', 'shop')
    search_fields = ('Invoice_number', 'customer_name')

admin.site.register(Product)
