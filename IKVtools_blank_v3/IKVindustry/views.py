from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q

from .models import Industry, IndustryFiles, WorkPackage, Outgoings
from .forms import IndustryFilesFormSet, WorkPackageFormSet, IndustryForm, OutgoingsFormSet

from IKVprotocol.models import Protocol, ToDo

from datetime import datetime
import pandas as pd
import numpy as np
import decimal


class IndustryListView(FormView):
    template_name = 'IKVindustry/industry_list.html'
    form_class = IndustryForm
    success_url = '#'

    def get(self, request, *args, **kwargs):
        try:
            industry = Industry.objects.get(pk=request.GET['id'])
            messages.warning(request, '<b>{}</b> wurde gelöscht.'.format(industry.short_title), extra_tags='delete')
            industry.delete()
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
        return super(IndustryListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        industry_projects = Industry.objects.all()
        
        try:
            current_year = self.current_year
        except:
            current_year = datetime.now().year
        context['current_year'] = current_year

        #update all projects that exceed finish_finance and set al_budget_left and a_budget_left to zero.
        #Otherwise you will see money that you do not have
        industry_projects.filter(status = 'END').filter(finish_finance_a__lte = datetime.now().date()).update(al_budget_left=0, assi_budget_left=0, released=False)

        context['industry_projects'] = industry_projects

        industry_projects_instruct = WorkPackage.objects.filter(instruct_at__year = current_year)
        industry_projects_invoiced = WorkPackage.objects.filter(~Q(instruct_at = None) & Q(invoiced_at__year = current_year))

        instruct_month = [0,0,0,0,0,0,0,0,0,0,0,0]
        invoiced_month = [0,0,0,0,0,0,0,0,0,0,0,0]
        buf = 0
        for i in range(12):
            project_month_instruct = industry_projects_instruct.filter(instruct_at__month = i+1)
            instruct_month[i] = buf + sum([x.price if x.foreign == False else 0 for x in project_month_instruct])
            buf += sum([x.price if x.foreign == False else 0 for x in project_month_instruct])

        buf = 0
        for i in range(12):
            project_month_invoiced = industry_projects_invoiced.filter(invoiced_at__month = i+1)
            invoiced_month[i] = buf + sum([x.price if x.foreign == False else 0 for x in project_month_invoiced])
            buf += sum([x.price if x.foreign == False else 0 for x in project_month_invoiced])

        invoiced_prev_year = WorkPackage.objects.filter(invoiced_at__year = str(int(current_year) - 1))
        invoiced_prev_year_sum = sum([x.price if x.foreign == False else 0 for x in invoiced_prev_year])
        instruct_prev_year = WorkPackage.objects.filter(Q(instruct_at__year__lte = str(int(current_year) - 1)) & ~Q(invoiced_at__year__lte = str(int(current_year) - 1)))
        instruct_prev_year_sum = sum([x.price if x.foreign == False else 0 for x in instruct_prev_year])

        instruct_month = [x + instruct_prev_year_sum for x in instruct_month]

        context['prev_year_invoiced'] = invoiced_prev_year_sum
        context['prev_year_instruct'] = instruct_prev_year_sum
        context['instruct_month'] = instruct_month
        context['invoiced_month'] = invoiced_month

        try:
            if self.request.GET['export']:
                self.xlsx_export(context['instruct_month'],
                                context['invoiced_month'],
                                industry_projects_instruct,
                                instruct_prev_year,
                                context['prev_year_instruct'],
                                context['prev_year_invoiced'],
                                current_year
                                )
        except:
            pass
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, '<b>{}</b> wurde erstellt'.format(self.request.POST['short_title']), extra_tags='created')
        return super().form_valid(form)

    def xlsx_export(self, instruct_month, invoiced_month, projects_instruct, instruct_prev_year, instruct_prev_year_sum, invoiced_prev_year_sum, current_year):
        xls = pd.ExcelWriter('C:/ikvtools_v3/industry_' + str(current_year) + '.xlsx', engine='xlsxwriter')
        overall_years = ['Vorjahr', 'Jan', 'Feb', 'Mrz', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
        instruct_month = instruct_month.copy()
        invoiced_month = invoiced_month.copy()
        instruct_month.insert(0,instruct_prev_year_sum)
        invoiced_month.insert(0,invoiced_prev_year_sum)
        overall_industry = pd.DataFrame(np.transpose([invoiced_month, instruct_month]),
                                        columns=['Fakturiert', 'Beauftragt'],
                                        index=overall_years)
        overall_industry.to_excel(xls, sheet_name='Überblick')

        industry_projects_instruct_export = projects_instruct.filter(foreign = False).order_by('instruct_at').values_list('project_id__fanr', 'project_id__short_title', 'price', 'instruct_at', 'invoiced_at')
        industry_projects_instruct_prev_year_export = instruct_prev_year.filter(foreign = False).order_by('instruct_at').values_list('project_id__fanr', 'project_id__short_title', 'price', 'instruct_at', 'invoiced_at')
        export_projects = industry_projects_instruct_prev_year_export | industry_projects_instruct_export
        export = pd.DataFrame(export_projects,
                              columns=['FA-Nummer', 'Kurztitel', 'Preis', 'Beauftragt', 'Fakturiert'])
        export.to_excel(xls, sheet_name='Überblick', startcol=5)
        xls.save()


class IndustryDetailView(DetailView):
    model = Industry

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['files'] = IndustryFiles.objects.filter(project_id = context['object'].id)
        context['work_package'] = WorkPackage.objects.filter(project_id = context['object'].id)
        context['outgoings'] = Outgoings.objects.filter(project_id = context['object'].id)
        context['template_name'] = self.template_name_suffix
        return context


class IndustryUpdateView(UpdateView):
    form_class = IndustryForm
    model = Industry
    template_name_suffix = '_update_form'
    success_url = '#'

    def get_context_data(self, **kwargs):
        context = super(IndustryUpdateView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.save()
        return super(IndustryUpdateView, self).form_valid(form)


class IndustryUpdateFileView(UpdateView):
    form_class = IndustryForm
    model = Industry
    template_name_suffix = '_update_file'
    success_url = '#'

    def get_context_data(self, **kwargs):
        data = super(IndustryUpdateFileView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['files'] = IndustryFilesFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['files'] = IndustryFilesFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        files = context['files']
        if files.is_valid():
            files.save()
        return super(IndustryUpdateFileView, self).form_valid(form)


class IndustryUpdateWorkPackageView(UpdateView):
    form_class = IndustryForm
    model = Industry
    template_name_suffix = '_update_workpackage'
    success_url = '#'

    def get_context_data(self, **kwargs):
        data = super(IndustryUpdateWorkPackageView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['work_package'] = WorkPackageFormSet(self.request.POST, instance=self.object)
        else:
            data['work_package'] = WorkPackageFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        work_package = context['work_package']
        if work_package.is_valid():
            work_package.save()
        return super(IndustryUpdateWorkPackageView, self).form_valid(form)


class IndustryUpdateOutgoingsView(UpdateView):
    form_class = IndustryForm
    model = Industry
    template_name_suffix = '_update_outgoing'
    success_url = '#'

    def get_context_data(self, **kwargs):
        data = super(IndustryUpdateOutgoingsView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['outgoings'] = OutgoingsFormSet(self.request.POST, instance=self.object)
        else:
            data['outgoings'] = OutgoingsFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        outgoings = context['outgoings']
        if outgoings.is_valid():
            outgoings.save()
        return super(IndustryUpdateOutgoingsView, self).form_valid(form)


class IndustryProtocol(TemplateView):
    template_name = 'IKVindustry/industry_protocol.html'

    def get_context_data(self, **kwargs):
        context = super(IndustryProtocol, self).get_context_data(**kwargs)
        protocol = Protocol.objects.filter(industry_project_id = self.kwargs['pk']).order_by('-date')
        context['protocol'] = protocol
        context['object'] = {'pk': self.kwargs['pk']}
        return context
