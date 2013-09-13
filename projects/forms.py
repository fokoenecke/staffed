from django import forms
from projects.models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        widgets = {
          'description': forms.Textarea(attrs={'rows':6, 'cols':60}),
        }
        fields = ["name", "description"]