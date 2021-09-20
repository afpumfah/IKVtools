from django.db import models

# Create your models here.

class Protocol(models.Model):
    public_project_id = models.ForeignKey('IKVpublic.Public', on_delete=models.CASCADE, verbose_name='Öffentliches Projekt', blank=True, null=True)
    industry_project_id = models.ForeignKey('IKVindustry.Industry', on_delete=models.CASCADE, verbose_name='Industrieprojekt', blank=True, null=True)
    title = models.CharField(max_length=200, verbose_name='Titel')
    place = models.CharField(max_length=200, verbose_name='Ort')
    date = models.DateField(verbose_name='Wann', blank=True, null=True)
    assistant_id = models.ManyToManyField('IKVassistant.Assistant', verbose_name='Assistent', blank=True)
    content = models.TextField(verbose_name='Protokol')


class ToDo(models.Model):
    protocol_id = models.ForeignKey('Protocol', on_delete=models.CASCADE, verbose_name='ToDo')
    assistant_id = models.ForeignKey('IKVassistant.Assistant', on_delete=models.CASCADE, verbose_name='Wer?')
    title = models.CharField(max_length=400, verbose_name='Was?')
    duedate = models.DateField(verbose_name='Fällig am')
    done = models.BooleanField(verbose_name='erledigt', default=False)
