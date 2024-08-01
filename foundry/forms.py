from .models import Company
from django import forms
from crispy_forms.bootstrap import Tab, TabHolder, FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout, Fieldset, Submit, Reset
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import StartupApplication

class StartupApplicationForm(forms.ModelForm):
    pitch_deck = forms.FileField(required=False,
        label="Upload a Pitch Deck",
        help_text="Select a PDF or DOC file to upload.",
    )
    
    class Meta:
        model = StartupApplication

        exclude = ['ownership_structure','support_requested','alignment_with_mission','create_date','edit_date', 'originality_score', 'marketability_score', 'feasibility_score', 'completeness_score', 'summary','gemini_originality_score','gemini_marketability_score','gemini_feasibility_score','gemini_completeness_score', 'gemini_summary']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'business_description': forms.Textarea(attrs={'class': 'form-control'}),
            'legal_structure': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.request = kwargs.pop('request', None)
        self.helper.form_id = 'company_update_form'
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
                        HTML("""<br/>"""),
                        Fieldset('',
                            'company_name','contact_email','business_description','legal_structure','pitch_deck', 'annual_revenue','funding_amount','outstanding_debt'
                            ),
                    ),
                    
                    Tab('Founders',
                        HTML("""<br/>"""),
                        Fieldset('',
                            'founder_names', 'team_members', 'advisors_mentors','target_audience','competition_analysis','market_demand_proof'
                            ,'marketing_strategy'
                            ),
                    ),
                    
                    Tab('Stage and Strategy',
                        HTML("""<br/>"""),
                        Fieldset('',
                                'development_stage','intellectual_property','customer_base','customer_acquisition_strategy','current_funding_sources'
                                ,'future_funding_plans'
                            ),
                    ),
                    
                    Tab('Progress and Future Plans',
                        HTML("""<br/>"""),
                        Fieldset('',
                                    'social_impact','revenue_model',
                                    'pricing_strategy','competitive_advantage','milestones_achievements','references_recommendations'
                            ),
                    ),
                        
                ),

                HTML("""<br/>"""),
                FormActions(
                    Submit('submit', 'Save', css_class='btn-default'),
                    Reset('reset', 'Reset', css_class='btn-warning')
                )
            )

        super().__init__(*args, **kwargs)

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
