from rest_framework import serializers
from auth_app.models import User
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    completeName = serializers.CharField(source='complete_name')
    repeatedPassword = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['completeName', 'email', 'password', 'repeatedPassword']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if data['password'] != data['repeatedPassword']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('repeatedPassword')
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            complete_name=validated_data['complete_name'],
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid email or password")
        data['user'] = user
        return data