from django.contrib import admin
from django import forms

from postgresqleu.confreg.models import Conference, ConferenceRegistration, RegistrationType
from models import Wikipage, WikipageHistory, WikipageSubscriber


class WikipageAdminForm(forms.ModelForm):
	class Meta:
		model = Wikipage

	def __init__(self, *args, **kwargs):
		super(WikipageAdminForm, self).__init__(*args, **kwargs)
		try:
			self.fields['author'].queryset = ConferenceRegistration.objects.filter(conference=self.instance.conference)
			self.fields['viewer_attendee'].queryset = ConferenceRegistration.objects.filter(conference=self.instance.conference)
			self.fields['editor_attendee'].queryset = ConferenceRegistration.objects.filter(conference=self.instance.conference)

			self.fields['viewer_regtype'].queryset = RegistrationType.objects.filter(conference=self.instance.conference)
			self.fields['editor_regtype'].queryset = RegistrationType.objects.filter(conference=self.instance.conference)
		except Conference.DoesNotExist:
			pass

class WikipageHistoryInline(admin.TabularInline):
	model = WikipageHistory
	readonly_fields = ['author', 'publishedat']
	exclude = ['contents',]
	can_delete = False
	max_num = 0
	extra = 0

class WikipageSubscriberInline(admin.TabularInline):
	model = WikipageSubscriber
	readonly_fields = ['subscriber', ]
	can_delete = True
	max_num = 0
	extra = 0

class WikipageAdmin(admin.ModelAdmin):
	form = WikipageAdminForm
	inlines = [WikipageHistoryInline, WikipageSubscriberInline]
	filter_horizontal = ['viewer_attendee', 'editor_attendee', ]


admin.site.register(Wikipage, WikipageAdmin)