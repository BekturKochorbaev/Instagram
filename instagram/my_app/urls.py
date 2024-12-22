from django.urls import path
from .views import *


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('profile_list/', UserProfileListAPIView.as_view(), name='profile_list'),
    path('profile_create/', UserProfileCreateAPIView.as_view(), name='profile_create'),
    path('follow_list/', FollowListAPIView.as_view(), name='follow_list'),
    path('post_list/', PostListAPIView.as_view(), name='post_list'),
    path('post_create/', PostCreateAPIView.as_view(), name='post_create'),
    path('comment/', CommentListCreateSerializers.as_view(), name='comment'),
    path('comment_like/', CommentLikeCreateAPIView.as_view(), name='comment_like'),
    path('story_list/', StoryListAPIView.as_view(), name='story_list'),
    path('story_create/', StoryCreateAPIView.as_view(), name='story_create'),

    path('save/', SavedViewSet.as_view({'get': 'retrieve'}), name='save_detail'),

    path('save_item/', SaveItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='save_item_list'),
    path('save_item/<int:pk>/', SaveItemViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='save_item_detail')



]