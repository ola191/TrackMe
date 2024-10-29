from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from projects.models import Project
from tasks.models import Task
from users.forms import CustomUserChangeForm


@login_required
def dashboard_view(request):
    recent_owner_projects = Project.objects.filter(Q(owner=request.user)).order_by('-created_at')[:3]
    recent_team_projects = Project.objects.filter(Q(team=request.user)).exclude(owner=request.user).order_by('-created_at')[:3]

    combined_projects = recent_owner_projects | recent_team_projects

    recent_tasks = Task.objects.filter(project__in=combined_projects).order_by('-created_at')[:8]
    print(recent_tasks)
    return render(request, 'dashboard/dashboard.html', {
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

@login_required
def settings_view(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = CustomUserChangeForm(instance=user)

    return render(request, 'dashboard/settings.html', {'form': form})