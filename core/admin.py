from django.contrib import admin
from core.models import Skillset, Skill, UserProfile

class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', )
    
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('last_name', )

admin.site.register(Skillset)
admin.site.register(Skill, SkillAdmin)
admin.site.register(UserProfile, UserProfileAdmin)