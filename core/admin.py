from django.contrib import admin
from core.models import Skillset, Skill

class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', )

admin.site.register(Skillset)
admin.site.register(Skill, SkillAdmin)