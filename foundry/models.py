from datetime import timedelta
from decimal import Decimal
import uuid

from enum import Enum

from django.db import models
from django.contrib import admin
from django.utils import timezone

from wagtail.models import Page

from modelcluster.fields import ParentalKey

from django.contrib.auth.models import User
from .util import evaluate_startup_application


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
    competition_analysis = models.TextField(help_text="List your closest Competitors", null=True, blank=True)
    market_demand_proof = models.TextField(help_text="Any research, surveys or signups you have summarize them here", null=True, blank=True)
    marketing_strategy = models.TextField(help_text="Your marketing plans other then paid advertising", null=True, blank=True)

    # Product/Service Development
    development_stage = models.CharField(max_length=50,choices=STAGE)
    intellectual_property = models.TextField(help_text="What IP have your registered or plan to register", null=True, blank=True)

    # Customer Base
    customer_base = models.TextField(help_text="Have you Identified your Users or Personas", null=True, blank=True)
    customer_acquisition_strategy = models.TextField(help_text="What is your plan to get them to pay for/use your product", null=True, blank=True)

    # Funding and Investment
    current_funding_sources = models.TextField()
    future_funding_plans = models.TextField()

    # Legal and Compliance
    regulatory_compliance = models.TextField(null=True, blank=True, help_text="Any Government or other compliance issues you need to address")
    legal_issues = models.TextField(null=True, blank=True, help_text="What if/any possible legal or regulatory issues have you identified")

    # Social Impact (if applicable)
    social_impact = models.TextField(blank=True, null=True, help_text="Do you have a social mission or see a positive social impact with your product")

    # Business Model
    revenue_model = models.CharField(max_length=50,choices=MODEL)
    pricing_strategy = models.TextField(null=True, blank=True)

    # Competitive Advantage
    competitive_advantage = models.TextField(null=True, blank=True)

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

    # Evaluation fields
    originality_score = models.FloatField(default=0.0, null=True, blank=True)
    marketability_score = models.FloatField(default=0.0, null=True, blank=True)
    feasibility_score = models.FloatField(default=0.0, null=True, blank=True)
    completeness_score = models.FloatField(default=0.0, null=True, blank=True)
    summary = models.TextField(blank=True, null=True)

    # Override the save method to include evaluation logic
    def save(self, *args, **kwargs):
        # Convert the instance to a dictionary suitable for analysis
        application_data = {
            'company_name': self.company_name,
            'business_description': self.business_description,
            'legal_structure': self.legal_structure,
            'ownership_structure': self.ownership_structure,
            'annual_revenue': self.annual_revenue,
            'funding_amount': self.funding_amount,
            'outstanding_debt': self.outstanding_debt,
            'development_stage': self.development_stage,
            'market_demand_proof': self.market_demand_proof,
            'marketing_strategy': self.marketing_strategy,
            'competitive_advantage': self.competitive_advantage,
            # Include other relevant fields as needed
        }

        # Assume `analyze_ai_response` is imported and ready to use
        # and it now accepts a dictionary and returns a dictionary with scores and summary
        evaluation_results = evaluate_startup_application(application_data)

        # Update the instance with evaluation results
        self.originality_score = evaluation_results.get('originality_score', 0.0)
        self.marketability_score = evaluation_results.get('marketability_score', 0.0)
        self.feasibility_score = evaluation_results.get('feasibility_score', 0.0)
        self.completeness_score = evaluation_results.get('completeness_score', 0.0)
        self.summary = evaluation_results.get('summary', '')

        super().save(*args, **kwargs)  # Call the "real" save() method.


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
    
# https://cloud.google.com/vertex-ai/docs/generative-ai/learn-resources


class EvaluationScores(models.Model):
    startup_application = models.OneToOneField(StartupApplication, on_delete=models.CASCADE)
    originality_score = models.FloatField()
    marketability_score = models.FloatField()
    feasibility_score = models.FloatField()
    completeness_score = models.FloatField()

    class Meta:
        verbose_name = "Evaluation Scores"
        verbose_name_plural = "Evaluation Scores"

    def __str__(self):
        return self.startup_application

class StartupApplicationAdmin(admin.ModelAdmin):
    list_display = ('startup_application','feasibility_score')
    search_fields = ('startup_application','feasibility_score')
    list_filter = ('startup_application',)
    display = 'Startup AI Scores'