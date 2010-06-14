import os.path
import random

from django import forms
from django import http
from django import template
from django.conf import settings
from django.db import models
from django.db.models import get_models
from django.shortcuts import render_to_response
from django.template.defaultfilters import slugify
from django.utils.importlib import import_module

from relatorio.templates.opendocument import Template

__all__ = ('Report',)

class Dict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

def gen_upload_to(instance, filename):
    return os.path.join(instance.__class__.__name__, str(random.randint(1, 2**31)), filename)

class Report(models.Model):
    """Represents a relatorio report, with custom fields and params"""
    template = models.FileField(upload_to=gen_upload_to)
    name = models.CharField(max_length=255)
    fields = models.TextField(default="{}", help_text="""
        You can use `forms.&lt;Field&gt;` to refers FormField classes of
        django.forms package.
        Use an empty dict ({}) if you do not need them.
    """)
    params = models.TextField(default="{}", help_text="""
        You can use `&lt;ModelName&gt;.objects...` for all installed models through
        all the installed apps. And `form.&lt;field_name&gt;` to refers the value
        which come from the form created based on the fields of this Report
        instance.
    """)

    _formats = {
        'odt': 'application/vnd.oasis.opendocument.text',
    }

    def __unicode__(self):
        return self.name

    def short_name(self):
        return slugify(self.name)

    def form_class(self):
        return type('Form', (forms.Form,), eval(self.fields))

    def handle_form(self, request):
        form_class = self.form_class()

        if not form_class.base_fields:
            return self.render_report(Dict())

        if request.method == "POST":
            form = form_class(request.POST)
            if form.is_valid():
                return self.render_report(Dict(form.cleaned_data))
        else:
            form = form_class()

        return render_to_response("autoreport/form.html",
            {'form': form, 'report_name': self.name},
            context_instance=template.RequestContext(request))

    def render_report(self, form_data, format='odt'):
        locals_ = locals()
        locals_.update(dict([(x.__name__, x) for x in get_models()]))
        locals_.update({'form': form_data})
        report = Template(source=None, filepath=self.template.path)
        if hasattr(settings, 'AUTOREPORT_CONTEXT_PROCESSOR'):
            path = settings.AUTOREPORT_CONTEXT_PROCESSOR
            i = path.rfind('.')
            context_processor = getattr(import_module(path[:i]), path[i+1:])
        else:
            context_processor = lambda d: d
        response = http.HttpResponse(report.generate(**context_processor(eval(self.params, globals(), locals_))).render().getvalue(), mimetype=self._formats[format])
        response['Content-Disposition'] = 'attachment; filename=%s.%s' % (self.short_name(), format)
        return response

    @models.permalink
    def get_absolute_url(self):
        return ('autoreport.views.handle_report', (), {'pk': self.pk})
