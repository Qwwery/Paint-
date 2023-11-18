from django.db import models
from django import forms


class Profils(models.Model):
    login = models.CharField('Логин', max_length=50)
    password = models.CharField('Пароль', max_length=20)

    def __str__(self):
        return self.login

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Image(models.Model):
    login = models.CharField('Логин', max_length=20)
    name = models.CharField('Имя рисунка', max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
