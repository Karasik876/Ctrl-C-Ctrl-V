from django.db import models
from users.models import UserAccount
from classes.models import Class


class Test(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, verbose_name='Пользователь')
    the_class = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name='Класс')
    test_name = models.CharField(max_length=50, default='Новый тест', verbose_name='Название')
    questions = models.IntegerField(verbose_name='Кол-во вопросов')
    choices = models.IntegerField(verbose_name='Кол-во ответов')
    answers = models.CharField(max_length=50, verbose_name='Ответы')
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')

    objects = models.Manager()

    def __str__(self):
        return self.test_name
