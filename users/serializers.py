from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'date_of_birth',
            'gender',
            'blood_group',
            'image',
            'password',
            'password2'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        """Ensure passwords match"""
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return data

    def create(self, validated_data):
        """Create and return a new user"""
        validated_data.pop('password2')  # Remove password2 from the data
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Validate user credentials"""
        email = data.get("email")
        password = data.get("password")

        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid email or password.")

        if not user.is_active:
            raise serializers.ValidationError("User account is inactive.")

        data["user"] = user  # Attach user object to data
        return data
    
    
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    def validate_new_password(self, value):
        """Validate the new password against Django's password policies"""
        validate_password(value)
        return value
    
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id", 
            "username", 
            "email", 
            "first_name", 
            "last_name",
            "date_of_birth",
            "gender",
            "blood_group",
            "image",
            "date_joined",
        ]
        read_only_fields = ["id", "email"]  # Users cannot change their email