from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
   class Meta:
      model = UserProfile
      fields =('username', 'email', 'password', 'first_name', 'last_name')
      extra_kwargs = {'password': {'write_only': True}}

   def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

   def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
                },
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Неверные учетные данные')

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),

        }



class UserProfileSimpleSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username']


class UserProfileListSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'image', 'bio', 'website']


class UserProfileCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'image', 'bio', 'website', 'gender']


class FollowListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['follower', 'following']


class PostLikeSerializers(serializers.ModelSerializer):
    user = UserProfileSimpleSerializers(read_only=True)

    class Meta:
        model = PostLike
        fields = ['user', 'post', 'like']


class PostCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['user', 'image', 'video', 'description', 'hashtag']


class PostListSerializers(serializers.ModelSerializer):
    user = UserProfileSimpleSerializers(read_only=True)
    count_like = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['user', 'image', 'video', 'description', 'hashtag', 'count_like']

    def get_count_like(self, obj):
        return obj.get_count_like()



class CommentLikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ['user', 'comment', 'like']


class CommentSerializers(serializers.ModelSerializer):
    user = UserProfileSimpleSerializers(read_only=True)
    count_like = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['post', 'user', 'text', 'parent', 'created_at', 'count_like']

    def get_count_like(self, obj):
        return obj.get_count_like()


class StoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['user', 'image', 'video', 'created_at']


class StoryCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['user', 'image', 'video',]


class SaveItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = SaveItem
        fields = ['post', 'save', 'created_at']


class SavedSerializers(serializers.ModelSerializer):
    save = SaveItemSerializers(read_only=True, many=True)

    class Meta:
        model = Saved
        fields = ['user', 'save']

