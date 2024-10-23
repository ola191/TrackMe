from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q
from projects.models import Project
from tasks.models import Task

@login_required
def dashboard_view(request):
    recent_owner_projects = Project.objects.filter(Q(owner=request.user)).order_by('-created_at')[:3]
    recent_team_projects = Project.objects.filter(Q(team=request.user)).exclude(owner=request.user).order_by('-created_at')[:3]

    combined_projects = recent_owner_projects | recent_team_projects

    recent_tasks = Task.objects.filter(project__in=combined_projects).order_by('-created_at')[:8]
    print(recent_tasks)
    return render(request, 'users/dashboard.html', {
        'recent_owner_projects': recent_owner_projects,
        'recent_team_projects':recent_team_projects,
        'recent_tasks': recent_tasks,
    })

@login_required
def projects_view(request):
    projects = Project.objects.filter(Q(owner=request.user) | Q(team=request.user))
    return render(request, 'projects/projects.html', {'projects': projects})

@login_required
def tasks_view(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/tasks.html', {'tasks': tasks})