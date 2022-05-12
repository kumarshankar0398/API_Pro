from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.exceptions import ValidationError
from uuid import uuid4
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    # def create(self, validated_data):
    #     user = User.objects.create(
    #         email=validated_data['email'],
    #         username=validated_data['username'],
    #         password=make_password(validated_data['password'])
    #     )
    #     user.set_password(user.password)
    #     # print(user.password)
    #     user.save()
    #     return user

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        user.set_password(user.password)
        # print(user.password)
        user.save()
        return user




class UserLoginSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField()
    password = serializers.CharField()
    token = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        user_id = data.get("user_id", None)
        password = data.get("password", None)
        user = User.objects.get(username=user_id)
        print('password:', user.password)
        print('password123:', password)
        check = user.check_password(password)
        print('check:', check)
        if not check:
            raise ValidationError("User credentials are not correct")
        if user.ifLogged:
            raise ValidationError("User already logged in.")
        user.ifLogged = True
        data['token'] = uuid4()
        user.token = data['token']
        user.save()
        return data

    class Meta:
        model = User
        fields = (
            'user_id',
            'password',
            'token',
        )

        read_only_fields = (
            'token',
        )


class UserLogoutSerializer(serializers.ModelSerializer):
    token = serializers.CharField()
    status = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        token = data.get("token", None)
        print(token)
        try:
            user = User.objects.get(token=token)
            if not user.ifLogged:
                raise ValidationError("User is not logged in.")
        except Exception as e:
            raise ValidationError(str(e))
        user.ifLogged = False
        user.token = ""
        user.save()
        data['status'] = "User is logged out."
        return data

    class Meta:
        model = User
        fields = (
            'token',
            'status',
        )


class ResetPasswordSErializer(serializers.Serializer):
    model = User
    email = serializers.EmailField(required=True)


class ResetPassSerializer(serializers.Serializer):
    model = User
    received_code = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    confirm_passwrod = serializers.CharField(required=True)
