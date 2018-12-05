from django.db import models
from django_mysql.models import ListCharField


# Create your models here.
class Puppy(models.Model):
    """
    Puppy Model
    Defines the attributes of a puppy
    """
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    breed = models.CharField(max_length=255, null=True)
    color = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_breed(self):
        return self.name + ' pertence à raça ' + self.breed

    def __repr__(self):
        return self.name + ' está adicionado.'


class UserFace(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class UserInsta(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class UserTinder(models.Model):
    name = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    age = models.IntegerField()
    gender_filter = models.IntegerField()
    max_ditance = models.IntegerField()
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    photo = models.CharField(max_length=255)
    fb_user_id = models.OneToOneField(UserFace, related_name='user_tinder', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class People(models.Model):
    name = models.CharField(max_length=255)
    age = models.PositiveSmallIntegerField()
    distance = models.PositiveSmallIntegerField()
    bio = models.TextField()
    jobs = models.CharField(max_length=255)
    schools = models.CharField(max_length=255)
    insta_name = models.CharField(max_length=255)
    insta_id = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PhotosPeople(models.Model):
    photo_id = models.CharField(max_length=255)
    photo_url = models.CharField(max_length=255)
    people = models.ForeignKey(People, related_name='photos', on_delete=models.CASCADE)

    def __str__(self):
        return '%s: %s' % (self.photo_id, self.photo_url)

    def __unicode__(self):
        return '%s: %s' % (self.photo_id, self.photo_url)