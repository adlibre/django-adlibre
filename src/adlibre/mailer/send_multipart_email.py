"""
#
# Original Source: http://www.rossp.org/blog/2007/oct/25/easy-multi-part-e-mails-django/
#
# Andrew Cutler: Added Premailer Support & File Attachment Support
#
"""

"""
    # Usage Example:

    from adlibre.mailer.send_multipart_email import send_multipart_mail

    subject = 'test email'
    recipient = 'test@example.com'
    template_context = {}

    send_multipart_mail('project/email/template', template_context, subject, recipient)


"""



def send_multipart_mail(template_name, email_context, subject, recipients, bcc=None,
                        sender=None, files=None, attachments=None, fail_silently=False):
    """
    This function will send a multi-part e-mail with both HTML and
    Text parts.

    template_name must NOT contain an extension. Both HTML (.html) and TEXT
        (.txt) versions must exist, eg 'emails/public_submit' will use both
        public_submit.html and public_submit.txt.

    email_context should be a plain python dictionary. It is applied against
        both the email messages (templates) & the subject.

    subject can be plain text or a Django template string, eg:
        New Job: {{ job.id }} {{ job.title }}

    recipients can be either a string, eg 'a@b.com' or a list, eg:
        ['a@b.com', 'c@d.com']. Type conversion is done if needed.

    sender can be an e-mail, 'Name <email>' or None. If unspecified, the
        DEFAULT_FROM_EMAIL will be used.

    """
    from django.core.mail import EmailMultiAlternatives
    from django.template import loader, Context
    from django.conf import settings
    from django.contrib.sites.models import Site

    from premailer import Premailer

    if not sender:
        sender = settings.DEFAULT_FROM_EMAIL

    context = Context(email_context)

    text_part = loader.get_template('%s.txt' % template_name).render(context)
    html_part = loader.get_template('%s.html' % template_name).render(context)
    subject_part = loader.get_template_from_string(subject).render(context)

    # Render html_part with Premailer
    base_url = 'http://%s' % (Site.objects.get_current().domain)
    pm = Premailer(html_part, include_star_selectors=True, base_url=base_url)
    html_part = pm.transform()

    if type(recipients) != list:
        recipients = [recipients,]

    # attachments = ('invoice.pdf', file_data, 'application/pdf')
    if type(attachments) != list and attachments != None:
        attachments = [attachments,]

    msg = EmailMultiAlternatives(subject_part, text_part, sender, recipients, bcc=bcc, attachments=attachments)
    msg.attach_alternative(html_part, "text/html")

    if files is not None:
        if type(files) != list:
            files = [files,]

        for file in files:
            msg.attach_file(file)

    return msg.send(fail_silently)






