from .models import *
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources

class StartupApplicationResource(resources.ModelResource):

    class Meta:
        model = StartupApplication  # or 'core.Book'

class StartupApplicationAdmin(ImportExportModelAdmin):
    resource_classes = [StartupApplicationResource]

admin.site.register(Company, CompanyAdmin)
admin.site.register(Foundry, FoundryAdmin)
admin.site.register(StartupApplication, StartupApplicationAdmin)
admin.site.register(EvaluationScores, EvaluationScoresAdmin)