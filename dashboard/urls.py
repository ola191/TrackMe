from django.urls import path

from projects.views import project_create_view, project_list_view, project_detail_view, serve_profile_picture
from tasks.views import task_create_view, task_list_view, task_detail_view
from .views import dashboard_view, projects_view, tasks_view, settings_view

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('projects/', projects_view, name='projects'),
    path('tasks/', tasks_view, name='tasks'),
    path('projects/<int:project_pk>/tasks/list', task_list_view, name='task_list'),
    path('projects/<int:project_pk>/tasks/<int:task_pk>/detail', task_detail_view, name='task_detail'),
    path('projects/create/', project_create_view, name='project_create'),
    path('projects/<int:project_pk>/tasks/create/', task_create_view, name='task_create'),
    path('projects/lists', project_list_view, name='project_list'),
    path('projects/<int:project_pk>/project_detail/', project_detail_view, name='project_detail'),
    path('settings/', settings_view, name='settings'),
    path('profile_pictures/<str:filename>/', serve_profile_picture, name='profile_picture'),
]