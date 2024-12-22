from django.shortcuts import render
from requests import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, viewsets, status
from rest_framework.pagination import PageNumberPagination
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({'detail': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class Pagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializers

    def get_queryset(self):
        return UserProfile.objects.filter(username=self.request.user.usernsme)


class UserProfileCreateAPIView(generics.CreateAPIView):
    serializer_class = UserProfileCreateSerializers

    def get_queryset(self):
        return UserProfile.objects.filter(username=self.request.user.usernsme)


class FollowListAPIView(generics.ListAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowListSerializers


class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializers
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['hashtag']
    search_fields = ['username',]
    ordering_fields = ['created_at']
    pagination_class = Pagination



class PostCreateAPIView(generics.CreateAPIView):
    serializer_class = PostCreateSerializers


class CommentListCreateSerializers(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers


class CommentLikeCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentLikeSerializers


class StoryListAPIView(generics.ListAPIView):
    queryset = Story.objects.all()
    serializer_class = StoryListSerializers


class StoryCreateAPIView(generics.ListAPIView):
    serializer_class = StoryCreateSerializers


class SavedViewSet(viewsets.ModelViewSet):
    serializer_class = SavedSerializers

    def get_queryset(self):
        return Saved.objects.filter(username=self.request.user)


class SaveItemViewSet(viewsets.ModelViewSet):
    serializer_class = SaveItemSerializers

    def get_queryset(self):
        return SaveItem.objects.filter(username=self.request.user)

