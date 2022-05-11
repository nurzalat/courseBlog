from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        if not self.parent:
            return f'{self.name}'
        else:
            return f'{self.parent} --> {self.name}'


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True)
    owner = models.ForeignKey('auth.User', related_name='posts_owner', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='posts_category', on_delete=models.CASCADE)
    preview = models.ImageField(upload_to='images/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self): return f'{self.owner} {self.title}'


class PostImages(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='images/')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='image_to_post')

    class Meta:
        verbose_name = 'image'
        verbose_name_plural = 'images'

    @staticmethod
    def generate_name():
        import random
        return 'image_' + str(random.randint(1000000, 9999999))

    def save(self, *args, **kwargs):
        self.title = self.generate_name()
        return super(PostImages, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.title} -> {self.post.id}'


class Comment(models.Model):
    owner = models.ForeignKey('auth.User', related_name='comment_to_user', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comment_to_post', on_delete=models.CASCADE)
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'comment'
        verbose_name_plural = 'comments'

    def __str__(self):
        return f'{self.owner} --> {self.post} --> {self.created_at}'


class Likes(models.Model):
    post = models.ForeignKey(Post, related_name='like_to_post', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', related_name='like_to_user', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['post', 'user']
        verbose_name = 'like'
        verbose_name_plural = 'likes'
