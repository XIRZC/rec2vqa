# Create your models here.
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=64, verbose_name='name')
    age = models.IntegerField(verbose_name='age')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'user'
        ordering = ['id']
        verbose_name = 'UserTable'
        verbose_name_plural = verbose_name