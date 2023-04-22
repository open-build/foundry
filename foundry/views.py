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
from .forms import CompanyForm
import requests

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

class CompanyCreate(CreateView,LoginRequiredMixin,):
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
