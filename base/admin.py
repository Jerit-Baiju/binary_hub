from django.contrib import admin
from base.models import Category, ScrapItem, Order

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created']
    search_fields = ['name']

@admin.register(ScrapItem)
class ScrapItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller', 'price', 'category', 'quantity', 'location', 'is_available', 'created']
    list_filter = ['is_available', 'category', 'condition']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'created'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer', 'seller', 'scrap_item', 'quantity', 'total_price', 'status', 'created']
    list_filter = ['status']
    date_hierarchy = 'created'
    search_fields = ['buyer__username', 'seller__username', 'scrap_item__title']
