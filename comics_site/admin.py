from django.contrib import admin
from .models import Category, Comic, Images


class ComicsImagesInline(admin.StackedInline):
    model = Images


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ComicsAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ComicsImagesInline]


admin.site.register(Comic, ComicsAdmin)
admin.site.register(Category, CategoryAdmin)
