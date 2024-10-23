from django import forms
from .models import Task, Comment


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['project', 'title', 'description', 'assignee', 'status', 'due_date']

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super(TaskForm, self).__init__(*args, **kwargs)

        if project:
            self.fields['project'].initial = project
            self.fields['project'].widget = forms.HiddenInput()
        else:
            self.fields['project'].queryset = Project.objects.all()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
