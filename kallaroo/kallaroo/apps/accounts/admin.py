from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User, UserAddress
from .forms import UserCreationForm, UserChangeForm

# Register your models here.
class UserAddressInline(admin.TabularInline):
	model = UserAddress
	extra = 0

class UserAdmin(BaseUserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm

	list_display = ('id', 'email', 'username', 'first_name', 'last_name','is_contractor', 'is_admin')
	list_filter = ('is_admin',)
	fieldsets = (

		('Account Info', {'fields': ('email','username','password')}),
		('Personal Info', {'fields': ('first_name', 'last_name',)}),
		('Permissions', {'fields': ('is_contractor', 'is_admin',)}),
		# ('Braintree', {'fields': ('braintree_id','braintree_client_token','payment_method_nonce','payment_method_token')}),
		('Stripe', {'fields': ('stripe_account_id', 'stripe_customer_id', 'stripe_card_id', 'stripe_bank_account_id',)}),
		('Address', {'fields': ('address',)}),
		('Subcategory', {'fields': ('subcategory',)}),
		('Sockets', {'fields': ('socket_id',)}),
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

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
