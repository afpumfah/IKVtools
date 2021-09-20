from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.contrib import messages

from .models import Protocol, ToDo
from .forms import ProtocolForm, ProtocolFormSet


class ProtocolListView(FormView):
    template_name = 'IKVprotocol/protocol_list.html'
    form_class = ProtocolForm
    success_url = '#'

    def get(self, request, *args, **kwargs):
        try:
            protocol = Protocol.objects.get(pk=request.GET['id'])
            messages.warning(request, '<b>{}</b> wurde gelöscht.'.format(protocol.title), extra_tags='delete')
            protocol.delete()
        except:
            pass
        return super().get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['protocol'] = Protocol.objects.all()
        return context

    def form_valid(self, form):
        buf = form.save()
        messages.success(self.request, '<b>{}</b> wurde erstellt.'.format(self.request.POST['title']), extra_tags='created')
        return redirect('IKVprotocol:update', pk=buf.pk)


class ProtocolUpdateView(UpdateView):
    model = Protocol
    form_class = ProtocolForm
    template_name = 'IKVprotocol/protocol_update.html'
    success_url = '#'

    def get(self, request, *args, **kwargs):
        try:
            protocol = Protocol.objects.get(pk=request.GET['id'])
            messages.warning(request, '<b>{}</b> wurde gelöscht.'.format(protocol.title), extra_tags='delete')
            protocol.delete()
            return redirect('IKVprotocol:list')
        except:
            pass

        return super().get(request, *args, **kwargs)
    

    def get_context_data(self, **kwargs):
        context = super(ProtocolUpdateView, self).get_context_data(**kwargs)
        context['protocol'] = Protocol.objects.all()

        if self.request.POST:
            context['todo'] = ProtocolFormSet(self.request.POST, instance=self.object)
        else:
            context['todo'] = ProtocolFormSet(instance=self.object)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        todo = context['todo']
        if todo.is_valid():
            todo.save()
            form.save()
            return redirect('IKVprotocol:update', pk=self.object.pk)
        return super(ProtocolUpdateView, self).form_valid(form)