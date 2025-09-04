from django.contrib.auth.models import User
from rest_framework import serializers
from .models.members import MemberProfile, MemberBodyProfile
from .models.boutiques import BoutiqueProfile, BoutiqueCustomer

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )

class MemberProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = MemberProfile
        fields = [
            'id', 'user', 'bio', 'phone', 'address', 'avatar',
            'social_media', 'created_by', 'created_at', 'updated_at'
        ]


class MemberBodyProfileSerializer(serializers.ModelSerializer):
    member = MemberProfileSerializer()
    class Meta:
        model = MemberBodyProfile
        fields = "__all__"


class BoutiqueProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoutiqueProfile
        fields = [
            'id', 'name', 'description', 'address', 'phone',
            'email', 'website', 'social_media', 'logo', 'banner',
            'created_by', 'created_at', 'updated_at', 'status'
        ]


class BoutiqueCustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = BoutiqueCustomer
        fields = ['id', 'user', 'boutique', 'membership_date', 'is_active']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        boutique_customer = BoutiqueCustomer.objects.create(user=user, **validated_data)
        return boutique_customer