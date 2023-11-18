from django.db import models
from users.models import UserAccount


class Test(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=50, default='Новый тест')
    questions = models.IntegerField()
    choices = models.IntegerField()
    answers = models.CharField(max_length=50)

    objects = models.Manager()

    def __str__(self):
        return self.test_name
