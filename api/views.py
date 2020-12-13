
from rest_framework import generics
from rest_framework.response import Response

from . import models
from . import permissions
from . import serializers
from . import services


class HistoryApiView(generics.ListAPIView):
    queryset = models.ScoreTransaction.objects.all()
    serializer_class = serializers.UserScopeTransactionSerializer
    permission_classes = [permissions.VkPermission]

    def get_queryset(self):
        if self.request.query_params.get('user_id'):
            return self.queryset.filter(user_id=self.request.query_params['user_id'])

        elif self.request.query_params.get('vk_group_id'):
            return self.queryset.filter(group_id=self.request.query_params['vk_group_id'])

        return self.queryset.none()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ScoreApiView(generics.ListAPIView):
    queryset = models.ScoreTransaction.objects.all()
    permission_classes = [permissions.VkPermission]

    def get_queryset(self):
        if self.request.query_params.get('user_id'):
            return self.queryset.filter(user_id=self.request.query_params['user_id'])
        return self.queryset

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
    permission_classes = [permissions.VkPermission]
    serializer_class = serializers.GroupSettingsSerializer
    lookup_field = 'group_id'

    def get_object(self):
        self.kwargs['group_id'] = self.request.query_params.get('group_id')
        return super(SettingsApiView, self).get_object()
