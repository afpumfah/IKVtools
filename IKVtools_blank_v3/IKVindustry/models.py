from django.db import models
from django.urls import reverse

from decimal import Decimal
from datetime import date

from IKVpublication.models import Publication

from datetime import datetime

# Create your models here.
class Industry(models.Model):

    RD = [
        ('RD', 'F&E'),
        ('S', 'Routine')
    ]

    STATUS = [
        ('CR', 'angelegt'),
        ('GO', 'laufend'),
        ('END', 'beendet'),
        ('DD', 'nicht beauftragt')
    ]

    fanr = models.CharField(max_length=200, verbose_name='FA-Nummer')
    company = models.CharField(max_length=200, verbose_name='Firma')
    title = models.CharField(max_length=200, verbose_name='Titel')
    short_title = models.CharField(max_length=200, verbose_name='Kurztitel')
    kind = models.CharField(max_length=200, verbose_name='Art', choices=RD)
    finish_finance_a = models.DateField(verbose_name='Ende Buchhaltung (Assistent)', null=True)
    finish_finance_al = models.DateField(verbose_name='Ende Buchhaltung (Abteilungsleiter)', null=True)
    finish_finance_s = models.DateField(verbose_name='Ende Buchhaltung (Studenten)', null=True)
    added = models.DateField(verbose_name='Letzte Änderung', editable=False)
    status = models.CharField(max_length=3, verbose_name='Status', choices=STATUS)

    #financial part
    sum_wp_instruct = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Summe beauftragter Arbeitspakte', default=0, editable=False)
    sum_wp_invoiced = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Summe fakturierter Arbeitspakte', default=0, editable=False)
    sum_wp = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Summe Arbeitspakte', default=0, editable=False)
    
    released = models.BooleanField(verbose_name='Projektgelder freigegeben', default=False)

    al_budget = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='AL-Budget', default=0, editable=False)
    al_budget_spent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ausgegebenes AL-Budget', default=0, editable=False)
    al_budget_left = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Verbleibendes Assistenten Budget', default=0, editable=False)
    
    assi_budget = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Assistenten Budget', default=0, editable=False)
    assi_budget_spent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ausgegebenes Assistenten Budget', default=0, editable=False)
    assi_budget_left = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Verbleibendes Assistenten Budget', default=0, editable=False)

    students_budget = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Studenten Budget', default=0, editable=False)


    def save(self, *args, **kwargs):
        self.added = date.today()
        work_package = WorkPackage.objects.filter(project_id = self.pk).exclude(foreign = True)
        self.sum_wp_instruct = 0
        self.sum_wp_invoiced = 0
        self.al_budget = 0
        self.assi_budget = 0
        self.students_budget = Decimal(0)
        for wp in work_package:
            if wp.instruct_at and not wp.invoiced_at:
                self.sum_wp_instruct += wp.price
            elif wp.instruct_at and wp.invoiced_at:
                self.sum_wp_invoiced += wp.price
        if self.released:
            for wp in work_package:
                if wp.instruct_at != None:
                    self.al_budget += wp.al_budget
                    self.assi_budget += wp.assi_material_budget
                    self.students_budget += wp.assi_students_budget
        self.sum_wp = self.sum_wp_instruct + self.sum_wp_invoiced

        spent = Outgoings.objects.filter(project_id = self.pk)
        self.al_budget_spent = 0
        self.assi_budget_spent = 0
        self.al_budget_left = 0
        self.assi_budget_left = 0
        if self.released:
            for out in spent:
                if out.kind == 'AL':
                    self.al_budget_spent += out.price
                elif out.kind == 'A':
                    self.assi_budget_spent += out.price
            self.al_budget_left = self.al_budget - self.al_budget_spent
            self.assi_budget_left = self.assi_budget - self.assi_budget_spent


        return super(Industry, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("IKVindustry:detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.fanr + ' - ' + self.short_title

    class Meta:
        verbose_name = 'Industrieprojekt'
        verbose_name_plural = 'Industrieprojekte'


class WorkPackage(models.Model):
    project_id = models.ForeignKey('Industry', on_delete=models.CASCADE, verbose_name='Projekt')
    assistant_id = models.ForeignKey('IKVassistant.Assistant', on_delete=models.CASCADE, verbose_name='Bearbeiter')
    title = models.CharField(max_length=200, verbose_name='Titel')
    material = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Material [%]', default=17.5)
    staff = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Personal [%]', default=17.5)
    foreign = models.BooleanField(verbose_name='Fremdleistung', default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Teilschrittvolumen')
    instruct_at = models.DateField(verbose_name='Beauftragt am', null=True, blank=True)
    invoiced_at = models.DateField(verbose_name='Fakturiert am',  null=True, blank=True)
    al_budget = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='AL-Budget', default=0, editable=False)
    assi_material_budget = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Assistenten Materialbudget', default=0, editable=False)
    assi_students_budget = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Assistenten Studentenbudget', default=0, editable=False)

    def save(self, *args, **kwargs):
        if self.foreign == False:
            self.al_budget = self.price * Decimal(.1)
            self.assi_material_budget = Decimal(self.price * self.material / 100)
            self.assi_students_budget = Decimal(self.price * self.staff / 100)
        else:
            self.al_budget = Decimal(0)
            self.assi_material_budget = Decimal(0)
            self.assi_students_budget = Decimal(0)

        return super(WorkPackage, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Teilschritt"
        verbose_name_plural = "Teilschritte"


def industry_path(instance, filename):
    return "IKVindustry/{}/{}".format(instance.project_id.id, filename)


class IndustryFiles(models.Model):
    project_id = models.ForeignKey('Industry', on_delete = models.CASCADE)
    file = models.FileField(upload_to=industry_path, verbose_name = 'Datei')
    description = models.CharField(max_length = 200, verbose_name = 'Beschreibung')

    def __str__(self):
        return str(self.file)

    class Meta:
        verbose_name = "Industrie Datei"
        verbose_name_plural = "Industrie Dateien"


class Outgoings(models.Model):
    project_id = models.ForeignKey('Industry', on_delete=models.CASCADE, verbose_name='Projekt')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ausgaben inkl. MwSt:')
    description = models.TextField(max_length=200, verbose_name='Beschreibung')
    added = models.DateField(verbose_name='Hinzugefügt', editable=False)
    
    AAL = [
        ('AL', 'AL-Budget'),
        ('A', 'Assistenten Budget'),
    ]

    kind = models.CharField(max_length=2, verbose_name='Budget', choices=AAL)

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        self.added = date.today()
        return super(Outgoings, self).save(*args, **kwargs)
