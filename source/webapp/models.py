from django.db import models
from django.contrib.auth import get_user_model


class Announcement(models.Model):
    CHOICES = (
        ('on_moderation', "на модерации"),
        ('published', "Опубликовано"),
        ('rejected', "ОТклонено"),
        ('delete', "На удаление"),
    )
    image = models.ImageField(upload_to='announcement/picture/', verbose_name='Картинка')
    title = models.CharField(max_length=100, blank=False, null=False, verbose_name='Заголовок')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    author = models.CharField(max_length=100, blank=False, null=False, verbose_name='Автор')
    category = models.CharField(max_length=100, blank=False, null=False, verbose_name='Категория')
    price = models.IntegerField(verbose_name='Цена')
    status = models.CharField(max_length=100, choices=CHOICES, default='on_moderation' ,verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    published_at = models.DateTimeField()
    edited_at = models.DateTimeField(auto_now=True, verbose_name='Время измнения')

    def __str__(self):
        return f'{self.title} - {self.author}'


class Category(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, verbose_name='Название')

    def __str__(self):
        return self.name


class Comment(models.Model):
    text = models.TextField(blank=False, null=False, verbose_name='Текст'),
    author = models.ForeignKey(get_user_model(),related_name='announcements', on_delete=models.CASCADE, verbose_name='Автор')
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='comments', verbose_name='Объявление')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return f'{self.text}-{self.author}'