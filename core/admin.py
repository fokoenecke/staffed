from django.contrib import admin
from core.models import Skillset, Skill, UserProfile
from projects.models import Application

class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', )
    
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('last_name', )

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('slot', )

admin.site.register(Skillset)
admin.site.register(Skill, SkillAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Application, ApplicationAdmin)