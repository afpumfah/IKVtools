from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q

from datetime import datetime
import pandas as pd

from .forms import AssistantForm, AssistantFormSet, AssistantFilesForm
from .models import Assistant, AssistantFiles

from IKVindustry.models import Industry, WorkPackage
from IKVpublication.models import Publication
from IKVpublic.models import Public, Financier
from IKVprotocol.models import Protocol, ToDo

class AssistantListView(FormView):
    template_name = 'IKVassistant/assistant_list.html'
    form_class = AssistantForm
    success_url = '#'

    def get(self, request, *args, **kwargs):
        try:
            assistant = Assistant.objects.get(pk=request.GET['id'])
            messages.warning(request, '<b>{} {}</b> wurde gelöscht.'.format(assistant.firstname, assistant.lastname), extra_tags='delete')
            assistant.delete()
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
        return super(AssistantListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assistant = Assistant.objects.all().exclude(status = 'IC')
        context['assistant'] = assistant

        try:
            current_year = self.current_year
        except:
            current_year = datetime.now().year
        context['current_year'] = current_year

        public_projects = Public.objects.filter(start__year__lte = current_year).filter(end__year__gte = current_year).exclude(status = 'DD').exclude(status = 'ID').exclude(status = 'CR').exclude(status = 'PL').exclude(status = 'PO')
        fin = {}
        for f in Financier.objects.all():
           project = public_projects.filter(financier = f.pk)
           complete_year = sum([x.funded_position*12 for x in project if x.start.year < current_year and x.end.year > current_year])
           finish_year = sum([x.funded_position*x.end.month for x in project if x.start.year < current_year and x.end.year == current_year])
           start_year = sum([x.funded_position*(13-x.start.month) for x in project if x.start.year == current_year and x.end.year > current_year])
           start_finish_year = sum([x.funded_position*(x.end.month + 1 - x.start.month) for x in project if x.start.year == current_year and x.end.year == current_year])
           sum_year = complete_year + finish_year + start_year + start_finish_year
           if sum_year != 0:
               fin[str(f)] = [sum_year, complete_year, finish_year, start_year, start_finish_year, f.color]
        context['financier'] = fin
        context['sum_financed'] = sum([value[0] for key,value in fin.items()])

        for st in Assistant.STATUS:
            assi = assistant.filter(status = st[0])
            assi_complete_year = sum([12 for x in assi if x.start.year < current_year and x.end.year > current_year])
            assi_finish_year = sum([x.end.month for x in assi if x.start.year < current_year and x.end.year == current_year])
            assi_start_year = sum([(13-x.start.month) for x in assi if x.start.year == current_year and x.end.year > current_year])
            assi_start_finish_year = sum([x.end.month + 1 - x.start.month for x in assi if x.start.year == current_year and x.end.year == current_year])
            context[st[0]] = assi_complete_year + assi_finish_year + assi_start_year + assi_start_finish_year
        context['fin_assistant'] = context['AC'] + context['PL'] + context['ALU']

        try:
            if self.request.GET['export']:
                self.xlsx_export(fin, context['sum_financed'], assistant, context['fin_assistant'], current_year)
        except:
            pass
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, '<b>{} {}</b> wurde erstellt'.format(self.request.POST['firstname'], self.request.POST['lastname']), extra_tags='created')
        return super().form_valid(form)

    def xlsx_export(self, financier, sum_financed, assistant, fin_asssistant, current_year):
        xls = pd.ExcelWriter('C:/ikvtools_v3/assistant_' + str(current_year) + '.xlsx', engine='xlsxwriter')
        overall_assistant = pd.DataFrame(financier)
        overall_assistant = overall_assistant.drop(5)
        overall_assistant = overall_assistant.rename(index={0 : '{} Gesamt'.format(current_year), 
                                                            1 : '{} durchgelaufen'.format(current_year),
                                                            2 : '{} beendet'.format(current_year),
                                                            3 : '{} gestartet'.format(current_year),
                                                            4 : '{} gestartet + beendet'.format(current_year)
                                                            })
        overall_assistant['Summe'] = sum_financed
        overall_assistant['Bedarf'] = fin_asssistant
        overall_assistant.to_excel(xls, sheet_name='Überblick')
        assis = assistant.values_list('firstname', 'lastname', 'start', 'end', 'status')
        assis = pd.DataFrame(assis,
                         columns=['Vorname', 'Nachname', 'Start', 'Ende', 'Status'])
        assis.to_excel(xls, sheet_name='Überblick', startcol=10)
        xls.save()


class AssistantDetailView(DetailView):
    model = Assistant

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['files'] = AssistantFiles.objects.filter(assistant_id = context['object'].id)
        context['template_name'] = self.template_name_suffix

        wp = WorkPackage.objects.filter(assistant_id = context['object'].id).values_list('project_id', flat=True).distinct()
        ip = Industry.objects.filter(pk__in = wp).order_by("-status")
        context['industry_projects'] = ip

        context['publications'] = context['object'].publication_set.all()
        context['public_projects'] = context['object'].publicassistant_set.all().order_by("-project_id__status")

        context['student_assistant'] = context['object'].studentassistant_set.all().order_by('student_id__lastname')
        context['thesis'] = context['object'].thesis_set.all()

        return context


class AssistantUpdateView(UpdateView):
    model = Assistant
    template_name_suffix = '_update_form'
    form_class = AssistantForm
    success_url = '#'

    def get_context_data(self, **kwargs):
        data = super(AssistantUpdateView, self).get_context_data(**kwargs)
        return data
    
    def form_valid(self, form):
        return super(AssistantUpdateView, self).form_valid(form)


class AssistantUpdateFilesView(UpdateView):
    model = Assistant
    template_name_suffix = '_update_file'
    form_class = AssistantForm
    success_url = '#'

    def get_context_data(self, **kwargs):
        data = super(AssistantUpdateFilesView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['files'] = AssistantFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['files'] = AssistantFormSet(instance=self.object)
        return data
    
    def form_valid(self, form):
        context = self.get_context_data()
        files = context['files']
        if files.is_valid():
            files.save()
        return super(AssistantUpdateFilesView, self).form_valid(form)


class AssistantProtocol(TemplateView):
    template_name = 'IKVassistant/assistant_protocol.html'

    def get_context_data(self, **kwargs):
        context = super(AssistantProtocol, self).get_context_data(**kwargs)
        protocol = Protocol.objects.filter(assistant_id = self.kwargs['pk']).order_by('-date')
        context['protocol'] = protocol
        context['object'] = {'pk': self.kwargs['pk']}
        return context
