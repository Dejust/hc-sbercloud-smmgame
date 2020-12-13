
from rest_framework import generics
from rest_framework.response import Response

from . import models
from . import permissions
from . import serializers
from . import services


class BaseHistoryApiView(generics.ListAPIView):
    queryset = models.ScoreTransaction.objects.all()
    serializer_class = serializers.UserScopeTransactionSerializer
    permission_classes = [permissions.VkPermission]
    lookup_param, lookup_model = None, None

    def get_queryset(self):
        value = self.request.query_params.get(self.lookup_param)
        if value:
            return self.queryset.filter(**{self.lookup_model: value})

        return self.queryset.none()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserHistoryApiView(BaseHistoryApiView):
    lookup_param, lookup_model = 'vk_user_id', 'user_id'


class GroupHistoryApiView(BaseHistoryApiView):
    lookup_param, lookup_model = 'vk_group_id', 'group_id'


class ScoreApiView(generics.ListAPIView):
    queryset = models.ScoreTransaction.objects.all()
    permission_classes = [permissions.VkPermission]

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id') or self.request.query_params.get('vk_user_id')
        if user_id:
            return self.queryset.filter(user_id=user_id)
        return self.queryset.none()

    def list(self, request, *args, **kwargs):
        data = services.aggregate_user_rate(self.get_queryset())
        return Response(data)


class RatesApiView(generics.ListAPIView):
    queryset = models.ScoreTransaction.objects.all()
    permission_classes = [permissions.VkPermission]

    def get(self, request, *args, **kwargs):
        data = services.aggregate_all_user_rates(self.get_queryset())
        return Response(data)


class SettingsApiView(generics.RetrieveAPIView, generics.CreateAPIView):
    queryset = models.GroupSettings.objects.all()
    permission_classes = [permissions.VkPermission, permissions.VKIsAdmin]
    serializer_class = serializers.GroupSettingsSerializer
    lookup_field = 'group_id'

    def get_object(self):
        self.kwargs['group_id'] = self.request.query_params.get('vk_group_id')
        return super(SettingsApiView, self).get_object()


class AchievementsApiView(generics.ListAPIView):
    queryset = models.ScoreTransaction.objects.all()
    permission_classes = [permissions.VkPermission]

    def get_queryset(self):
        user_id = self.request.query_params.get('vk_user_id')
        if user_id:
            return self.queryset.filter(user_id=user_id)
        return self.queryset.none()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = services.get_achievements(queryset)
        return Response(data)


