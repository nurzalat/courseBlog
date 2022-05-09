from django.contrib.auth.models import User
from rest_framework import serializers

from blog_api.models import Category, Post


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=4, write_only=True, required=True)
    password_confirm = serializers.CharField(min_length=4, write_only=True, required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password_confirm')

    def validate(self, attrs):
        password_confirm = attrs.pop('password_confirm')
        if not password_confirm == attrs['password']:
            raise serializers.ValidationError('Passwords don\'t match')
        return attrs

    @staticmethod
    def validate_first_name(value):
        if not value.istitle():
            raise serializers.ValidationError('Name should start with capital letter')
        return value

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'],
                                   first_name=validated_data['first_name'],
                                   last_name=validated_data['last_name'],)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)


class UserDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(
        source='owner.username'
    )

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'owner', 'preview', 'category',)
