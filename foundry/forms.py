from .models import Company
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from crispy_forms.layout import Layout, Submit, Reset
from functools import partial
from django import forms
from django.urls import reverse

from django import forms
from django.forms import formset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import StartupApplication

class StartupApplicationForm(forms.ModelForm):
    class Meta:
        model = StartupApplication

        exclude = ['create_date','edit_date']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'business_description': forms.Textarea(attrs={'class': 'form-control'}),
            'legal_structure': forms.Select(attrs={'class': 'form-control'}),
        }
        def __init__(self, *args, **kwargs):

            self.helper = FormHelper()
            self.helper.form_method = 'post'
            # get rid of extra keywords before calling super
            self.request = kwargs.pop('request')
            # call super to get form fields
            super(CompanyForm, self).__init__(*args, **kwargs)
            self.helper.form_id = 'Company_update_form'
            self.helper.form_class = 'form-horizontal'
            self.helper.label_class = 'col-sm-2'
            self.helper.field_class = 'col-sm-6'
            self.helper.form_error_title = 'Form Errors'
            self.helper.error_text_inline = True
            self.helper.help_text_inline = True
            self.helper.html5_required = True
            self.helper.layout = Layout(

                HTML("""<br/>"""),
                TabHolder(
                    Tab('Company Information',
                        Fieldset('',
                            'company_name','business_description','legal_structure',
                            ),
                    ),
                    
                    Tab('Company Structure',
                        Fieldset('',
                            'ownership_structure', 'annual_revenue', 'funding_amount','outstanding_debt'
                            ),
                    ),
                    
                    Tab('Founders',
                        Fieldset('',
                            'founder_names', 'team_members', 'advisors_mentors','target_audience','competition_analysis','market_demand_proof','marketing_strategy'
                            ),
                    ),
                    
                    Tab('Stage and Strategy',
                        Fieldset('',
                                'development_stage','intellectual_property','customer_base','customer_acquisition_strategy','current_funding_sources','future_funding_plans'
                            ),
                    ),
                    
                    Tab('Compliance',
                        Fieldset('',
                                    'regulatory_compliance','legal_issues', 'scalability','expansion_plans','social_impact','revenue_model','pricing_strategy','competitive_advantage','milestones_achievements','references_recommendations','alignment_with_mission','support_requested'
                            ),
                    ),
                        
                ),

                HTML("""<br/>"""),
                FormActions(
                    Submit('submit', 'Save', css_class='btn-default'),
                    Reset('reset', 'Reset', css_class='btn-warning')
                )
            )

            super(StartupApplicationForm, self).__init__(*args, **kwargs)




class FounderSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Company Forms
class CompanyForm(forms.ModelForm):
    brief = forms.FileField(required=False,
        label="Upload a file",
        help_text="Select a PDF or DOC file to upload.",
    )

    class Meta:
        model = Company
        exclude = ['create_date','edit_date']
        widgets = {'comments': forms.Textarea(attrs={'rows':4}),
        }

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        # get rid of extra keywords before calling super
        self.request = kwargs.pop('request')
        # call super to get form fields
        super(CompanyForm, self).__init__(*args, **kwargs)
        self.helper.form_id = 'Company_update_form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-6'
        self.helper.form_error_title = 'Form Errors'
        self.helper.error_text_inline = True
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.layout = Layout(

            HTML("""<br/>"""),
            TabHolder(
                Tab('Position Description',
                     Fieldset('',
                        'name','position_title','level','skills','description','brief','position_pay','status','language','location','remote'
                        ),
                ),
            ),

            HTML("""<br/>"""),
            FormActions(
                Submit('submit', 'Save', css_class='btn-default'),
                Reset('reset', 'Reset', css_class='btn-warning')
            )
        )

        super(CompanyForm, self).__init__(*args, **kwargs)
