from django_components import component

from projects.models import Project

@component.register("projects")
class ProjectListComponent(component.Component):
    template_name = "projects/comp-projects.html"

    def get_context_data(self, **kwargs):
        projects = Project.objects.all()
        return {
            "projects": projects
        }