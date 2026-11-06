from django.db import models
from django.contrib.auth.models import User


class UserStudyProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    study_streak = models.PositiveIntegerField(default=0)
    total_sessions = models.PositiveIntegerField(default=0)
    last_active = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class TopicExplanation(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    topic = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=30)
    summary = models.TextField(blank=True)
    explanation = models.TextField(blank=True)
    code_example = models.TextField(blank=True)
    key_takeaways = models.TextField(blank=True)
    interview_tips = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic


class InterviewQuestionSet(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    subject = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=30)
    question_count = models.PositiveIntegerField(default=5)
    questions = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class Quiz(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    topic = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=30)
    questions = models.JSONField(default=list)
    user_answers = models.JSONField(default=dict)
    score = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    percentage = models.FloatField(default=0)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


class ChatMessage(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"