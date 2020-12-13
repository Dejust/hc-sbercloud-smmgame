from rest_framework import serializers

from . import models


class UserScopeTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ScoreTransaction
        fields = ['id', 'user_id', 'activity_type', 'score']


class GroupSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GroupSettings
        fields = ['group_id', 'score_by_likes', 'score_by_comments']
