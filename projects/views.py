from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm

@login_required
def project_list_view(request):
    projects = Project.objects.filter(owner=request.user)
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
    return render(request, 'projects/project_detail.html', {'project': project})
