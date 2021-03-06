from django.conf import settings
from django.utils import timezone

from postgresqleu.util.time import today_global
from .models import Member, MemberLog, get_config

from datetime import timedelta


class InvoiceProcessor(object):
    can_refund = False
    # Process invoices once they're getting paid
    #
    # In the case of membership, that simply means extending the
    # membership.

    def process_invoice_payment(self, invoice):
        # We'll get the member from the processorid
        try:
            member = Member.objects.get(pk=invoice.processorid)
        except member.DoesNotExist:
            raise Exception("Could not find member id %s for invoice!" % invoice.processorid)

        cfg = get_config()

        # The invoice is paid, so it's no longer active!
        # It'll still be in the archive, of course, but not linked from the
        # membership record.
        member.activeinvoice = None

        # Extend the membership. If already paid to a date in the future,
        # extend from that date. Otherwise, from today.
        if member.paiduntil and member.paiduntil > today_global():
            member.paiduntil = member.paiduntil + timedelta(days=cfg.membership_years * 365)
        else:
            member.paiduntil = today_global() + timedelta(days=cfg.membership_years * 365)
        member.expiry_warning_sent = None

        # If the member isn't already a member, set todays date as the
        # starting date.
        if not member.membersince:
            member.membersince = today_global()

        member.save()

        # Create a log record too, and save it
        MemberLog(member=member, timestamp=timezone.now(), message="Payment for %s years received, membership extended to %s" % (cfg.membership_years, member.paiduntil)).save()

    # Process an invoice being canceled. This means we need to unlink
    # it from the membership.
    def process_invoice_cancellation(self, invoice):
        # We'll get the member from the processorid
        try:
            member = Member.objects.get(pk=invoice.processorid)
        except Member.DoesNotExist:
            raise Exception("Could not find member id %s for invoice!" % invoice.processorid)

        # Just remove the active invoice
        member.activeinvoice = None
        member.save()

    # Return the user to a page showing what happened as a result
    # of their payment. In our case, we just return the user directly
    # to the membership page.
    def get_return_url(self, invoice):
        return "%s/membership/" % settings.SITEBASE

    def get_admin_url(self, invoice):
        try:
            member = Member.objects.get(pk=invoice.processorid)
        except Member.DoesNotExist:
            return None
        return '/admin/membership/members/{0}/'.format(member.pk)
