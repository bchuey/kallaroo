from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from ..categories.models import Subcategory
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.core.validators import RegexValidator
import braintree
import stripe

"""
*Don't forget to import the PLATFORM_SECRET_KEY

stripe.api_key = PLATFORM_SECRET_KEY
"""

stripe.api_key = 'sk_test_BvXnJuHaPBDFDR0nou3Qq4Qn'

braintree.Configuration.configure(braintree.Environment.Sandbox,
    merchant_id=settings.BRAINTREE_MERCHANT_ID,
    public_key=settings.BRAINTREE_PUBLIC,
    private_key=settings.BRAINTREE_PRIVATE,
)


# Create your models here.
class UserManager(BaseUserManager):
	def create_user(self, email, username, first_name, last_name, password=None):
		if not email:
			raise ValueError("Users must have an email address")
		user = self.model(
			email=self.normalize_email(email),
			username = username,
			first_name=first_name,
			last_name=last_name,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, first_name, last_name, password):
		user = self.create_user(
			email=email, 
			username=username, 
			first_name=first_name, 
			last_name=last_name,
			password=password
		)
		user.is_admin = True
		user.save(using=self._db)
		return user

class User(AbstractBaseUser):
	email = models.EmailField(max_length=255, unique=True)
	username = models.CharField(max_length=80)
	first_name = models.CharField(max_length=45)
	last_name = models.CharField(max_length=45)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	joined_on = models.DateTimeField(auto_now_add=True, auto_now=False)
	is_online = models.BooleanField(default=False)
	is_contractor = models.BooleanField(default=False)
	profile_pic = models.ImageField(null=True, blank=True)
	subcategory = models.ForeignKey(Subcategory, max_length=255, null=True, blank=True)
	rating = models.IntegerField(null=True, blank=True)
	
	# phone number for Twilio
	phone_regex = RegexValidator(regex=r'', message="Phone numbers must be in +9999999999 format")
	phone_number = models.CharField(max_length=12, validators=[phone_regex], blank=True)


	# address
	address = models.CharField(max_length=255, null=True, blank=True)

	# Braintree unique ID
	# braintree_id = models.CharField(max_length=255, null=True, blank=True)
	# braintree_client_token = models.CharField(max_length=2000, null=True, blank=True)
	# payment_method_nonce = models.CharField(max_length=255, null=True, blank=True)
	# payment_method_token = models.CharField(max_length=255, null=True, blank=True)

	# Stripe (Managed Accounts)
	date_of_birth = models.DateField(auto_now_add=False, auto_now=False, null=True, blank=True)
	stripe_account_id = models.CharField(max_length=255, null=True, blank=True)
	stripe_customer_id = models.CharField(max_length=255, null=True, blank=True)
	stripe_card_id = models.CharField(max_length=255, null=True, blank=True)
	stripe_bank_account_id = models.CharField(max_length=255, null=True, blank=True)

	stripe_secret_key = models.CharField(max_length=255, null=True, blank=True)
	stripe_publishable_key = models.CharField(max_length=255, null=True, blank=True)


	# sockets
	socket_id = models.CharField(max_length=255, null=True, blank=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

	objects = UserManager()

	def __str__(self):
		return self.email

	class Meta:
		db_table = 'users'

	def get_full_name(self):
		full_name = '%s' + ' ' + '%s' %(first_name, last_name)
		return self.full_name

	def get_short_name(self):
		return self.username

	def is_staff(self):
		return self.is_admin

	def has_perm(self, perm, object=None):
		return True

	def has_module_perms(self, app_label):
		return True

	"""
	You can call these instance methods in a view later on.
	e.g. context['client_token'] = user.get_client_token()

	Might be best to save the client_token once you have created it the first time
	"""
	# def get_braintree_id(self):

	# 	if not self.braintree_id:
	# 		result = braintree.Customer.create({
	# 			"first_name": self.first_name,
	# 	    	"last_name": self.last_name,
	# 	    	"email": self.email,
	# 		})
	# 		if result.is_success:
	# 			self.braintree_id = result.customer.id
	# 			self.save()
	# 	return self.braintree_id
	# 	# return None
		
	# def get_client_token(self):
	# 	customer_id = self.get_braintree_id()
	# 	if customer_id:
	# 		client_token = braintree.ClientToken.generate({
	# 				"customer_id": customer_id,
	# 			})
	# 		self.braintree_client_token = client_token
	# 		self.save()
	# 		return client_token
	# 	return None

	"""
	==========
	STRIPE
	==========
	"""

	# def get_stripe_id(self):
	# 	result = stripe.Account.create(
	# 				country='US',
	# 				managed=True,
	# 			)

	# 	self.stripe_id = result.id
	# 	self.stripe_secret_key = result.keys.secret
	# 	self.stripe_publishable_key = result.keys.publishable
	# 	self.save()

	# 	context = {
	# 		'stripe_id': self.stripe_id,
	# 		'stripe_secret_key': self.stripe_secret_key,
	# 		'stripe_publishable_key': self.stripe_publishable_key,
	# 	}

	# 	return context


"""
===============================
Need to learn how signals work
===============================
1.) On registration, send a signal and run the CreateBraintreeCustomer
2.) instance is the User that just registered
3.) add 'braintree_id' field to User model
4.) set instance.braintree_id = result.customer.id 

post_save.connect(method_name, sender=another_method_or_class_name)

"""
# def update_braintree_id(sender, instance, *args, **kwargs):
# 	if not instance.braintree_id:
# 		instance.get_braintree_id()

# post_save.connect(update_braintree_id, sender=User)

# class UserPaymentInfo(models.Model):
# 	user = models.ForeignKey(User, on_delete=models.CASCADE)
# 	date_of_birth = models.DateField(blank=True)
# 	stripe_id = models.CharField(max_length=255, blank=True)
# 	stripe_secret_key = models.CharField(max_length=255, blank=True)
# 	stripe_publishable_key = models.CharField(max_length=255, blank=True)

# 	class Meta:
# 		db_table = 'userpaymentinfos'

# 	def __str__(self):
# 		return str(self.id)

# 	"""
# 	==========
# 	STRIPE
# 	==========
# 	"""

# 	def get_stripe_id(self):
# 		result = stripe.Account.create(
# 					country='US',
# 					managed=True,
# 				)

# 		self.stripe_id = result.id
# 		self.stripe_secret_key = result.keys.secret
# 		self.stripe_publishable_key = result.keys.publishable
# 		self.save()

# 		context = {
# 			'stripe_id': self.stripe_id,
# 			'stripe_secret_key': self.stripe_secret_key,
# 			'stripe_publishable_key': self.stripe_publishable_key,
# 		}

# 		return context







class UserAddressManager(models.Manager):
	def create_address(self, street_number, street_address, city, state, zipcode):

		address = self.model(
			street_number=street_number,
			street_address=street_address,
			city=city,
			state=state,
			zipcode=zipcode,
		)

		address.save(using=self._db)
		return address

class UserAddress(models.Model):
	STATE_CHOICES = (
		('AZ', 'AZ'),
		('CA', 'CA'),
		('TX', 'TX'),
	)
	street_number = models.IntegerField()
	street_address = models.CharField(max_length=60)
	city = models.CharField(max_length=60)
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='AZ')
	zipcode = models.IntegerField()
	user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

	objects = UserAddressManager()

	class Meta:
		db_table = 'user_addresses'

	def __str__(self):
		return self.get_address()

	def get_address(self):
		return "%s %s, %s, %s, %s" %(self.street_number, self.street_address, self.city, self.state, self.zipcode)
