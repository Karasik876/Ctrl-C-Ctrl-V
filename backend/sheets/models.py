from django.db import models
from users.models import UserAccount
from tests.models import Test
from classes.models import Class


class Sheet(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, verbose_name='Пользователь')
    test = models.ForeignKey(Test, on_delete=models.SET_NULL, null=True, verbose_name='Тест')
    the_class = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name='Класс')
    name_image = models.CharField(max_length=255, null=True, verbose_name='Имя')
    sheet_image = models.CharField(max_length=255, null=True, verbose_name='Бланк')
    student_answers = models.CharField(max_length=255, verbose_name='Ответы')
    result = models.IntegerField(verbose_name='Кол-во баллов')
    scanned_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата сканирования')

    objects = models.Manager()

    def __str__(self):
        return f'{self.user} | {self.test} | {self.the_class}'
