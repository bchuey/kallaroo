from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User, Contractor, ContractorProfile, UserAddress
from .forms import UserCreationForm, UserChangeForm

# Register your models here.
class UserAddressInline(admin.TabularInline):
	model = UserAddress
	extra = 0

class UserAdmin(BaseUserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm

	list_display = ('email', 'username', 'first_name', 'last_name', 'is_admin')
	list_filter = ('is_admin',)
	fieldsets = (

		(None, {'fields': ('email','username','password')}),
		('Personal info', {'fields': ('first_name', 'last_name',)}),
		('Permissions', {'fields': ('is_admin',)}),
		('Braintree', {'fields': ('braintree_id','braintree_client_token','payment_method_nonce','payment_method_token')})
	)

	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2')

		}),

	)
	seach_fields = ('email',)
	ordering = ('email',)
	filter_horizontal = ()
	inlines = [
		UserAddressInline,
	]

class ContractorProfileInline(admin.StackedInline):

	model = ContractorProfile
	extra = 1


class ContractorAdmin(admin.ModelAdmin):

	list_display = ['id','username', 'email', 'first_name', 'last_name', 'is_online', 'is_active']
	model = Contractor
	inlines = [
		ContractorProfileInline,
	]

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Contractor, ContractorAdmin)