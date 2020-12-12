from base64 import b64encode
from hashlib import sha256
from hmac import HMAC
from urllib.parse import urlencode

from django.conf import settings

from rest_framework.permissions import BasePermission


class VkPermission(BasePermission):
    secret = settings.VK_API_TOKEN

    def has_permission(self, request, view):
        query = request.query_params
        vk_subset = dict(sorted(x for x in query.items() if x[0][:3] == "vk_"))
        hash_code = b64encode(HMAC(self.secret.encode(), urlencode(vk_subset, doseq=True).encode(), sha256).digest())
        decoded_hash_code = hash_code.decode('utf-8')[:-1].replace('+', '-').replace('/', '_')
        return query["sign"] == decoded_hash_code
