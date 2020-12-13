
from django.urls import path

from . import views


urlpatterns = [
    path('history', views.HistoryApiView.as_view()),
    path('score', views.ScoreApiView.as_view()),
    path('rates', views.RatesApiView.as_view()),
    path('settings', views.SettingsApiView.as_view())
]
