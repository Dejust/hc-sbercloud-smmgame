from rest_framework import serializers

from . import models


class UserScopeTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ScoreTransaction
        fields = ['id', 'activity_type', 'score']
