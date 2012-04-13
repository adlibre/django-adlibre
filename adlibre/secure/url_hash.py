import hashlib

from django.conf import settings


def get_hash(input, method='md5', salt=settings.SECRET_KEY):
    """

    Creates a secure hash associated with an object. That can be used for URL tokenization in lieu of session auth.

    Usage:

    in models.py
        ...
            @property
            def url_hash(self):
                from adlibre.secure.url_hash import get_hash
                return get_hash(self.id)[:8]
        ...

    in urls.py
        ...
        url(r'^account/invoice/(?P<invoice_hash>[\-\d\w]+)/(?P<invoice_id>[\-\d]+)$', 'show_invoice', name='show_invoice'),
        ...

    in views.py
        ...
        i = get_object_or_404(Invoice, id=invoice_id,)

        if i.url_hash != invoice_hash:
            raise Http404
        ...

    """
    h = hashlib.new(method)
    h.update(str(input))
    h.update(salt)
    return h.hexdigest()
