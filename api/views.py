from django.db.models import Sum

from rest_framework import generics
from rest_framework.filters import SearchFilter

from rest_framework.response import Response

from . import models
from . import serializers
from . import services


class HistoryApiView(generics.ListAPIView):
    queryset = models.ScoreTransaction.objects.all()
    serializer_class = serializers.UserScopeTransactionSerializer

    def get_queryset(self):
        if self.request.query_params.get('vk_user_id'):
            return self.queryset.filter(user_id=self.request.query_params['vk_user_id'])

        elif self.request.query_params.get('vk_group_id'):
            return self.queryset.filter(group_id=self.request.query_params['vk_group_id'])

        return self.queryset.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({'verify': True, 'data': serializer.data})


class ScoreApiView(generics.ListAPIView):
    queryset = models.ScoreTransaction.objects.all()

    def get_queryset(self):
        if self.request.query_params.get('vk_user_id'):
            return self.queryset.filter(user_id=self.request.query_params['vk_user_id'])
        return self.queryset

    def list(self, request, *args, **kwargs):
        data = services.aggregate_user_rate(self.get_queryset())
        return Response({'verify': True, 'data': data})


class RatesApiView(generics.ListAPIView):
    queryset = models.ScoreTransaction.objects.all()

    def get(self, request, *args, **kwargs):
        # rates and user
        data = services.aggregate_all_user_rates(self.get_queryset())
        return Response({'verify': True, 'data': data})


class SettingsApiView(generics.RetrieveUpdateAPIView):
    queryset = models.GroupSettings.objects.all()
