from core.models import UserProfile, Skillset
from django.db import models
    
class Project(models.Model):
    def __unicode__(self):
        return self.name
    
    def slots(self):
        return Slot.objects.filter(project=self)
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    owner = models.ForeignKey(UserProfile)
     
class Slot(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    user = models.ForeignKey(UserProfile, blank=True, null=True)
    project = models.ForeignKey(Project)
    skillset = models.OneToOneField(Skillset)
    
    def applicants(self):
        applications = Application.objects.all().filter(slot=self).select_related()
        applicants = set()
        
        for application in applications:
            applicants.add(application.applicant)
        
        return applicants 

class Application(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    slot = models.ForeignKey(Slot)
    applicant = models.ForeignKey(UserProfile)
    accepted = models.NullBooleanField()
    