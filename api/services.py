from django.db.models import Sum


def aggregate_user_rate(queryset):
    return queryset.aggregate(score=Sum('score'))


def aggregate_all_user_rates(queryset):
    return queryset.values('user_id').annotate(total_scores=Sum('score')).order_by('total_scores')