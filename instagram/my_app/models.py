from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    bio = models.TextField()
    image = models.ImageField(upload_to='profile_image/', null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    GENDER = (
        ('male', 'male'),
        ('female', 'female'),
        ('other', 'other')

    )
    gender = models.CharField(max_length=10, choices=GENDER)

    def __str__(self):
        return str(self.username)


class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='following')
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.follower


class Post(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_post')
    image = models.ImageField(upload_to='post_image/', null=True, blank=True)
    video = models.FileField(upload_to='post_videos/', null=True, blank=True)
    description = models.TextField()
    hashtag = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'

    def get_count_like(self):
        like = self.like.all()
        if like.exists():
            return like.count()
        return 0


class PostLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like')
    like = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'

    class Meta:
        unique_together = ('user', 'post')



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_comment')
    text = models.TextField()
    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name='parent_review', null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'

    def get_count_like(self):
        like = self.comment_like.all()
        if like.exists():
            return like.count()
        return 0


class CommentLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_comment_like')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_like')
    text = models.TextField()
    like = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user

    class Meta:
        unique_together = ('user', 'comment')


class Story(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_story')
    image = models.ImageField(upload_to='store_image/', null=True, blank=True)
    video = models.FileField(upload_to='story_videos/', null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'


class Saved(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_save')

    def __str__(self):
        return self.user


class SaveItem(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='save_post')
    save = models.ForeignKey(Saved, on_delete=models.CASCADE, related_name='save')
    created_at = models.DateField(auto_now_add=True)


class Chat(models.Model):
    person = models.ManyToManyField(UserProfile)
    created_date = models.DateField(auto_now_add=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='massege')
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='author')
    text = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='massege_img/')
    video = models.FileField(upload_to='massege_video/')



