from django.db import models
from users.models import UserAccount


class Class(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, verbose_name='Пользователь')
    class_name = models.CharField(max_length=20, default='Новый класс', verbose_name='Название')
    class_number = models.IntegerField(verbose_name='Класс')
    class_letter = models.CharField(max_length=1, default='', verbose_name='Буква')
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')

    objects = models.Manager()

    def __str__(self):
        return f'{self.class_name} {self.class_number}{self.class_letter}'
