from .models import *
from django.contrib import admin

admin.site.register(Company, CompanyAdmin)
admin.site.register(Foundry, FoundryAdmin)
admin.site.register(StartupApplication, StartupApplicationAdmin)
admin.site.register(EvaluationScores, EvaluationScoresAdmin)
