from django.contrib import admin
from .models import Task, Bid, Location
# Register your models here.

class LocationInline(admin.TabularInline):
	model = Location
	extra = 0

class BidInline(admin.TabularInline):
	model = Bid
	extra = 0

class TaskAdmin(admin.ModelAdmin):
	model = Task
	list_display = ('id', 'title', 'user')
	inlines = [
		BidInline, LocationInline,
	]
	fieldsets = (
		('Task', {
			'fields': ('user', 'contractor', 'title', 'description', 'special_instructions',)
		}),
		('Bidding', {
			'fields': ('bidding_closed_at',)
		}),
		('Task Status', {
			'fields': ('task_status', 'task_clock_in', 'task_clock_out', 'is_completed', 'task_completed_at',)
		}),
		('Payment', {
			'fields': ('final_payment',)
		}),
		('Subcategory', {
			'fields': ('subcategory',)
		}),
		('Address', {
			'fields': ('address',)
		}),
	)


admin.site.register(Task, TaskAdmin)