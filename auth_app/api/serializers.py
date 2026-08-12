from rest_framework import serializers
from auth_app.models import User


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