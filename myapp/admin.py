from django.contrib import admin
from .models import Computer, Part, Game, Cart, Shop


@admin.register(Computer)
class ComputerAdmin(admin.ModelAdmin):
    list_display = ('name', 'year_of_creation', 'user', 'date_of_sell', 'supplier', 'firm', 'price')
    search_fields = ('name', 'firm', 'user__username')  # Allows searching by name, firm, or username
    list_filter = ('year_of_creation', 'firm', 'state')  # Filter by these fields
    date_hierarchy = 'date_of_sell'  # Date-based drill-down navigation


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('name', 'firm', 'price', 'amount', 'date_of_creation', 'date_of_sale')
    search_fields = ('name', 'firm')
    list_filter = ('firm', 'date_of_creation', 'date_of_sale')
    date_hierarchy = 'date_of_creation'
    # For many-to-many relationships like computers


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'firm', 'price', 'date_of_publish')
    search_fields = ('name', 'firm')
    list_filter = ('firm', 'date_of_publish')
    date_hierarchy = 'date_of_publish'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'date_of_payment')
    search_fields = ('user__username',)
    list_filter = ('date_of_payment',)
    readonly_fields = ('total_price',)  # Make total_price read-only since it's calculated


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'total_users', 'total_sales', 'total_parts_in_stock', 'created_at', 'updated_at')
    search_fields = ('name', 'address')
    readonly_fields = ('total_sales', 'total_users', 'total_parts_in_stock', 'created_at',
                       'updated_at')  # Read-only fields for calculated data
