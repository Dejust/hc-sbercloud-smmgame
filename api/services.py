from django.db.models import Sum, functions


def aggregate_user_rate(queryset):
    return queryset.aggregate(score=functions.Coalesce(Sum('score'), 0))


def aggregate_all_user_rates(queryset, limit=3):
    return queryset.values('user_id').annotate(total_scores=Sum('score')).order_by('-total_scores')[:limit]


def get_achievements(queryset):
    achievements = []
    return achievements
