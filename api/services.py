from django.db.models import Sum, functions

count_greet = 'ты совершил {} акивностей, так держать!'

ACHIEVE_COUNT_MAP = [
    {
        'achieve': False,
        'slug': 'first_action',
        'title': 'Первая активность',
        'description': 'Награда за первое действие',
        'check': 1,
        'is_description_visible': False,
    },
    {
        'achieve': False,
        'slug': '10',
        'title': f'В десяточку!',
        'description': count_greet.format(10),
        'check': 10,
        'is_description_visible': False,
    },
    {
        'achieve': False,
        'slug': '100',
        'title': f'Держи соточку, {count_greet.format(100)}',
        'description': count_greet.format(100),
        'check': 100,
        'is_description_visible': False,
    },
    {
        'achieve': False,
        'slug': '1000',
        'title': f'Активист!',
        'check': 1000,
        'description': {count_greet.format(1000)},
        'is_description_visible': False,
    },
    {
        'achieve': False,
        'slug': '10000',
        'title': f'Монстр активности, {count_greet.format(10000)}',
        'check': 10000,
        'description': {count_greet.format(10000)},
        'is_description_visible': False,
    },
]

ACHIEVE_COMMENT_MAP = [
    {
        'achieve': False,
        'slug': 'hikka',
        'title': 'Я не хикка',
        'description': 'Награда за первое сообщение',
        'check': 1,
        'is_description_visible': False,
    },
    {
        'achieve': False,
        'slug': 'owl',
        'title': 'Приветливая сова',
        'description': 'Награда за 100 сообщений',
        'check': 10,
        'is_description_visible': False,
    },
]

ACHIEVE_LIKE_MAP = [
    {
        'achieve': False,
        'slug': 'snake',
        'title': 'Змея игрунья',
        'description': 'Награда за 10 лайков',
        'check': 10,
        'is_description_visible': False,
    },
]

BONUS_ACHIEVE = {
    'title': 'achieve_hunter',
    'slug': 'hunter',
    'achieve': False,
    'description': 'Охотник за наградами, ты собрал более 5 наград',
    'is_description_visible': False,
}


def aggregate_user_rate(queryset):
    return queryset.aggregate(score=functions.Coalesce(Sum('score'), 0))


def aggregate_all_user_rates(queryset, limit=3):
    return queryset.values('user_id').annotate(total_scores=Sum('score')).order_by('-total_scores')[:limit]


def get_achievements(queryset):
    count = queryset.count()
    comment_count = queryset.filter(activity_type='like').count()
    likes_count = queryset.filter(activity_type='comment').count()

    achievements = [{**a, **{'achieve': a['check'] <= count}} for a in ACHIEVE_COUNT_MAP]
    achievements.extend([{**a, **{'achieve': a['check'] <= comment_count}} for a in ACHIEVE_COMMENT_MAP])
    achievements.extend([{**a, **{'achieve': a['check'] <= likes_count}} for a in ACHIEVE_LIKE_MAP])

    ba = BONUS_ACHIEVE.copy()
    if len(list(filter(lambda x: x['achieve'], achievements))) >= 5:
        ba['achieve'] = True

    achievements.append(BONUS_ACHIEVE)

    return achievements
