from django.db import models
import datetime
from django.utils import timezone

class User(models.Model):
    user_name = models.CharField(max_length=100, primary_key=True)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    def __unicode__(self):
        return self.user_name


class Poll(models.Model):
    pub_date = models.DateTimeField('date published')
    create_user = models.CharField(max_length=200)
    json_string = models.TextField()
    poll_type = models.CharField(max_length=10)
    cost = models.FloatField(default=0.0)
    count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.question



class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    business_id = models.IntegerField()
    name = models.CharField(max_length=100)
    s_photo_url = models.CharField(max_length=2048)
    rating_img_url = models.CharField(max_length=2048)
    votes = models.IntegerField(default=0)


class Dish(models.Model):
    poll_id = models.IntegerField()
    dish_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.FloatField()
    amount = models.IntegerField()





