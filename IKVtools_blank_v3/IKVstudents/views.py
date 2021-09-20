from django.shortcuts import render, HttpResponseRedirect
from django.views.generic.edit import UpdateView
from django.views.generic import FormView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Count
from django.forms.models import model_to_dict

from .models import Student, StudentAssistant, Thesis, MeanPrice
from .forms import StudentForm, StudentAssistantFormSet, ThesisFormSet, PriceForm

from IKVindustry.models import Industry
from IKVpublic.models import Public
from IKVassistant.models import Assistant

import datetime as dt
from datetime import datetime
import pandas as pd
from decimal import Decimal

# Create your views here.
class StudentListView(FormView):
    template_name = 'IKVstudents/student_list.html'
    form_class = StudentForm
    success_url = reverse_lazy('IKVstudents:list')

    def get(self, request, *args, **kwargs):
        try:
            student = Student.objects.get(pk=request.GET['id'])
            messages.warning(request, '<b>{} {}</b> wurde gelöscht.'.format(student.firstname, student.lastname), extra_tags='delete')
            student.delete()
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

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        students = Student.objects.all()
        context['students'] = students

        try:
            current_year = self.current_year
        except:
            current_year = datetime.now().year

        context['current_year'] = current_year
        students_year = StudentAssistant.objects.filter(end__year__gte = str(current_year)).filter(start__year__lte = str(current_year))
        complete_year = sum([x.price for x in students_year if x.start.year < current_year and x.end.year > current_year])
        finish_year = sum([x.price*x.end.month for x in students_year if x.start.year < current_year and x.end.year == current_year])
        start_year = sum([x.price*(13 - x.start.month) for x in students_year if x.start.year == current_year and x.end.year > current_year])
        start_finish_year = sum([x.price*(x.end.month + 1 - x.start.month) for x in students_year if x.start.year == current_year and x.end.year == current_year])
        context['students_need'] = complete_year + finish_year + start_year + start_finish_year
        
        
        try:
            mean_price = MeanPrice.objects.get(pk=1)
            industry_year = Industry.objects.filter(finish_finance_s__year = str(current_year))
            context['industry_budget'] = sum(x.students_budget for x in industry_year)

            public_year = Public.objects.filter(end__year__gte = str(current_year)).filter(start__year__lte = str(current_year)).exclude(status='CR').exclude(status = 'PL').exclude(status = 'PO')
            complete_year = sum([Decimal(x.funded_students)*12*mean_price.mean_price for x in public_year if x.start.year < current_year and x.end.year > current_year])
            finish_year = sum([Decimal(x.funded_students)*mean_price.mean_price*x.end.month for x in public_year if x.start.year < current_year and x.end.year == current_year])
            start_year = sum([Decimal(x.funded_students)*mean_price.mean_price*(13 - x.start.month) for x in public_year if x.start.year == current_year and x.end.year > current_year])
            start_finish_year = sum([Decimal(x.funded_students)*mean_price.mean_price*(x.end.month + 1 - x.start.month) for x in public_year if x.start.year == current_year and x.end.year == current_year])
            context['public_budget'] = complete_year + finish_year + start_year + start_finish_year

            assistant_year = Assistant.objects.filter(end__year__gte = str(current_year)).filter(start__year__lte = str(current_year))
            complete_year = sum([12*mean_price.mean_price for x in assistant_year if x.start.year < current_year and x.end.year > current_year])
            finish_year = sum([mean_price.mean_price*x.end.month for x in assistant_year if x.start.year < current_year and x.end.year == current_year])
            start_year = sum([mean_price.mean_price*(13 - x.start.month) for x in assistant_year if x.start.year == current_year and x.end.year > current_year])
            start_finish_year = sum([mean_price.mean_price*(x.end.month + 1 - x.start.month) for x in assistant_year if x.start.year == current_year and x.end.year == current_year])
            context['assistant_budget'] = complete_year + finish_year + start_year + start_finish_year

            thesis = Thesis.objects.filter(release_date__year = str(current_year))
            context['ma'] = thesis.filter(type = 'MA').count() 
            context['pa'] = thesis.filter(type = 'PA').count() 
            context['ba'] = thesis.filter(type = 'BA').count() 
        except:
            pass
        
        try:
            if self.export:
                xls = pd.ExcelWriter('C:/ikvtools_v3/students_' + str(current_year) + '.xlsx', engine='xlsxwriter')
                overall_budget = [(context['students_need'],0,0,0),
                                  (0, context['assistant_budget'], context['public_budget'], context['industry_budget'])]
                sum_budget = pd.DataFrame(overall_budget,
                                          columns=['Bedarf', 'Grundausstattung', 'öffentlich', 'Industrie'],
                                          index=['Bedarf', 'Finanziert'])

                sum_budget.to_excel(xls, sheet_name='Überblick', float_format='%.2f')

                #Studenten
                students = students_year.values_list('assistant_id__lastname', 'student_id__firstname', 'student_id__lastname', 'status', 'hours', 'price', 'start', 'end')
                students = pd.DataFrame(list(students), 
                                        columns=['Assistent', 'Vorname', 'Nachname', 'Status', 'Stunden', 'Preis', 'Start', 'Ende'])
                students['Diff'] = 0
                for index, x in students.iterrows():
                    if x['Ende'].year > current_year and x['Start'].year < current_year:
                        students['Diff'][index] = 12
                    elif x['Ende'].year == current_year and x['Start'].year < current_year: 
                        students['Diff'][index] = x['Ende'].month
                    elif x['Ende'].year > current_year and x['Start'].year == current_year:
                        students['Diff'][index] = 13 - x['Start'].month
                    else:
                        students['Diff'][index] = x['Ende'].month - x['Start'].month + 1
                students['Betrag'] = students['Preis'] * students['Diff']
                students.to_excel(xls, sheet_name='Überblick', startcol=6)

                #Grundausstattung
                assistant = assistant_year.values_list('lastname', 'start', 'end')
                assistant = pd.DataFrame(assistant,
                                         columns=['Nachname', 'Start', 'Ende'])
                assistant['Diff'] = 0
                for index, x in assistant.iterrows():
                    if x['Ende'].year > current_year and x['Start'].year < current_year:
                        assistant['Diff'][index] = 12
                    elif x['Ende'].year == current_year and x['Start'].year < current_year: 
                        assistant['Diff'][index] = x['Ende'].month
                    elif x['Ende'].year > current_year and x['Start'].year == current_year:
                        assistant['Diff'][index] = 13 - x['Start'].month
                    else:
                        assistant['Diff'][index] = x['Ende'].month - x['Start'].month + 1
                assistant['Betrag'] = assistant['Diff'] * mean_price.mean_price
                assistant.to_excel(xls, sheet_name='Überblick', startcol=19)

                #Öffentliche Projekte
                public = public_year.values_list('fanr', 'short_title', 'start', 'end', 'funded_students')
                public = pd.DataFrame(public,
                                      columns=['FA-Nummer', 'Kurztitel', 'Start', 'Ende', 'HiWi-Stellen'])
                public['Diff'] = 0
                for index, x in public.iterrows():
                    if x['Ende'].year > current_year and x['Start'].year < current_year:
                        public['Diff'][index] = 12
                    elif x['Ende'].year == current_year and x['Start'].year < current_year: 
                        public['Diff'][index] = x['Ende'].month
                    elif x['Ende'].year > current_year and x['Start'].year == current_year:
                        public['Diff'][index] = 13 - x['Start'].month
                    else:
                        public['Diff'][index] = x['Ende'].month - x['Start'].month + 1
                public['Betrag'] = public['Diff'] * float(mean_price.mean_price) * public['HiWi-Stellen']
                public.to_excel(xls, sheet_name='Überblick', startcol=19, startrow=len(assistant) + 2)

                #Industrie
                industry = industry_year.values_list('fanr', 'short_title', 'finish_finance_s', 'students_budget')
                industry = pd.DataFrame(industry,
                                        columns=['FA-Nummer', 'Kurztitel', 'Ende Buchhaltung', 'Budget'])
                industry.to_excel(xls, sheet_name='Überblick', startcol=19, startrow=len(assistant)+len(public)+4)

                #Abschlussarbeiten
                thesis_count = pd.DataFrame([(context['ma'], context['ba'], context['pa'])],
                                            columns=['MA', 'BA', 'PA'])
                thesis_count.to_excel(xls, sheet_name='Abschlussarbeiten')

                thesis_year = thesis.values_list('supervisor_id__lastname', 'student_id__lastname', 'type', 'title', 'release_date')
                thesis_year = pd.DataFrame(thesis_year,
                                           columns=['Betreuer','SuWi', 'Art', 'Titel', 'Datum'])
                thesis_year.to_excel(xls, sheet_name='Abschlussarbeiten', startcol=5)

                thesis_open = Thesis.objects.filter(release_date=None).values_list('supervisor_id__lastname', 'student_id__lastname', 'type', 'title', 'release_date')
                thesis_open = pd.DataFrame(thesis_open,
                                           columns=['Betreuer','SuWi', 'Art', 'Titel', 'Datum'])
                thesis_open.to_excel(xls, sheet_name='Abschlussarbeiten', startcol=5, startrow=len(thesis_year)+2) 
                xls.save()
        except:
            pass

        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        form.save()
        messages.success(self.request, '<b>{} {}</b> wurde erstellt.'.format(self.request.POST['firstname'], self.request.POST['lastname']), extra_tags='created')
        return super(StudentListView, self).form_valid(form)


class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'IKVstudents/student_update.html'
    success_url = reverse_lazy('IKVstudents:list')

    def get(self, request, *args, **kwargs):
        try:
            student = Student.objects.get(pk=request.GET['id'])
            messages.warning(request, '<b>{} {}</b> wurde gelöscht.'.format(student.firstname, student.lastname), extra_tags='delete')
            student.delete()
            return HttpResponseRedirect(reverse_lazy('IKVstudents:list'))
        except:
            pass
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StudentUpdateView, self).get_context_data(**kwargs)
        context['students'] = Student.objects.all()
        if self.request.POST:
            context['student_assistant'] = StudentAssistantFormSet(self.request.POST, instance=self.object)
            context['thesis'] = ThesisFormSet(self.request.POST, instance=self.object)
        else:
            context['student_assistant'] = StudentAssistantFormSet(instance=self.object)
            context['thesis'] = ThesisFormSet(instance=self.object)

        shk = {}
        whk = {}
        mean_price = MeanPrice.objects.get(pk=1)
        for f in MeanPrice._meta.get_fields()[2:]:
            if f.name[0] == 's':
                shk[f.name[-2:]] = getattr(mean_price, f.name)
            else:
                whk[f.name[-2:]] = getattr(mean_price, f.name)

        for k, v in shk.items():
            shk[k] = shk[k], whk[k]

        form = PriceForm({'mean_price':1000000})
        context['price'] = shk

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        student_assistant = context['student_assistant']
        thesis = context['thesis']
        if student_assistant.is_valid():
            student_assistant.save()
        if thesis.is_valid():
            thesis.save()
        return  super(StudentUpdateView, self).form_valid(form)


class PriceUpdateView(FormView):
    form_class = PriceForm
    template_name = 'IKVstudents/settings_meanprice.html'
    success_url = '#'

    def get_initial(self):
        try:
            initial = super(PriceUpdateView, self).get_initial()
            mean_price = MeanPrice.objects.get(pk=1)
            initial.update(model_to_dict(mean_price))
        except:
            initial = 0
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            mean_price = MeanPrice.objects.get(pk=1)
            if not mean_price:
                context['mean_price'] = 'Noch nicht vorhanden'
            else:
                context['mean_price'] = str(mean_price.mean_price) + ' €'
                shk = {}
                whk = {}
                for f in MeanPrice._meta.get_fields()[2:]:
                    if f.name[0] == 's':
                        shk[f.name[-2:]] = getattr(mean_price, f.name)
                    else:
                        whk[f.name[-2:]] = getattr(mean_price, f.name)

                for k, v in shk.items():
                    shk[k] = shk[k], whk[k]

                form = PriceForm({'mean_price':1000000})
                context['price'] = shk
        except:
            pass

        return context
    
    def form_valid(self, form):
        mean_price = MeanPrice.objects.filter(pk=1)
        if not mean_price:
            new = MeanPrice(mean_price = self.request.POST['mean_price'],
                            shk_07 = self.request.POST['shk_07'],
                            shk_08 = self.request.POST['shk_08'],
                            shk_09 = self.request.POST['shk_09'],
                            shk_10 = self.request.POST['shk_10'],
                            shk_11 = self.request.POST['shk_11'],
                            shk_12 = self.request.POST['shk_12'],
                            shk_13 = self.request.POST['shk_13'],
                            shk_14 = self.request.POST['shk_14'],
                            shk_15 = self.request.POST['shk_15'],
                            shk_16 = self.request.POST['shk_16'],
                            shk_17 = self.request.POST['shk_17'],
                            shk_18 = self.request.POST['shk_18'],
                            shk_19 = self.request.POST['shk_19'],
                            whk_07 = self.request.POST['whk_07'],
                            whk_08 = self.request.POST['whk_08'],
                            whk_09 = self.request.POST['whk_09'],
                            whk_10 = self.request.POST['whk_10'],
                            whk_11 = self.request.POST['whk_11'],
                            whk_12 = self.request.POST['whk_12'],
                            whk_13 = self.request.POST['whk_13'],
                            whk_14 = self.request.POST['whk_14'],
                            whk_15 = self.request.POST['whk_15'],
                            whk_16 = self.request.POST['whk_16'],
                            whk_17 = self.request.POST['whk_17'],
                            whk_18 = self.request.POST['whk_18'],
                            whk_19 = self.request.POST['whk_19'],
            )
            new.save()
        else:
            mean_price = MeanPrice.objects.get(pk=1)
            mean_price.mean_price = self.request.POST['mean_price']
            mean_price.shk_07 = self.request.POST['shk_07']
            mean_price.shk_08 = self.request.POST['shk_08']
            mean_price.shk_09 = self.request.POST['shk_09']
            mean_price.shk_10 = self.request.POST['shk_10']
            mean_price.shk_11 = self.request.POST['shk_11']
            mean_price.shk_12 = self.request.POST['shk_12']
            mean_price.shk_13 = self.request.POST['shk_13']
            mean_price.shk_14 = self.request.POST['shk_14']
            mean_price.shk_15 = self.request.POST['shk_15']
            mean_price.shk_16 = self.request.POST['shk_16']
            mean_price.shk_17 = self.request.POST['shk_17']
            mean_price.shk_18 = self.request.POST['shk_18']
            mean_price.shk_19 = self.request.POST['shk_19']
            mean_price.whk_07 = self.request.POST['whk_07']
            mean_price.whk_08 = self.request.POST['whk_08']
            mean_price.whk_09 = self.request.POST['whk_09']
            mean_price.whk_10 = self.request.POST['whk_10']
            mean_price.whk_11 = self.request.POST['whk_11']
            mean_price.whk_12 = self.request.POST['whk_12']
            mean_price.whk_13 = self.request.POST['whk_13']
            mean_price.whk_14 = self.request.POST['whk_14']
            mean_price.whk_15 = self.request.POST['whk_15']
            mean_price.whk_16 = self.request.POST['whk_16']
            mean_price.whk_17 = self.request.POST['whk_17']
            mean_price.whk_18 = self.request.POST['whk_18']
            mean_price.whk_19 = self.request.POST['whk_19']
            mean_price.save()
        messages.success(self.request, 'Änderungen wurden erfolgreich übernommen.')
        return super().form_valid(form)
