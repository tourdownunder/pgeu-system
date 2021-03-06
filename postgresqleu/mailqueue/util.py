from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.nonmultipart import MIMENonMultipart
from email.utils import formatdate, formataddr
from email.header import Header
from email import encoders

from postgresqleu.util.context_processors import settings_context

from django.template.loader import get_template

from .models import QueuedMail


def template_to_string(templatename, attrs={}):
    context = {}
    context.update(attrs)
    context.update(settings_context())
    return get_template(templatename).render(context)


def send_template_mail(sender, receiver, subject, templatename, templateattr={}, attachments=None, bcc=None, sendername=None, receivername=None, suppress_auto_replies=True, is_auto_reply=False):
    send_simple_mail(sender, receiver, subject,
                     template_to_string(templatename, templateattr),
                     attachments, bcc, sendername, receivername,
                     suppress_auto_replies, is_auto_reply)


def _encoded_email_header(name, email):
    if name:
        return formataddr((str(Header(name, 'utf-8')), email))
    return email


def send_simple_mail(sender, receiver, subject, msgtxt, attachments=None, bcc=None, sendername=None, receivername=None, suppress_auto_replies=True, is_auto_reply=False):
    # attachment format, each is a tuple of (name, mimetype,contents)
    # content should be *binary* and not base64 encoded, since we need to
    # use the base64 routines from the email library to get a properly
    # formatted output message
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['To'] = _encoded_email_header(receivername, receiver)
    msg['From'] = _encoded_email_header(sendername, sender)
    msg['Date'] = formatdate(localtime=True)
    if suppress_auto_replies:
        # Do our best to set some headers to indicate that auto-replies like out of office
        # messages should not be sent to this email.
        msg['X-Auto-Response-Suppress'] = 'All'
        if is_auto_reply:
            msg['Auto-Submitted'] = 'auto-replied'
        else:
            msg['Auto-Submitted'] = 'auto-generated'

    msg.attach(MIMEText(msgtxt, _charset='utf-8'))

    if attachments:
        for filename, contenttype, content in attachments:
            main, sub = contenttype.split('/')
            part = MIMENonMultipart(main, sub)
            part.set_payload(content)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % filename)
            encoders.encode_base64(part)
            msg.attach(part)

    # Just write it to the queue, so it will be transactionally rolled back
    QueuedMail(sender=sender, receiver=receiver, subject=subject, fullmsg=msg.as_string()).save()
    # Any bcc is just entered as a separate email
    if bcc:
        if type(bcc) is list or type(bcc) is tuple:
            bcc = set(bcc)
        else:
            bcc = set((bcc, ))

        for b in bcc:
            QueuedMail(sender=sender, receiver=b, subject=subject, fullmsg=msg.as_string()).save()


def send_mail(sender, receiver, subject, fullmsg):
    # Send an email, prepared as the full MIME encoded mail already
    QueuedMail(sender=sender, receiver=receiver, subject=subject, fullmsg=fullmsg).save()
