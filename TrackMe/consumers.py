import json
from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone

from projects.models import Project
from users.models import CustomUser

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
       pass

    async def disconnect(self, close_code):
        pass

    async def update_project(self, data):
        pass

    async def send_notification(self, event):
        pass

    async def set_user_status(self, online):
        pass

    @database_sync_to_async
    def update_user_status(self, user_id, online):
        pass

    async def get_user_project_groups(self, user_id):
        pass

    @database_sync_to_async
    def get_projects_for_user(self, user_id):
        pass

    async def get_project_members(self, project_id):
        pass

    @database_sync_to_async
    def get_members_for_project(self, project_id):
        pass

    @database_sync_to_async
    def update_project_in_db(self, project_id, data):
        pass