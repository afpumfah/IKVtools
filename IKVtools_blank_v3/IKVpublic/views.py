from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.contrib import messages

from django.db.models import Count

from .models import Public, PublicAssistant, PublicFiles, PublicWorkPackage, Financier
from .forms import PublicForm, PublicFilesFormSet, PublicAssistantFormSet, PublicWorkPackageFormSet, PublicFilesForm, FinancierForm

from IKVpublication.models import Publication
from IKVprotocol.models import Protocol

from datetime import datetime
import pandas as pd

# Create your views here.

class PublicListView(FormView):
    template_name = 'IKVpublic/public_list.html'
    form_class = PublicForm
    success_url = '#'

    def get(self, request, *args, **kwargs):
        try:
            public = Public.objects.get(pk=request.GET['id'])
            messages.warning(request, '<b>{}</b> wurde gelöscht.'.format(public.short_title), extra_tags='delete')
            public.delete()
        except:
            pass

        try:
            self.current_year = int(self.request.GET['year'])
        except:
            self.current_year = datetime.now().year

        try:
            self.export = self.request.GET['export']
        except:
            pass

        return super(PublicListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        public_projects = Public.objects.all()
        context['public_projects'] = public_projects

        try:
            current_year = self.current_year
        except:
            current_year = datetime.now().year
        context['current_year'] = current_year

        public_project_year = public_projects.filter(start__year__lte = current_year).filter(end__year__gte = current_year).exclude(status = 'ID').exclude(status = 'CR').exclude(status = 'DD').exclude(status = 'PL').exclude(status = 'PO')

        fin = {}
        for f in Financier.objects.all():
            count_fin = public_project_year.filter(financier = f.pk).count()
            if count_fin != 0:
                fin[str(f)] = [count_fin, f.color]
        context['financier'] = fin

        try:
            if self.request.GET['export']:
                self.xlsx_export(context['financier'], public_project_year, current_year)
        except:
            pass

        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, '<b>{}</b> wurde erstellt'.format(self.request.POST['short_title']), extra_tags='created')
        return super().form_valid(form)

    def xlsx_export(self, financier, public_project, current_year):
        xls = pd.ExcelWriter('C:/ikvtools_v3/public_' + str(current_year) + '.xlsx', engine='xlsxwriter')
        overall_projects = pd.DataFrame(financier)
        overall_projects = overall_projects.drop(1)
        overall_projects.to_excel(xls, sheet_name='Überblick')

        projects = public_project.values_list('fanr', 'financier__name', 'project_number', 'short_title', 'start', 'end', 'funded_position', 'status')
        projects = pd.DataFrame(projects,
                                columns=['FA-Nummer', 'Geldgeber', 'Nummer', 'Kurztitel', 'Start', 'Ende', 'Anzahl Stellen', 'Status'])
        projects.to_excel(xls, sheet_name='Überblick', startcol=8)

        registered_public_projects = Public.objects.filter(status = 'CR')
        registered_public_projects = registered_public_projects.values_list('fanr', 'financier__name', 'project_number', 'short_title', 'start', 'end', 'funded_position', 'status')
        registered_public_projects = pd.DataFrame(registered_public_projects,
                                                  columns=['FA-Nummer', 'Geldgeber', 'Nummer', 'Kurztitel', 'Start', 'Ende', 'Anzahl Stellen', 'Status'])
        registered_public_projects.to_excel(xls, sheet_name='Überblick', startcol=8, startrow=len(projects) + 3)

        xls.save()

class PublicDetailView(DetailView):
    model = Public

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['files'] = PublicFiles.objects.filter(project_id = context['object'].id)
        context['assistant'] = PublicAssistant.objects.filter(project_id = context['object'].id)
        context['work_package'] = PublicWorkPackage.objects.filter(project_id = context['object'].id)
        context['template_name'] = self.template_name_suffix
        context['optime'] = str(round((context['object'].end - context['object'].start).days / 30))

        context['publications'] = context['object'].publication_set.all()
        context['nr_publication'] = len(context['publications'])
        return context


class PublicUpdateView(UpdateView):
    form_class = PublicForm
    model = Public
    template_name_suffix = '_update_form'
    success_url = '#'

    def get_context_data(self, **kwargs):
        context = super(PublicUpdateView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        return super(PublicUpdateView, self).form_valid(form)


class PublicUpdateFileView(UpdateView):
    form_class = PublicForm
    model = Public
    template_name_suffix = '_update_file'
    success_url = '#'

    def get_context_data(self, **kwargs):
        context = super(PublicUpdateFileView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['files'] = PublicFilesFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['files'] = PublicFilesFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        files = context['files']
        if files.is_valid():
            files.save()       
        return super(PublicUpdateFileView, self).form_valid(form)


class PublicUpdateAssistantView(UpdateView):
    form_class = PublicForm
    model = Public
    template_name_suffix = '_update_assistant'
    success_url = '#'

    def get_context_data(self, **kwargs):
        context = super(PublicUpdateAssistantView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['assistant'] = PublicAssistantFormSet(self.request.POST, instance=self.object)
        else:
            context['assistant'] = PublicAssistantFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        assistant = context['assistant']
        if assistant.is_valid():
            assistant.save()       
        return super(PublicUpdateAssistantView, self).form_valid(form)


class PublicUpdateWorkPackageView(UpdateView):
    form_class = PublicForm
    model = Public
    template_name_suffix = '_update_workpackage'
    success_url = '#'

    def get_context_data(self, **kwargs):
        context = super(PublicUpdateWorkPackageView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['work_package'] = PublicWorkPackageFormSet(self.request.POST, instance=self.object)
        else:
            context['work_package'] = PublicWorkPackageFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        wp = context['work_package']
        if wp.is_valid():
            wp.save()       
        return super(PublicUpdateWorkPackageView, self).form_valid(form)


class FinancierView(FormView):
    form_class = FinancierForm
    model = Financier
    template_name = 'IKVpublic/settings_financier.html'
    success_url = '#'

    def get(self, request, *args, **kwargs):
        try:
            financier = Financier.objects.get(pk=request.GET['id'])
            messages.warning(request, '<b>{}</b> wurde gelöscht.'.format(financier.name), extra_tags='delete')
            financier.delete()
        except:
            pass

        return super(FinancierView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['financier'] = Financier.objects.all()
        return context
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, '<b>{}</b> wurde erstellt'.format(self.request.POST['name']), extra_tags='created')
        return super(FinancierView, self).form_valid(form)


class FinancierUpdateView(UpdateView):
    form_class = FinancierForm
    model = Financier
    template_name = 'IKVpublic/settings_financier_update.html'
    success_url = reverse_lazy('IKVpublic:settings_financier')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['financier'] = Financier.objects.all() 
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        messages.success(self.request, '<b>{}</b> wurde geändert'.format(self.request.POST['name']), extra_tags='created')
        return super(FinancierUpdateView, self).form_valid(form)


class PublicProtocol(TemplateView):
    template_name = 'IKVpublic/public_protocol.html'

    def get_context_data(self, **kwargs):
        context = super(PublicProtocol, self).get_context_data(**kwargs)
        protocol = Protocol.objects.filter(public_project_id = self.kwargs['pk']).order_by('-date')
        context['protocol'] = protocol
        context['object'] = {'pk': self.kwargs['pk']}
        return context
