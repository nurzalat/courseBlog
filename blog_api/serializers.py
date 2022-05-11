from django.contrib.auth.models import User
from rest_framework import serializers

from blog_api.models import Category, Post, PostImages, Comment


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
        exclude = ('password',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImages
        exclude = ('id',)


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Comment
        fields = ('id', 'body', 'owner', 'created_at', 'post',)


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(
        source='owner.username'
    )
    image_to_post = PostImageSerializer(many=True, read_only=False, required=False)
    comment_to_post = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'owner', 'preview', 'image_to_post', 'category', 'comment_to_post', )

    def create(self, validated_data):
        # print('validated_data: ', validated_data)
        request = self.context.get('request')
        # print('request ', request)
        # print('Files: ', request.FILES)
        images_data = request.FILES
        created_post = Post.objects.create(**validated_data)
        # print(created_post)
        # print('worked', images_data.getlist('image_to_post'))
        images_objects = [PostImages(post=created_post, image=image) for image in images_data.getlist('image_to_post')]
        PostImages.objects.bulk_create(images_objects)
        return created_post

    def is_liked(self, post):
        user = self.context.get('request').user
        return user.like_to_user.filter(post=post).exists()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comments_detail'] = CommentSerializer(instance.comment_to_post.all(), many=True).data
        user = self.context.get('request').user
        if user.is_authenticated:
            representation['is_liked'] = self.is_liked(instance)
        representation['likes_count'] = instance.like_to_post.count()
        return representation
