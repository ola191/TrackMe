from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task, Comment
from .forms import TaskForm, CommentForm
from projects.models import Project

@login_required
def task_list_view(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    tasks = Task.objects.filter(project=project)
    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'project': project})

@login_required
def task_create_view(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, project=project)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('task_list', project_pk=project.pk)
    else:
        form = TaskForm(project=project)
    return render(request, 'tasks/task_create.html', {'form': form, 'project': project})

@login_required
def task_detail_view(request, project_pk, task_pk):
    task = get_object_or_404(Task, pk=task_pk)
    comments = task.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
            return redirect('task_detail', pk=task.pk)
    else:
        comment_form = CommentForm()
    return render(request, 'tasks/task_detail.html', {'task': task, 'comments': comments, 'comment_form': comment_form, 'project_pk': project_pk})
