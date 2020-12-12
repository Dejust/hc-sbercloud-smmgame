
from django.db import models
from django.utils import timezone


class ScoreTransaction(models.Model):
    ACTIVITIES = [
        ('like', 'like'),
        ('comment', 'comment')
    ]

    user_id = models.IntegerField()
    group_id = models.IntegerField()
    activity_type = models.CharField(max_length=20, choices=ACTIVITIES)
    score = models.IntegerField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)


class GroupSettings(models.Model):
    group_id = models.IntegerField()
    score_by_likes = models.IntegerField()
    score_by_comments = models.IntegerField()
