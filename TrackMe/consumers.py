import json
from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone

from projects.models import Project
from users.models import CustomUser

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['user'].id
        self.groups = await self.get_user_project_groups(self.user_id)

        for group in self.groups:
            await self.channel_layer.group_add(group, self.channel_name)

        await self.accept()

        await self.set_user_status(online=True)

    async def disconnect(self, close_code):
        await self.set_user_status(online=False)

        for group in self.groups:
            await self.channel_layer.group_discard(group, self.channel_name)

    async def update_project(self, data):
        project_id = data['project_id']
        await self.update_project_in_db(project_id, data)

        message = {
            'title': 'project_update',
            'body': 'Project has been updated.',
            'project_id': project_id,
            'user': self.user_id
        }
        project_members = await self.get_project_members(project_id)
        for member in project_members:
            if member.is_authenticated:
                await self.channel_layer.group_send(f"user_{member.id}", {
                    'type': 'send_notification',
                    'message': message
                })

    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event['message']))

    async def set_user_status(self, online):
        await self.update_user_status(self.user_id, online)

    @database_sync_to_async
    def update_user_status(self, user_id, online):
        user_profile = CustomUser.objects.get(id=user_id)
        user_profile.status = 'online' if online else 'offline'
        user_profile.last_activity = timezone.now()
        user_profile.save()

    async def get_user_project_groups(self, user_id):
        projects = await self.get_projects_for_user(user_id)
        return [f"project_{project.id}" for project in projects]

    @database_sync_to_async
    def get_projects_for_user(self, user_id):
        return list(Project.objects.filter(team=user_id))

    async def get_project_members(self, project_id):
        project_members = await self.get_members_for_project(project_id)
        return project_members

    @database_sync_to_async
    def get_members_for_project(self, project_id):
        project = Project.objects.get(id=project_id)
        return project.team.all()

    @database_sync_to_async
    def update_project_in_db(self, project_id, data):
        project = Project.objects.get(id=project_id)
        project.save()