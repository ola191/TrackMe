from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from projects.models import Project
from tasks.models import Task

@login_required
def dashboard_view(request):
    return render(request, 'users/dashboard.html')

@login_required
def projects_view(request):
    projects = Project.objects.filter(owner=request.user)
    return render(request, 'projects/projects.html', {'projects': projects})

@login_required
def tasks_view(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/tasks.html', {'tasks': tasks})