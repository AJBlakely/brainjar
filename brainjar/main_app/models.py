from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    class Status(models.TextChoices):
        NOT_STARTED = 'not_started', 'Not Started'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NOT_STARTED)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topics')
    tags = models.ManyToManyField('Tag', blank=True, related_name='topics')

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags')

    class Meta:
        unique_together = [('user', 'name')]
        ordering = ['name']

    def __str__(self):
        return self.name


class Note(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='notes')
    date = models.DateField()
    content = models.TextField()
    reference = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.topic.name} – {self.date}"
