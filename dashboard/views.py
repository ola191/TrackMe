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

    new_notifications = [
        'test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8'
    ]

    return render(request, 'dashboard/dashboard.html', {
        'recent_owner_projects': recent_owner_projects,
        'recent_team_projects':recent_team_projects,
        'recent_tasks': recent_tasks,
        'new_notifications' : new_notifications
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

    return render(request, 'dashboard/settings.html', {'form': form, 'view': 'profile'})

def faq_view(request):
    faq_data = [
        {
            "section_name": "Login",
            "articles": [
                {
                    "title": "Email Change",
                    "description": "Changing your email address is currently unavailable."
                },
                {
                    "title": "Username and Password",
                    "description": "Use new passwords that haven't been used before."
                }
            ]
        },
        {
            "section_name": "Register",
            "articles": [
                {
                    "title": "Email Recovery and Password Reset",
                    "description": "The email recovery and password reset features are currently unavailable."
                },
                {
                    "title": "Password",
                    "description": "Set a new password that hasn't been used before."
                }
            ]
        },
        {
            "section_name": "Dashboard",
            "articles": [
                {
                    "title": "What the Dashboard Displays",
                    "description": "The dashboard shows your latest projects, projects you are part of, and recent tasks."
                }
            ]
        },
        {
            "section_name": "Settings",
            "articles": [
                {
                    "title": "Ability to Change Data",
                    "description": "Data that is view-only is grayed out; other data can be modified normally."
                }
            ]
        },
        {
            "section_name": "Other",
            "articles": [
                {
                    "title": "Icons",
                    "description": "A circle with an X indicates no users are available."
                }
            ]
        }
    ]
    return render(request, 'dashboard/faq.html', {"faq" : faq_data})