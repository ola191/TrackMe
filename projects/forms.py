from django import forms
from .models import Project
from users.models import CustomUser
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']

class AddTeamMemberForm(forms.Form):
    member = forms.ModelChoiceField(queryset=CustomUser.objects.all(), label='Add Team Member')