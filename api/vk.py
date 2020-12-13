import vk
from django.conf import settings


session = vk.Session(access_token=settings.VK_SERVICE_TOKEN)
api = vk.API(session)


def get_users(user_ids):
    users = api.users.get(user_ids=user_ids, fields='photo_200', v='5.126')

    return {
        user['id']: {
            'first_name': user['first_name'] if user['first_name'] != 'DELETED' else '—',
            'last_name': user['last_name'],
            'photo_200': user.get('photo_200', None)
        }
        for user in users
    }
