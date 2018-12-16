from django.db.models import Q

from postgresqleu.util.backendlookups import LookupBase
from postgresqleu.confreg.models import Conference, ConferenceRegistration, Speaker


class RegisteredUsersLookup(LookupBase):
    @property
    def url(self):
        return '/events/admin/{0}/lookups/regs/'.format(self.conference.urlname)

    @property
    def label_from_instance(self):
        return lambda x: u'{0} <{1}>'.format(x.fullname, x.email)

    @classmethod
    def get_values(self, query, conference):
        return [{'id': r.id, 'value': r.fullname}
                for r in ConferenceRegistration.objects.filter(
                    conference=conference,
                    payconfirmedat__isnull=False).filter(
                        Q(firstname__icontains=query) | Q(lastname__icontains=query) | Q(email__icontains=query)
                    )[:30]]


class SpeakerLookup(LookupBase):
    @property
    def url(self):
        return '/events/admin/lookups/speakers/'

    @property
    def label_from_instance(self):
        return lambda x: u"%s (%s)" % (x.fullname, x.user.username)

    @classmethod
    def get_values(self, query):
        return [
            {'id': s.id,
             'value': u"%s (%s)" % (s.fullname, s.user.username if s.user else '')
            }
            for s in Speaker.objects.filter(
                Q(fullname__icontains=query) | Q(twittername__icontains=query) | Q(user__username__icontains=query)
            )[:30]
        ]
