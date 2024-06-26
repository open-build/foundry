from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import View
from django.shortcuts import redirect


from .models import Company, Foundry
from .models import StartupApplication, EvaluationScores
from .forms import CompanyForm, StartupApplicationForm, FounderSignUpForm
import requests

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

import json
from django.conf import settings

def preprocess_application_data(application):
    """
    Preprocess the application data to create a comprehensive summary text.
    Adjust the details as per your model's requirements.
    """
    details = [
        application.business_description,
        f"Legal Structure: {application.legal_structure}",
        f"Ownership Structure: {application.ownership_structure}",
        f"Annual Revenue: {application.annual_revenue}",
        f"Funding Amount: {application.funding_amount}",
        f"Outstanding Debt: {application.outstanding_debt}",
        f"Development Stage: {application.development_stage}",
        application.market_demand_proof,
        application.marketing_strategy,
        application.competitive_advantage,
        # Add more fields as necessary
    ]
    return " ".join(details)

import openai

def evaluate_startup_idea(application):
    """
    Evaluate the detailed startup application using ChatGPT for scoring based on specific criteria.
    """
    openai.api_key = settings.OPENAI_API_KEY

    # Define the application summary from preprocess_application_data
    application_summary = preprocess_application_data(application)

    # Generate the review using ChatGPT
    response = openai.Completion.create(
        engine="davinci", 
        prompt=application_summary + "\nCriteria:\n1. Originality\n2. Marketability\n3. Feasibility\n4. Completeness\nScore:",
        max_tokens=50
    )

    # Extract scores from the response
    if response.choices[0].text:
        review_text = response.choices[0].text
    else:
        review_text = "AI Failed to Summarize the Application. Please review manually."
    originality_score = float(review_text.split('\n')[1].split(':')[-1])
    marketability_score = float(review_text.split('\n')[2].split(':')[-1])
    feasibility_score = float(review_text.split('\n')[3].split(':')[-1])
    completeness_score = float(review_text.split('\n')[4].split(':')[-1])

    # Save evaluation scores
    EvaluationScores.objects.create(
        startup_application=application,
        summary=review_text,
        originality_score=originality_score,
        marketability_score=marketability_score,
        feasibility_score=feasibility_score,
        completeness_score=completeness_score
    )
    
    return review_text, originality_score, marketability_score, feasibility_score, completeness_score


import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email_notification(to_email):
    message = Mail(
        from_email='foundry@buildly.io',
        to_emails=to_email,
        subject='Buildly Foundry Submission Notification',
        html_content='<strong>Thank you for submitting your startup to the Buildly and First City Foundry</strong>')
    
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))


def startup_application(request):

    if request.method == 'POST':
        form = StartupApplicationForm(request.POST)
        if form.is_valid():
            # Save form data here for each step
            # Redirect to the next step or completion page
            form = form.save()
             # Send email notification
            emails = form.contact_email + 'team@buildly.io' 
            send_email_notification(emails)  # Assuming 'email' is the field in your form containing the recipient's email address
            return redirect('startup_application')
            messages.success(request, 'Success, your Foundry application was Submitted!')
    else:
        form =  StartupApplicationForm()

    return render(request, 'startup_application.html', {'form': form})


@login_required
def founder_signup(request):
    if request.user.is_founder:
        raise PermissionDenied

    if request.method == 'POST':
        form = FounderSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/login/')
    else:
        form = FounderSignUpForm()

    return render(request, 'founder_signup.html', {'form': form})

class MyView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'


def homepage(request):
    """View function for home page of site."""

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'home_page.html')


@login_required(login_url='/')
def dashboard(request,pk):

    getReport = Company.objects.all().filter(id=pk)

    return render(request, 'dashboard.html', {'getReport': getReport, })


@login_required(login_url='/')
def report(request,pk):

    getReport = Company.objects.all().filter(id=pk)

    return render(request, 'report.html', {'getReport': getReport, 'id': pk})


class CompanyList(ListView,LoginRequiredMixin):
    """
    Monitored Sites
    """
    model = Company
    template_name = 'company_list.html'

    def get(self, request, *args, **kwargs):

        getHunts = Company.objects.all().filter(foundry=request.foundry)

        return render(request, self.template_name, {'getHunts': getHunts,})

class CompanyCreate(CreateView):
    """
    Montior for sites creation
    """
    model = Company
    template_name = 'company_form.html'
    #pre-populate parts of the form
    def get_initial(self):
        initial = {
            'user': self.request.user,
            }

        return initial

    def get_form_kwargs(self):
        kwargs = super(CompanyCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()
        messages.success(self.request, 'Success, Monitored Site Created!')
        return redirect('/companys/')

    form_class = CompanyForm


class CompanyUpdate(UpdateView,LoginRequiredMixin,):
    """
    Update and Edit Montiored Site.
    """
    model = Company
    template_name = 'company_form.html'
    form_class = CompanyForm

    def get_form_kwargs(self):
        kwargs = super(CompanyUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return render(self.get_context_data(form=form))

    def form_valid(self, form):
        form.instance.url = form.instance.url.replace("http://","")
        form.instance.url = form.instance.url.replace("https://","")
        form.save()
        messages.success(self.request, 'Success, Monitored Site Updated!')

        return redirect('/companys/')


class CompanyDelete(DeleteView,LoginRequiredMixin,):
    """
    Delete a MontiorSite
    """
    model = Company

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return render(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()
        messages.success(self.request, 'Success, Montior Site Deleted!')
        return redirect('/companys/')
