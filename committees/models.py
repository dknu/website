from ckeditor.fields import RichTextField
from django.contrib.auth.models import Group, User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_delete
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from smart_selects.db_fields import ChainedForeignKey
from sorl.thumbnail import ImageField


class Committee(Group):
    # Har name fra superklassen
    email = models.EmailField(null=True, blank=True)
    image = ImageField(upload_to='komiteer')
    slug = models.SlugField(null=True, blank=True)
    visible = models.BooleanField(default=True)

    one_liner = models.CharField(max_length=30, verbose_name="Lynbeskrivelse")
    header = models.CharField(max_length=150, verbose_name="Overskrift", blank=True, null=True)
    description = RichTextField(verbose_name='Beskrivelse', config_name='committees')

    parent = models.ForeignKey('Committee', null=True, blank=True, related_name="subcommittees")
    admins = models.ManyToManyField(User)
    # Har Many2ManyField til Permission i superklasse

    class Meta:
        permissions = (
            ("can_edit_committees", "Can edit all committees"),
            ("committee_admin", "Can edit this committee and parent committee."),
        )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('verv:view', kwargs={'slug':self.slug})

    def add_user(self, user):
        if user not in self.user_set.all():
            self.user_set.add(user)
            self.save()
            if self.parent is not None:
                self.parent.add_user(user)

    def remove_user(self, user):
        if user in self.user_set.all():
            self.user_set.remove(user)
            self.save()
            for subcommittee in self.subcommittees.all():
                subcommittee.remove_user(user)


class Position(Group):
    title = models.CharField(max_length=100, verbose_name="Stillingstittel")
    email = models.EmailField(null=True, blank=True, verbose_name="Epost")
    pos_in_committee = models.ForeignKey(Committee, null=False)
    usr = models.ForeignKey(User, null=False)
    # permission_group = models.ForeignKey(Group)

    def __str__(self):
        return str(self.title)
