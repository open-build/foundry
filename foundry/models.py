from datetime import timedelta
from decimal import Decimal
import uuid

from enum import Enum

from django.db import models
from django.contrib import admin
from django.utils import timezone

from wagtail.core.models import Page

from modelcluster.fields import ParentalKey

from django.contrib.auth.models import User


class HomePage(Page):
    pass

class AboutPage(Page):
    pass

class News(Page):
    pass

class Contact(Page):
    pass

class Status(Enum):
    DRAFT = 'Draft'
    PLANNED = 'Planned'
    STARTED = 'Started'
    FOUND = 'Found'
    CANCELED = 'CANCELED'

STATUS_CHOICES = (
    (Status.DRAFT.value, 'Draft'),
    (Status.PLANNED.value, 'Planned'),
    (Status.STARTED.value, 'Started'),
    (Status.FOUND.value, 'Found'),
    (Status.CANCELED.value, 'CANCELED'),
)

class Foundry(models.Model):
    name = models.CharField(max_length=255, blank=True, help_text="Name your hunt, i.e. The Search for Ops Commander")
    industry = models.CharField(max_length=255, blank=True, help_text="Market or Industry Focus")
    location = models.CharField(max_length=255, blank=True, help_text="Geographic Location of Foundry")
    remote = models.CharField(max_length=255, blank=True, help_text="Remote, In-Office or Hybrid")
    description = models.TextField(blank=True, help_text="Describe in detail the program")
    brief = models.FileField(null=True, blank=True, help_text="Document Upload")
    owner = models.ForeignKey('auth.User',blank=True, null=True, on_delete=models.CASCADE)
    url = models.CharField(max_length=255, null=True, blank=True, help_text="Your GitHub Profile URL")
    status = models.CharField(max_length=255, blank=True, choices=STATUS_CHOICES, help_text="How far along is the Foundry", default="DRAFT")
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        # onsave add create date or update edit date
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Foundry, self).save(*args, **kwargs)


class FoundryAdmin(admin.ModelAdmin):
    list_display = ('name','owner','url','status','create_date','edit_date')
    search_fields = ('name','owner','status')
    list_filter = ('name',)
    display = 'Foundry'


class Company(models.Model):
    foundry = models.ForeignKey(Foundry, null=False, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, blank=True)
    company_profile = models.CharField(max_length=255, blank=True)
    company_url = models.CharField(max_length=255, blank=True)
    company_industry = models.CharField(max_length=255, blank=True)
    elevator_pitch = models.CharField(max_length=255, blank=True)
    pitch_deck = models.FileField(null=True, blank=True, help_text="Document Upload")
    business_plan = models.FileField(null=True, blank=True, help_text="Document Upload")
    status = models.CharField(max_length=255, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        # onsave add create date or update edit date
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Company, self).save(*args, **kwargs)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name','status','create_date','edit_date')
    search_fields = ('foundry__name','status')
    list_filter = ('foundry__name','status')
    display = 'Company Entries'


class ContactMail(models.Model):
    name = models.CharField(max_length=255, blank=True)
    inquiry = models.CharField(max_length=255, blank=True)
    message = models.TextField(blank=True)
    email = models.CharField(max_length=255, blank=True)
    file = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=255, blank=True)
    read = models.BooleanField(default=False)
    spam = models.BooleanField(default=False)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    def clean_email(self):
        original_email = self.cleaned_data.get('email')

        if "@" not in original_email:
            raise ValidationError("Invalid Email address")

        if "." not in original_email:
            raise ValidationError("Invalid Email address")

        return original_email

    def save(self, *args, **kwargs):
        # onsave add create date or update edit date
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(ContactMail, self).save(*args, **kwargs)


class ContactMailAdmin(admin.ModelAdmin):
    list_display = ('name','email','url','read','spam','create_date','edit_date')
    search_fields = ('name','email')
    list_filter = ('name',)
    display = 'Contact Form'