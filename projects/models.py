from core.models import UserProfile, Skillset
from django.db import models
    
class Project(models.Model):
    def __unicode__(self):
        return self.name
    
    def slots(self):
        return Slot.objects.filter(project=self)
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    owner = models.ForeignKey(UserProfile)
     
class Slot(models.Model):
    user = models.OneToOneField(UserProfile, blank=True, null=True)
    project = models.ForeignKey(Project)
    skillset = models.OneToOneField(Skillset)