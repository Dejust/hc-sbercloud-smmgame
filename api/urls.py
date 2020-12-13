
from django.urls import path

from . import views


urlpatterns = [
    path('history/user', views.UserHistoryApiView.as_view()),
    path('history/group', views.GroupHistoryApiView.as_view()),
    path('score', views.ScoreApiView.as_view()),
    path('rates', views.RatesApiView.as_view()),
    path('settings', views.SettingsApiView.as_view()),
    path('achivements', views.AchievementsApiView.as_view())
]
