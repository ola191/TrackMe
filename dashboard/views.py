from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q
from projects.models import Project
from tasks.models import Task

@login_required
def dashboard_view(request):
    return render(request, 'users/dashboard.html')

@login_required
def projects_view(request):
    projects = Project.objects.filter(Q(owner=request.user) | Q(team=request.user))
    return render(request, 'projects/projects.html', {'projects': projects})

@login_required
def tasks_view(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/tasks.html', {'tasks': tasks})