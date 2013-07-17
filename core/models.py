from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', related_name='profile')
    matriculation_nr = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    studies = models.CharField(max_length=255)
              
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)


class Skill(models.Model):
    name = models.CharField(max_length=200)
    image_name = models.CharField(max_length=50)
    red = models.IntegerField()
    blue = models.IntegerField()
    green = models.IntegerField()

class Skillset(models.Model):
    skills = models.ManyToManyField(Skill, blank=True, null=True)