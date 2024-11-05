from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    STATUS_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('busy', 'Busy'),
        ('away', 'Away'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='offline')

    def __str__(self):
        return self.username

    def send_friend_request(self, to_user):
        if not Friendship.objects.filter(from_user=self, to_user=to_user).exists():
            Friendship.objects.create(from_user=self, to_user=to_user, status='requested')

    def accept_friend_request(self, from_user):
        friendship = Friendship.objects.filter(from_user=from_user, to_user=self, status='requested').first()
        if friendship:
            friendship.status = 'accepted'
            friendship.save()

    def decline_friend_request(self, from_user):
        friendship = Friendship.objects.filter(from_user=from_user, to_user=self, status='requested').first()
        if friendship:
            friendship.status = 'declined'
            friendship.save()

    def block_user(self, to_user):
        Friendship.objects.update_or_create(
            from_user=self,
            to_user=to_user,
            defaults={'status': 'blocked'}
        )

    def is_friend(self, other_user):
        return Friendship.objects.filter(
            from_user=self, to_user=other_user, status='accepted'
        ).exists() or Friendship.objects.filter(
            from_user=other_user, to_user=self, status='accepted'
        ).exists()

class Friendship(models.Model):
    STATUS_CHOICES = [
        ('requested', gettext_lazy('Requested')),
        ('accepted', gettext_lazy('Accepted')),
        ('declined', gettext_lazy('Declined')),
        ('blocked', gettext_lazy('Blocked')),
    ]

    from_user = models.ForeignKey(CustomUser, related_name='sent_friend_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, related_name='received_friend_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='requested')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user} -> {self.to_user} ({self.status})"