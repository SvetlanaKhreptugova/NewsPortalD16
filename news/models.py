from django.core.cache import cache
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse

politic = 'PL'
culture = 'CL'
society = 'SC'
economy = 'EC'

OPTIONS = [
    (politic, 'Политика'),
    (culture, 'Культура'),
    (society, 'Общество'),
    (economy, 'Экономика')
]

news = "NS"
article = "AC"

TYPE = [
    (news, 'Новости'),
    (article, 'Статья')
]


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_author = models.IntegerField(default=0)
    author = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)

    def update_rating(self):
        sum_rating_of_post_multiply = \
            Post.objects.filter(author_id=self.pk).aggregate(rating=Coalesce(Sum('rating_post'), 0))['rating'] * 3
        rating_comments_author = Comment.objects.filter(comment_user_id=self.author).aggregate(
            comment_rating=Coalesce(Sum('rating_comment'), 0))['comment_rating']
        rating_comments_posts = Comment.objects.filter(comment_post__author__author=self.author).aggregate(
            post_rating=Coalesce(Sum('rating_comment'), 0))['post_rating']
        self.rating_author = sum_rating_of_post_multiply + rating_comments_author + rating_comments_posts
        self.save()

    def __str__(self):
        return f'{self.author}'


class Category(models.Model):
    themes = models.CharField(max_length=2, choices=OPTIONS, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories')

    def __str__(self):
        return self.get_themes_display()


class Post(models.Model):
    # objects = None
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    view = models.CharField(max_length=2, choices=OPTIONS)
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=250)
    text = models.TextField()
    rating_post = models.IntegerField(default=0)

    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        self.rating_post -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'

    def __str__(self):
        return f'{self.text}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    in_category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post}'  # добавил возможно удалить


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=250)
    time_in = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -= 1
        self.save()
