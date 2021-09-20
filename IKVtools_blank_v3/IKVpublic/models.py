from django.db import models
from django.urls import reverse

from datetime import date
from PIL import Image

# Create your models here.
class Public(models.Model):

    STATUS = [
        ('ID', 'Idee'),
        ('CR', 'beantragt'),
        ('GO', 'laufend'),
        ('END', 'beendet'),
        ('DD', 'abgelehnt'),
        ('PL', 'geplant'),
        ('PO', 'Post-AL'),
        ('AC', 'bewilligt'),
    ]

    fanr = models.CharField(max_length=200, verbose_name='FA-Nummer')
    financier = models.ForeignKey('Financier', on_delete=models.CASCADE, verbose_name="Geldgeber", null=True, blank=True)
    project_number = models.CharField(max_length=200, verbose_name='Förderkennzeichen')
    title = models.CharField(max_length=200, verbose_name='Titel')
    short_title = models.CharField(max_length=200, verbose_name='Kurztitel')
    added = models.DateField(verbose_name='Letzte Änderung', editable=False)
    start = models.DateField(verbose_name='Projektstart')
    end = models.DateField(verbose_name='Projektende')
    al_date = models.DateField(verbose_name='AL-Datum', null=True, blank=True)
    gl_date = models.DateField(verbose_name='GL-Datum', null=True, blank=True)
    status = models.CharField(max_length=3, verbose_name='Status', choices=STATUS)
    funded_position = models.FloatField(verbose_name='Finanzierte Stellen')
    funded_students = models.FloatField(verbose_name='Finanzierte HiWis')
    summary = models.TextField(verbose_name='Zusammenfassung', default='Noch keine Zusammenfassung erstellt')

    def get_absolute_url(self):
        return reverse("IKVpublic:detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.short_title

    def save(self, *args, **kwargs):
        self.added = date.today()
        return super(Public, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Öffentliches Projekt'
        verbose_name_plural = 'Öffentliche Projekte'


class PublicAssistant(models.Model):
    project_id = models.ForeignKey('Public', on_delete=models.CASCADE, verbose_name='Projekt')
    assistant_id = models.ForeignKey('IKVassistant.Assistant', on_delete = models.CASCADE, verbose_name='Bearbeiter')
    start = models.DateField(verbose_name='Start Assistent')
    end = models.DateField(verbose_name='Ende Assistent')

    def __str__(self):
        return str(self.project_id)

    class Meta:
        verbose_name = 'Bearbeiter'
        verbose_name_plural = 'Bearbeiter'


def public_path(instance, filename):
    return "IKVpublic/{}/{}".format(instance.project_id.id, filename)


class PublicFiles(models.Model):
    project_id = models.ForeignKey('Public', on_delete = models.CASCADE)
    file = models.FileField(upload_to=public_path, verbose_name = 'Datei')
    description = models.CharField(max_length = 200, verbose_name = 'Beschreibung')

    def __str__(self):
        return str(self.file)

    class Meta:
        verbose_name = 'Öffentliches Projekt Datei'
        verbose_name_plural = 'Öffentliches Projekt Dateien'


class PublicWorkPackage(models.Model):
    project_id = models.ForeignKey('Public', on_delete=models.CASCADE, verbose_name='Projekt')
    title = models.CharField(max_length=200, verbose_name='Titel')
    start = models.DateField(verbose_name='Arbeitspaket (Start)')
    end = models.DateField(verbose_name='Arbeitspaket (Ende)')

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Arbeitspaket'
        verbose_name_plural = 'Arbeitspakete'

def image_path(instance, filename):
    return "static/financier/{}".format(filename)

class Financier(models.Model):
    name = models.CharField(max_length=200, verbose_name='Geldgeber')
    image = models.ImageField(upload_to=image_path, verbose_name='Logo', width_field='width', height_field='height')
    width = models.IntegerField(editable=False, default=100)
    height = models.IntegerField(editable=False, default=100)
    color = models.CharField(max_length=7, verbose_name='Farbe', default='#FFFFFF')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Financier, self).save(*args, **kwargs)
        imag = Image.open(self.image.path)
        if imag.width > 400 or imag.height> 300:
            output_size = (300, 300)
            imag.thumbnail(output_size)
            imag.save(self.image.path)

    class Meta:
        verbose_name = 'Geldgeber'
        verbose_name_plural = 'Geldgeber'