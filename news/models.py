from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from django.contrib.auth.admin import User
from files.models import Image
import re

class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    main_content = RichTextUploadingField(blank=True)
    ingress_content = RichTextUploadingField(blank=True)

    internal = models.BooleanField(default=False, verbose_name='Intern')
    pub_date = models.DateTimeField('Publication date', default=timezone.now)
    thumbnail = models.ForeignKey(Image, on_delete=models.SET_NULL, blank=True, null=True)
    redirect = models.IntegerField('Redirect', default=0)

    def __str__(self):
        return self.title

    @staticmethod
    def get_class():
        return "Article"

    class Meta:
        app_label = 'news'
        ordering = ('-pub_date',)

    def redirect_id(self):
        if self.redirect:
            return self.redirect
        return self.id


class Event(models.Model):
    title = models.CharField(max_length=100, verbose_name='Tittel')
    main_content = RichTextUploadingField(blank=True, verbose_name='Artikkel')
    ingress_content = RichTextUploadingField(blank=True, verbose_name='Ingress')
    pub_date = models.DateTimeField(default=timezone.now, verbose_name='Publiseringsdato')
    thumbnail = models.ForeignKey(Image, on_delete=models.SET_NULL, blank=True, null=True, )

    internal = models.BooleanField(default=False, verbose_name='Intern')
    registration = models.BooleanField(default=False, verbose_name='Påmelding')
    max_limit = models.PositiveIntegerField(blank=True, null=True, default=0, verbose_name='Max påmeldte')
    registration_start = models.DateTimeField(default=timezone.now, verbose_name='Registrering start')
    deregistration_end = models.DateTimeField(default=timezone.now, verbose_name='Avregistrering slutt')
    external_registration = models.CharField(max_length=200, default='', verbose_name='Ekstern påmelding url', blank=True, null=True)

    time_start = models.DateTimeField(verbose_name='Start tidspunkt')
    time_end = models.DateTimeField(verbose_name='Slutt tidspunkt')
    place = models.CharField(max_length=100, blank=True, verbose_name='Sted')
    place_href = models.CharField(max_length=200, blank=True, verbose_name='Sted URL')

    def __str__(self):
        return self.title

    @staticmethod
    def get_class():
        return "Event"

    def registered_count(self):
        return min(self.max_limit, len(EventRegistration.objects.filter(event=self)))

    def is_registered(self, user):
        if user in [er.user for er in EventRegistration.objects.filter(event=self).order_by('date')][:self.max_limit]:
            return True
        return False

    def is_waiting(self, user):
        if user in [er.user for er in EventRegistration.objects.filter(event=self).order_by('date')][self.max_limit:]:
            return True
        return False

    def userstatus(self, user):
        if self.is_registered(user): return "Påmeldt"
        if self.is_waiting(user): return "Venteliste"
        return "Ikke påmeldt"

    def registered_percentage(self):
        if self.max_limit:
            return round(self.registered_count() / self.max_limit * 100)
        else:
            return 100

    def registered_list(self):
        return sorted([("%s %s" % (er.user.first_name, er.user.last_name), er.username()) for er in EventRegistration.objects.filter(event=self).order_by('date')][:self.max_limit])

    def register_email(self):
        return ''.join(sorted([er.user.email + '; ' if er.user.email else '' for er in EventRegistration.objects.filter(event=self).order_by('date')][:self.max_limit]))

    def waitlist_email(self):
        return ''.join(sorted([er.user.email + '; ' if er.user.email else '' for er in EventRegistration.objects.filter(event=self).order_by('date')][self.max_limit:]))

    def attending_usernames(self):
        return [er.username() for er in EventRegistration.objects.filter(event=self, attended=True).order_by('date')]

    def wait_list(self):
        return [(a[0]+1, a[1][0], a[1][1]) for a in enumerate([("%s %s" % (er.user.first_name, er.user.last_name), er.username()) for er in EventRegistration.objects.filter(event=self).order_by('date')][self.max_limit:])]

    def registration_button_status(self, user):
        now = timezone.now()
        try:
            er = EventRegistration.objects.get(user=user, event=self)
            if self.deregistration_end > now:
                return True, True
        except EventRegistration.DoesNotExist:
            if now > self.registration_start and self.time_end > now:
                return False, True
        return False, False


    def attended(self, user, status):
        try:
            er = EventRegistration.objects.get(event=self, user=user)
            er.attended = status
            er.save()
            return True
        except EventRegistration.DoesNotExist:
            return False


    class Meta:
        app_label = 'news'
        ordering = ("-time_start",)


class Upload(models.Model):
    title = models.CharField(max_length=100, verbose_name='Filnavn')
    time = models.DateTimeField(default=timezone.now, verbose_name='Tittel')
    file = models.FileField(upload_to='uploads')
    number = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'news'


class EventRegistration(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    date = models.DateTimeField(default=timezone.now, verbose_name="Registration time")
    attended = models.BooleanField(default=False)

    def username(self):
        return self.user.username

    def name(self):
        return self.user.first_name.capitalize() + " " + self.user.last_name.capitalize()

    def __str__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)
