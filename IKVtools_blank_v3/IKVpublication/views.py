from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.contrib import messages

from .models import Publication, Author, Journal
from .forms import PublicationForm, AuthorForm, JournalForm

from IKVpublic.models import Public
from IKVassistant.models import Assistant

from datetime import datetime

import pandas as pd

# Create your views here.
class PublicationListView(FormView):
    template_name = 'IKVpublication/publication_list.html'
    form_class = PublicationForm
    success_url = reverse_lazy('IKVpublication:list')

    def get(self, request, *args, **kwargs):
        try:
            publication = Publication.objects.get(pk=request.GET['id'])
            messages.warning(request, '<b>{}</b> wurde gelöscht.'.format(publication.title), extra_tags='delete')
            publication.delete()
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

        return super(PublicationListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        publication = Publication.objects.all()
        context['publication'] = publication
        
        try:
            current_year = self.current_year
        except:
            current_year = datetime.now().year
            
        context['current_year'] = current_year
        
        publication_year = publication.filter(release_date__year = str(current_year)).filter(status='GO')

        revj = sum([x.assistant_id.exclude(status='IC').count()/x.assistant_id.count() for x in publication_year.filter(reviewed = 'revj')])
        jour = sum([x.assistant_id.exclude(status='IC').count()/x.assistant_id.count() for x in publication_year.filter(reviewed = 'jour')])
        revc = sum([x.assistant_id.exclude(status='IC').count()/x.assistant_id.count() for x in publication_year.filter(reviewed = 'revc')])
        conf = sum([x.assistant_id.exclude(status='IC').count()/x.assistant_id.count() for x in publication_year.filter(reviewed = 'conf')])
        othe = sum([x.assistant_id.exclude(status='IC').count()/x.assistant_id.count() for x in publication_year.filter(reviewed = 'othe')])

        context['publication_stats'] = [revj, jour, revc, conf, othe]

        try:
            if self.export:
                xls = pd.ExcelWriter('C:/ikvtools_v3/publication_' + str(current_year) + '.xlsx', engine='xlsxwriter')

                overall_publication = [(revj, jour, revc, conf, othe)]
                overall_publication = pd.DataFrame(overall_publication,
                                                   columns=['rez. Journal', 'Journal', 'rez. Konferenz', 'Konferenz', 'Sonstige'])
                overall_publication.to_excel(xls, sheet_name='Überblick')

                publication = publication_year.values_list('assistant_id__lastname', 'title','journal__name', 'reviewed', 'release_date')
                publication = pd.DataFrame(publication,
                                           columns=['Assistenten', 'Tiel', 'Journal', 'Art', 'Erscheinungsdatum'])
                publication.to_excel(xls, sheet_name='Überblick', startcol=7)

                xls.save()
        except:
            pass
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, '<b>{}</b> wurde erstellt'.format(self.request.POST['title']), extra_tags='created')
        return super(PublicationListView, self).form_valid(form)


class PublicationUpdateView(UpdateView):
    form_class = PublicationForm
    model = Publication
    template_name_suffix = '_update'
    success_url = reverse_lazy('IKVpublication:list')

    def get(self, request, *args, **kwargs):
        try:
            publication = Publication.objects.get(pk=request.GET['id'])
            messages.warning(request, '<b>{}</b> wurde gelöscht.'.format(publication.title), extra_tags='delete')
            publication.delete()
            return HttpResponseRedirect(reverse_lazy('IKVpublication:list'))
        except:
            pass
        return super(PublicationUpdateView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PublicationUpdateView, self).get_context_data(**kwargs)
        context['publication'] = Publication.objects.all()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        return super(PublicationUpdateView, self).form_valid(form)


class SettingsAuthor(FormView):
    form_class = AuthorForm
    model = Author
    template_name = 'IKVpublication/settings_author.html'
    success_url = '#'

    def get(self, request, *args, **kwargs):
        try:
            author = Author.objects.get(pk=request.GET['id'])
            messages.warning(request, '<b>{} {}</b> wurde gelöscht.'.format(author.firstname, author.lastname), extra_tags='delete')
            author.delete()
        except:
            pass

        return super(SettingsAuthor, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(SettingsAuthor, self).get_context_data(*args, **kwargs)
        context['author'] = Author.objects.all()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form.save()
        messages.success(self.request, '<b>{} {}</b> wurde erstellt'.format(self.request.POST['firstname'], self.request.POST['lastname']), extra_tags='created')
        return super(SettingsAuthor, self).form_valid(form)


class SettingsJournal(FormView):
    form_class = JournalForm
    model = Journal
    template_name = 'IKVpublication/settings_journal.html'
    success_url = '#'

    def get(self, request, *args, **kwargs):
        try:
            journal = Journal.objects.get(pk=request.GET['id'])
            messages.warning(request, '<b>{}</b> wurde gelöscht.'.format(journal.name), extra_tags='delete')
            journal.delete()
        except:
            pass

        return super(SettingsJournal, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(SettingsJournal, self).get_context_data(*args, **kwargs)
        context['journal'] = Journal.objects.all()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form.save()
        messages.success(self.request, '<b>{}</b> wurde erstellt'.format(self.request.POST['name']), extra_tags='created')
        return super(SettingsJournal, self).form_valid(form)
