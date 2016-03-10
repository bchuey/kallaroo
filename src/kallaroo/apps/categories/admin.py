from django.contrib import admin
from .models import Category, Subcategory

class SubcategoryInline(admin.StackedInline):
	model = Subcategory
	extra  = 1
	fields = ['title', 'tagline', 'is_active']

class CategoryAdmin(admin.ModelAdmin):
	model = Category
	list_display = ['id', 'title']
	inlines = [
		SubcategoryInline,
	]


admin.site.register(Category, CategoryAdmin)