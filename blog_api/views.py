from django.core.exceptions import ObjectDoesNotExist
from rest_auth.views import LogoutView
from rest_framework import generics, permissions
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

# from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth.models import User
from blog_api import serializers
from blog_api.models import Category, Post, Comment
from blog_api.permissions import IsAuthor

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

# TODO add likes


class StandardPaginationClass(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10000


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


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


# ViewSet implementation
class PostViewSet(ModelViewSet):
    class Meta:
        model = Post
        fields = '__all__'
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('category', 'owner',)
    search_fields = ('title',)
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = StandardPaginationClass

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(['GET'], detail=True)
    def comments(self, request, pk):
        post = self.get_object()
        comments = post.comment_to_post.all()
        serializer = serializers.CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        # only authenticated user can create a post
        if self.action in ('create',):
            return [permissions.IsAuthenticated()]
        # only owner of post can update/delete post/s
        elif self.action in ('update', 'partial_update', 'destroy',):
            return [IsAuthor()]
        # everyone can view posts
        else:
            return [permissions.AllowAny()]


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthor,)


# API view
# class PostView(APIView):
#     def get(self, request):
#         posts = Post.objects.all()
#         serializer = serializers.PostSerializer(posts, many=True, context={'request': self.request})
#         # context={'request': 'format': self.format_kwarg, self.request, 'view': self}
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = serializers.PostSerializer(data=request.data, context={'request': self.request})
#         if serializer.is_valid():
#             serializer.save(owner=request.user)
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)
#
#
# class PostDetailView(APIView):
#     @staticmethod
#     def get_object(pk):
#         try:
#             return Post.objects.get(pk=pk)
#         except Post.DoesNotExist:
#             raise Exception("Not Found")
#
#     def get(self, request, pk):
#         post = self.get_object(pk)
#         serializer = serializers.PostSerializer(post)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         post = self.get_object(pk)
#         serializer = serializers.PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save(owner=request.user)
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors)
#
#     def delete(self, request, pk):
#         post = self.get_object(pk)
#         post.delete()
#         return Response("Post is deleted", 204)


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
