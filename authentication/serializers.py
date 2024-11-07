from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'phone_number', 'email', 'password']

    def create(self, validated_data):
        user = User(
            phone_number=validated_data['phone_number'],
            name=validated_data['name'],
            email=validated_data.get('email')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    