from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from .models import User, BlogPost, Category, Tag, Comment
from .serializers import (
    UserSerializer, BlogPostSerializer, CategorySerializer,
    TagSerializer, CommentSerializer
)
from .permissions import IsAdminUser, IsBloggerUser, IsAdminOrAuthorOrReadOnly
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from .exceptions import BlogPostNotFound, UnauthorizedAccess, InvalidBlogData
from django.db import transaction

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        if self.request.user.is_admin:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

class BlogPostViewSet(viewsets.ModelViewSet):
    serializer_class = BlogPostSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'categories__name', 'tags__name']
    ordering_fields = ['created_at', 'title']

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_admin:
            return BlogPost.objects.all()
        return BlogPost.objects.filter(is_hidden=False)

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [IsBloggerUser]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminOrAuthorOrReadOnly]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                raise InvalidBlogData(detail=serializer.errors)
            
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            raise InvalidBlogData(detail=str(e))

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            raise BlogPostNotFound()

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            
            if instance.author != request.user and not request.user.is_admin:
                raise UnauthorizedAccess()

            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            if not serializer.is_valid():
                raise InvalidBlogData(detail=serializer.errors)
            
            self.perform_update(serializer)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            raise BlogPostNotFound()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if instance.author != request.user and not request.user.is_admin:
                raise UnauthorizedAccess()
            
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            raise BlogPostNotFound()

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_admin:
            return Comment.objects.all()
        return Comment.objects.filter(is_hidden=False)

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminOrAuthorOrReadOnly]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        post = get_object_or_404(BlogPost, pk=self.kwargs['post_pk'])
        serializer.save(author=self.request.user, post=post)
