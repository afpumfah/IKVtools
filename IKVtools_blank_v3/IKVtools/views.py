from django.views.generic import TemplateView, FormView
from django.shortcuts import render

from IKVstudents.models import Thesis
from IKVpublication.models import Publication
from IKVpublic.models import Public
from IKVindustry.models import Industry
from IKVprotocol.models import ToDo
from IKVassistant.models import Assistant

from datetime import datetime

class Index(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        try:
            done_pk = request.GET['done']
            todo = ToDo.objects.get(pk=done_pk)
            todo.done = True
            todo.save()
        except:
            pass
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(Index, self).get_context_data(*args, **kwargs)

        current_month = datetime.now().month
        current_year = datetime.now().year
        context['current_month'] = current_month
        context['current_year'] = current_year

        #Industry
        planned_industry = Industry.objects.filter(status = 'CR')
        context['planned_industry'] = planned_industry

        end_finance = Industry.objects.filter(finish_finance_a__year = current_year).filter(finish_finance_a__month = current_month + 1)
        context['end_finance'] = end_finance

        #Public Projects
        planned_public_projects = Public.objects.filter(status = 'PL').order_by('al_date')
        context['planned_public_projects'] = planned_public_projects

        post_al_public_projects = Public.objects.filter(status = 'PO').order_by('al_date')
        context['post_al_public_projects'] = post_al_public_projects

        accepted_public_projects = Public.objects.filter(status = 'AC').order_by('start')
        context['accepted_public_projects'] = accepted_public_projects

        registered_public_projects = Public.objects.filter(status = 'CR').order_by('al_date')
        context['registered_public_projects'] = registered_public_projects

        #Thesis
        registered_thesis = Thesis.objects.filter(release_date = None)
        context['registered_thesis'] = registered_thesis

        #Publication
        registered_publication = Publication.objects.filter(status = 'CR').order_by('release_date')
        context['registered_publications'] = registered_publication

        planned_publications = Publication.objects.filter(status = 'PL').order_by('release_date')
        context['planned_publications'] = planned_publications

        #ToDo
        todo = ToDo.objects.filter(done = False).order_by('duedate')
        context['todo'] = todo
        
        #Birthday
        birth = Assistant.objects.filter(birth__month = current_month).exclude(status = 'IC').order_by('birth')
        context['birth'] = birth

        return context


class Settings(TemplateView):
    template_name = "settings.html"

    def get_context_data(self, *args, **kwargs):
        context = super(Settings, self).get_context_data(*args, **kwargs)
        context = {'test':'NAME'}
        return context
