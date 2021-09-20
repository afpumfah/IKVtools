from django.db import models
from django.urls import reverse

from datetime import date

# Create your models here.

class Assistant(models.Model):
    STATUS = [
        ('AC', 'Aktiv'),
        ('ALU', 'Alumni'),
        ('PL', 'Geplant'),
        ('IC', 'Inaktiv'),
    ]

    firstname = models.CharField(max_length=200, verbose_name='Vorname')
    lastname = models.CharField(max_length=200, verbose_name='Nachname')
    email = models.EmailField(max_length=250, verbose_name = 'Email')
    phone = models.IntegerField(verbose_name = 'Telefonnummer')
    birth = models.DateField(verbose_name='Geburtstag')
    start = models.DateField(verbose_name='Einstieg')
    end = models.DateField(verbose_name='Ausstieg')
    added = models.DateField(verbose_name='Letzte Änderung', editable=False)
    status = models.CharField(max_length=3, verbose_name='Status', choices=STATUS)

    def save(self, *args, **kwargs):
        self.added = date.today()
        return super(Assistant, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('IKVassistant:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.lastname
    
    class Meta:
        verbose_name = 'Assistent'
        verbose_name_plural = 'Assistenten'


def assistant_path(instance, filename):
    return "IKVassistant/{}/{}".format(instance.assistant_id.id, filename)


class AssistantFiles(models.Model):
    assistant_id = models.ForeignKey('Assistant', on_delete=models.CASCADE)
    file = models.FileField(upload_to=assistant_path, verbose_name='Datei')
    description = models.CharField(max_length=200, verbose_name='Beschreibung')
        
    def __str__(self):
        return str(self.file)

    class Meta:
        verbose_name = 'Assistent Datei'
        verbose_name_plural = 'Assistent Dateien'