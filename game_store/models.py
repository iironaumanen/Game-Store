from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

class StoreUser(AbstractUser):
    owned_games = models.ManyToManyField('Game', blank = True)
    is_developer = models.BooleanField(default = False)


class Game(models.Model):
    title = models.CharField(max_length = 30)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    source = models.URLField(default = '')
    submitter = models.ForeignKey('StoreUser', on_delete=models.CASCADE)
    categories = models.ManyToManyField('Category')

    def __unicode__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length = 30, primary_key = True)
    

class Score(models.Model):
    score = models.BigIntegerField()
    time = models.DateTimeField(primary_key = True, default=datetime.datetime.now())
    submitter = models.ForeignKey('StoreUser', on_delete=models.CASCADE)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)

class Save(models.Model):
    user = models.ForeignKey('StoreUser', on_delete=models.CASCADE)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    data = models.TextField()

class Transaction(models.Model):
    id = models.CharField(max_length = 32, primary_key = True)
    date = models.DateTimeField()
    price = models.IntegerField()
    is_complete = models.BooleanField()
    buyer = models.ForeignKey('StoreUser', on_delete=models.CASCADE)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
