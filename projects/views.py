from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from users.models import CustomUser
from .models import Project
from .forms import ProjectForm, AddTeamMemberForm
from tasks.models import Task

@login_required
def project_list_view(request):
    projects = Project.objects.filter(Q(owner=request.user) | Q(team=request.user))
    return render(request, 'projects/project_list.html', {'projects': projects})

@login_required
def project_create_view(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            form.save_m2m()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'projects/project_create.html', {'form': form})

@login_required
def project_detail_view(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    tasks = Task.objects.filter(project=project)

    if request.method == 'POST':
        if 'add_member' in request.POST:
            form = AddTeamMemberForm(request.POST, project=project)
            if form.is_valid():
                member = form.cleaned_data['member']
                if member not in project.team.all():
                    project.team.add(member)
                    return redirect('project_detail', project_pk=project.pk)
        elif 'remove_member' in request.POST:
            member_id = request.POST.get('member_id')
            member = CustomUser.objects.filter(id=member_id).first()
            if member in project.team.all():
                project.team.remove(member)
            return redirect('project_detail', project_pk=project.pk)
    else:
        form = AddTeamMemberForm(project=project)

    return render(request, 'projects/project_detail.html', {'project': project, 'tasks': tasks, 'form': form})
