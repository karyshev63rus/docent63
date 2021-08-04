from django.contrib import admin
from .models import Section, Product


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'section', 'slug', 'price', 'available')
    list_editable = ('price', 'available')
    list_filter = ('section', 'available')
    prepopulated_fields = {'slug': ('name',)}
