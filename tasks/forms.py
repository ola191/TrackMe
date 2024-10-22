from django import forms
from .models import Task, Comment


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['project', 'title', 'description', 'assignee', 'status', 'due_date']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
