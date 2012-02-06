import hashlib

from django.conf import settings


def get_hash(input, method='md5', salt=settings.SECRET_KEY):
    h = hashlib.new(method)
    h.update(str(input))
    h.update(salt)
    return h.hexdigest()
