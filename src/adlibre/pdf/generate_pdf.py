### xhtml2pdf requirements
import cStringIO as StringIO
import cgi
import os
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import RequestContext
from django.conf import settings
import xhtml2pdf.pisa as pisa
##


def generate_pdf(template, context):

    html  = render_to_string(template, context, )
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), dest=result, link_callback=fetch_resources )

    if not pdf.err:
        return result.getvalue()
    raise Exception('PDF Generation Failed!')


def fetch_resources(uri, rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    return path
