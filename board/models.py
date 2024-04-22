from django.db import models

from config import settings


class Advertisement(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    description = models.CharField(max_length=150, verbose_name='Описание')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')
    image = models.ImageField(upload_to='images/')

    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']


class Review(models.Model):
    text = models.TextField(max_length=150, verbose_name='Текст отзыва')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name='Автор')
    ad = models.ForeignKey(Advertisement, on_delete=models.CASCADE, verbose_name='Объявление')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
