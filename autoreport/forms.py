from django import forms

from autoreport.models import Report

class SelectReportForm(forms.Form):
    report = forms.ModelChoiceField(Report.objects.order_by('name'))
