from django import http
from django import template
from django.shortcuts import get_object_or_404, redirect, render_to_response

from autoreport.models import Report
from autoreport.forms import SelectReportForm

__all__ = ('handle_report', 'handle_reports')

def handle_report(request, pk=None):
    """
    Use this view to display a single form with report fields, and/or
    render the report with its configured params.
    It uses the template "autoreport/form.html".
    """
    if not pk:
        return http.HttpResponseBadRequest()

    report = get_object_or_404(Report, pk=pk)
    return report.handle_form(request)

def handle_reports(request):
    """
    This view renders the selector for which report you would like
    to get, and then, take it.
    It uses the template "autoreport/reports.html".
    """
    if request.method == "POST":
        form = SelectReportForm(request.POST)
        if form.is_valid():
            return redirect(form.cleaned_data['report'])
    else:
        form = SelectReportForm()

    return render_to_response("autoreport/reports.html",
        {'form': form},
        context_instance=template.RequestContext(request))
