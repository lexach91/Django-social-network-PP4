from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from profiles.models import Profile
from communities.models import Community


POST_TYPE_CHOICES = (
    (1, 'profile_wall'),
    (2, 'community_wall'),
)


class Post(models.Model):
    """Post model"""
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='posts',
        null=True,
    )
    content = models.TextField(max_length=500)
    has_media = models.BooleanField(default=False)
    image = CloudinaryField(
        'post_image',
        folder='posts',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)
    post_type = models.IntegerField(choices=POST_TYPE_CHOICES)
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name='posts',
        null=True,
        blank=True
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='posts',
        null=True,
        blank=True
    )
    likes = models.ManyToManyField(
        User,
        related_name='liked_posts',
        blank=True
    )
    dislikes = models.ManyToManyField(
        User,
        related_name='disliked_posts',
        blank=True
    )

    def get_likes(self):
        """Returns count of the post's likes"""
        return self.likes.count()

    def get_dislikes(self):
        """Returns count of the post's dislikes"""
        return self.dislikes.count()

    def comments_count(self):
        """Returns count of the post's comments"""
        return self.comments.count()

    def get_comments(self):
        """Returns all post's comments"""
        return self.comments.all()

    def get_url(self):
        """Returns post's url with its id"""
        if self.post_type == 1:
            return f'/profiles/{self.profile.user.username}/#post-{self.id}'
        else:
            return f'/communities/{self.community.slug}/#post-{self.id}'

    class Meta:
        """Post model meta"""
        ordering = ['-created_at']

    def __str__(self):
        """Post model string representation"""
        return self.content


class Comment(models.Model):
    """Comment model"""
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='comments',
        null=True,
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)
    likes = models.ManyToManyField(
        User,
        related_name='liked_comments',
        blank=True
    )
    dislikes = models.ManyToManyField(
        User,
        related_name='disliked_comments',
        blank=True
    )

    class Meta:
        """Comment model meta"""
        ordering = ['created_at']

    def __str__(self):
        """Comment model string representation"""
        return self.content

    def get_likes(self):
        """Returns count of the comment's likes"""
        return self.likes.count()

    def get_dislikes(self):
        """Returns count of the comment's dislikes"""
        return self.dislikes.count()

    def get_url(self):
        """Returns comment's url with its post id"""
        if self.post.post_type == 1:
            url_start = '/profiles/'
            url_wall = self.post.profile.user.username
            url_post = f'#post-{self.post.id}'
            return url_start + url_wall + url_post
        else:
            url_start = '/communities/'
            url_wall = self.post.community.slug
            url_post = f'#post-{self.post.id}'
            return url_start + url_wall + url_post
