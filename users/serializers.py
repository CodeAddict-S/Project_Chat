from users.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "password")

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            email=validated_data.get("email", ""),
        )
        user.set_password(validated_data["password"])  # parolni hash bilan saqlash
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        # Agar email yuborilgan bo‘lsa → username ni email orqali topamiz
        if email and not username:
            try:
                user_obj = User.objects.get(email=email)
                username = user_obj.username
            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid email or password.")

        # authenticate username orqali ishlaydi
        user = authenticate(username=username, password=password)
        if user:
            if not user.is_active:
                raise serializers.ValidationError("User is inactive.")
            data["user"] = user
            return data

        raise serializers.ValidationError("Invalid credentials.")
