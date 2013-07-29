from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_save

class Skill(models.Model):
    
    def __unicode__(self):
        return self.name
    
    name = models.CharField(max_length=200)
    image_name = models.CharField(max_length=50)
    red = models.IntegerField()
    blue = models.IntegerField()
    green = models.IntegerField()

#leider bietet Django keine einfache Moeglichkeit, die Beziehung zwischen Skill- und SKillset 
#unseren Anforderungen entsprechend umzusetzen. Deshalb weichen wir hier auf die 
#zwar programmiertechnisch unschoene, aber deutlich lesbarere und unkompliziertere Version
#mit den 5 Skillfeldern aus
class Skillset(models.Model):
    skill1 = models.ForeignKey(Skill, related_name='skill1', blank=True, null=True)
    skill2 = models.ForeignKey(Skill, related_name='skill2', blank=True, null=True)
    skill3 = models.ForeignKey(Skill, related_name='skill3', blank=True, null=True)
    skill4 = models.ForeignKey(Skill, related_name='skill4', blank=True, null=True)
    skill5 = models.ForeignKey(Skill, related_name='skill5', blank=True, null=True)

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', related_name='profile')
    skillset = models.OneToOneField('Skillset', related_name='skillset', null=True)
    matriculation_nr = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    studies = models.CharField(max_length=255)
              
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        _, created = UserProfile.objects.get_or_create(user=instance)

def create_user_skillset(sender, instance, *args, **kwargs):
    if instance.skillset is None:
        skillset = Skillset()
        skillset.save()
        instance.skillset = skillset

post_save.connect(create_user_profile, sender=User)
pre_save.connect(create_user_skillset, sender=UserProfile)
