from django import forms
from .models import Project
from users.models import CustomUser

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']

class AddTeamMemberForm(forms.Form):
    member = forms.ModelChoiceField(queryset=CustomUser.objects.none(), label='')

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)
        if project:
            self.fields['member'].queryset = CustomUser.objects.exclude(id=project.owner_id)