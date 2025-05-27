from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from datetime import timedelta

User = get_user_model()

class Task(models.Model):
    STATUS_CHOICES = (
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('closed', 'Closed')
    )
    URGENCY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )

    project = models.ForeignKey('projects.Project', on_delete=models.PROTECT, related_name='tasks')
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='medium')
    responsible = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    @property
    def elapsed_time(self):
        total = timedelta()
        for ts in self.time_sessions.all():
            total += ts.duration or timedelta()
        return total

    @property
    def elapsed_time_display(self):
        total = self.elapsed_time
        hours = total.total_seconds() // 3600
        minutes = (total.total_seconds() % 3600) // 60
        return f"{int(hours)}h {int(minutes)}m"

    @property
    def active_session(self):
        return self.time_sessions.filter(stopped_at__isnull=True).first()

    @property
    def can_start_or_stop(self):
        return self.status != 'closed'  # customize based on status if needed

    @property
    def can_be_closed(self):
        return not self.time_sessions.filter(stopped_at__isnull=True).exists() and self.status != 'closed'

    def has_sessions(self):
        return self.time_sessions.exists()
    
    @property
    def status_color(self):
        status_colors = {
            'todo': 'secondary',
            'in_progress': 'primary',
            'done': 'success'
        }
        return status_colors.get(self.status, 'secondary')

    @property
    def urgency_color(self):
        urgency_colors = {
            'low': 'info',
            'medium': 'warning',
            'high': 'danger'
        }
        return urgency_colors.get(self.urgency, 'secondary')
    
    @classmethod
    def get_active_session_for_user(cls, user):
        """Returns the active task session for a user, if any"""
        active_task = cls.objects.filter(
            time_sessions__user=user,
            time_sessions__stopped_at__isnull=True
        ).first()
        return active_task
    
    def close_task(self):
        """Closes the task if possible"""
        if self.status == 'closed':
            raise ValueError("Task already closed")
        
        if self.time_sessions.filter(stopped_at__isnull=True).exists():
            raise ValueError("Cannot close task with active sessions")
        
        self.status = 'closed'
        self.closed_at = now()
        self.save()

        return {
            'success': True,
            'message': f"Task {self.id} closed successfully"
        }

class TimeSession(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='time_sessions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    started_at = models.DateTimeField()
    stopped_at = models.DateTimeField(null=True, blank=True)
    billed = models.BooleanField(default=False)

    @property
    def duration(self):
        if not self.stopped_at:
            return now() - self.started_at
        return self.stopped_at - self.started_at