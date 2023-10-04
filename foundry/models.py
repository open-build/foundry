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
    

class StartupApplication(models.Model):
    LEGAL = [
        ('C Corp', 'C Corp'),
        ('LLC', 'LLC'),
        ('Partnership', 'Partnership'),
        ('Non-Profit', 'Non-Profit'),
        # Add more structure choices as needed
    ]
    STAGE = [
        ('Idea Stage', 'Idea Stage'),
        ('Market Fit', 'Market Fit'),
        ('Proof of Concept', 'Proof of Concept'),
        ('MVP', 'MVP'),
        ('Growth Stage', 'Growth Stage'),
        # Add more structure choices as needed
    ]
    MODEL = [
        ('B2B', 'B2B'),
        ('B2C', 'B2C'),
        ('B2G', 'B2G'),
        ('B2B2C', 'B2B2C'),
        # Add more structure choices as needed
    ]
    # General Information
    company_name = models.CharField(max_length=255)
    business_description = models.TextField()
    legal_structure = models.CharField(max_length=50,choices=LEGAL)
    ownership_structure = models.CharField(max_length=50)
    pitch_deck = models.FileField(null=True, blank=True, help_text="Document Upload")

    # Financial Information
    annual_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    funding_amount = models.DecimalField(max_digits=10, decimal_places=2)
    outstanding_debt = models.DecimalField(max_digits=10, decimal_places=2)

    # Team and Leadership
    founder_names = models.CharField(max_length=255)
    team_members = models.TextField(null=True, blank=True, help_text="If you have employees on payroll list them here")
    advisors_mentors = models.TextField(null=True, blank=True)

    # Market Research
    target_audience = models.TextField(help_text="Primary and Secondary Markets")
    competition_analysis = models.TextField(help_text="List your closest Competitors")
    market_demand_proof = models.TextField(help_text="Any research, surveys or signups you have summarize them here")
    marketing_strategy = models.TextField(help_text="Your marketing plans other then paid advertising")

    # Product/Service Development
    development_stage = models.CharField(max_length=50,choices=STAGE)
    intellectual_property = models.TextField(help_text="What IP have your registered or plan to register")

    # Customer Base
    customer_base = models.TextField(help_text="Have you Identified your Users or Personas")
    customer_acquisition_strategy = models.TextField(help_text="What is your plan to get them to pay for/use your product")

    # Funding and Investment
    current_funding_sources = models.TextField()
    future_funding_plans = models.TextField()

    # Legal and Compliance
    regulatory_compliance = models.TextField(null=True, blank=True, help_text="Any Government or other compliance issues you need to address")
    legal_issues = models.TextField(null=True, blank=True, help_text="What if/any possible legal or regulatory issues have you identified")

    # Scalability and Growth Potential
    scalability = models.TextField(help_text="How well will your product scale")
    expansion_plans = models.TextField(null=True, blank=True, help_text="How do you plan to grow and expand")

    # Social Impact (if applicable)
    social_impact = models.TextField(blank=True, null=True, help_text="Do you have a social mission or see a positive social impact with your product")

    # Business Model
    revenue_model = models.CharField(max_length=50,choices=MODEL)
    pricing_strategy = models.TextField()

    # Competitive Advantage
    competitive_advantage = models.TextField()

    # Milestones and Achievements
    milestones_achievements = models.TextField(help_text="List Milestones/Acheivments so far for your Product")

    # References and Recommendations
    references_recommendations = models.TextField(null=True, blank=True,help_text="Customer or Investor References")

    # Fit with First City Foundry
    alignment_with_mission = models.TextField(null=True, blank=True)
    support_requested = models.TextField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Startup Application"
        verbose_name_plural = "Startup Applications"

    def __str__(self):
        return self.company_name
    
    
class StartupApplicationAdmin(admin.ModelAdmin):
    list_display = ('company_name','created_at')
    search_fields = ('company_name','created_at')
    list_filter = ('company_name',)
    display = 'Startup Form'

class ComparableCompany(models.Model):
    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    description = models.TextField()

    startups = models.ManyToManyField(StartupApplication, related_name="comparable_companies")

    class Meta:
        verbose_name = "Comparable Company"
        verbose_name_plural = "Comparable Companies"

    def __str__(self):
        return self.name

class SuccessData(models.Model):
    comparable_company = models.OneToOneField(ComparableCompany, on_delete=models.CASCADE)
    revenue = models.DecimalField(max_digits=10, decimal_places=2)
    employee_count = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Success Data"
        verbose_name_plural = "Success Data"

    def __str__(self):
        return f"Success Data for {self.comparable_company.name}"
