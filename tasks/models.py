from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=255)
    due_date = models.DateField()
    importance = models.IntegerField()  # 1-10
    estimated_hours = models.IntegerField()
    dependencies = models.JSONField(default=list, blank=True)  # List of task IDs

    def __str__(self):
        return self.title
