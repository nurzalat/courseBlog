from django.core.exceptions import ObjectDoesNotExist
from rest_auth.views import LogoutView
from rest_framework import generics, permissions

from rest_framework.viewsets import ModelViewSet

from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth.models import User
from blog_api import serializers
from blog_api.models import Category, Post

# TODO add permissions to post and comment
# TODO end comment CRUD
# TODO add likes


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserRegisterSerializer


class CustomLogoutView(LogoutView):
    permission_classes = (permissions.IsAuthenticated, )


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserListSerializer


class UserDetailedView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserDetailedSerializer


class PostView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = serializers.PostSerializer(posts, many=True, context={'request': self.request})
        # context={'request': 'format': self.format_kwarg, self.request, 'view': self}
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.PostSerializer(data=request.data, context={'request': self.request})
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class PostDetailView(APIView):
    @staticmethod
    def get_object(pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Exception("Not Found")

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = serializers.PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = serializers.PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response("Post is deleted", 204)

# ViewSet implementation
# class PostViewSet(ModelViewSet):
#     class Meta:
#         model = Post
#         fields = '__all__'
#     queryset = Post.objects.all()
#     serializer_class = serializers.PostSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)


# CRUD implementation
# class PostCreateView(generics.CreateAPIView):
#     serializer_class = serializers.PostSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
#
# class PostListView(generics.ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = serializers.PostSerializer
#
#
# class PostDetailView(generics.RetrieveAPIView):
#     queryset = Post.objects.all()
#     serializer_class = serializers.PostSerializer
#
#
# class PostUpdateView(generics.UpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = serializers.PostSerializer
#
#
# class PostDeleteView(generics.DestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = serializers.PostSerializer

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer