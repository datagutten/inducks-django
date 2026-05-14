from django.contrib import admin
from inducks import models


@admin.register(models.Issue)
class IssueAdmin(admin.ModelAdmin):
    list_filter = ['publication']
    list_display = ['publication', 'issuecode', 'issuenumber', 'title', 'oldestdate']
