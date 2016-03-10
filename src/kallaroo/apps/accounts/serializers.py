from django.contrib.auth import update_session_auth_hash 	# http://django.readthedocs.org/en/latest/topics/auth/default.html

from rest_framework import serializers

from .models import User

class CreateUserSerializer(serializers.ModelSerializer):

	class Meta:

		model = User
		fields = ('email', 'username', 'first_name', 'last_name', 'password', 'profile_pic', 'is_contractor', 'subcategory',)
		extra_kwargs = {'password': {'write_only': True}}

	def create(self, validated_data):
		user = User(
			email=validated_data['email'],
			username=validated_data['username'],
			first_name=validated_data['first_name'],
			last_name=validated_data['last_name'],
			profile_pic=validated_data['profile_pic'],
			is_contractor=validated_data['is_contractor'],
			subcategory=validated_data['subcategory'],
		)

		user.set_password(validated_data['password'])
		user.save()

		return user

class UserSerializer(serializers.ModelSerializer):
	# password = serializers.CharField(write_only=True, required=False)
	# password2 = serializers.CharField(write_only=True, required=False)

	class Meta:

		model = User
		fields = ('id', 'email', 'username', 'first_name', 'last_name',
			'joined_on', 'subcategory', 'rating', 'phone_number', 'date_of_birth',
			'stripe_account_id', 'stripe_customer_id', 'stripe_card_id', 'stripe_bank_account_id',
			'stripe_secret_key', 'stripe_publishable_key', 'socket_id','password',)
		read_only_fields = ('joined_on', 'stripe_account_id', 'stripe_customer_id', 'stripe_card_id',
			'stripe_bank_account_id', 'stripe_secret_key', 'stripe_publishable_key', 'socket_id',)

