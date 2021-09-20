from django.db import models
from django.urls import reverse

class Student(models.Model):

    firstname = models.CharField(max_length=200, verbose_name='Vorname')
    lastname = models.CharField(max_length=200, verbose_name='Nachname')

    def __str__(self):
        return self.lastname

    def get_absolute_url(self):
        return reverse('IKVstudents:list')

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Studenten'


class StudentAssistant(models.Model):
    STATUS = [
        ('SHK', 'SHK'),
        ('WHB', 'WHB'),
    ]
    
    student_id = models.ForeignKey('Student', on_delete=models.CASCADE, verbose_name='Student')
    assistant_id = models.ForeignKey('IKVassistant.Assistant', on_delete=models.CASCADE, verbose_name='Assistent')
    status = models.CharField(max_length=3, verbose_name='Status', choices=STATUS)
    hours = models.IntegerField(verbose_name='Stunden pro Woche')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    start = models.DateField(verbose_name='Start')
    end = models.DateField(verbose_name='Ende')

    def __str__(self):
        return self.student_id.lastname

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Studenten'


class Thesis(models.Model):
    TYPE = [
        ('MA', 'Masterarbeit'),
        ('BA', 'Bachelorarbeit'),
        ('PA', 'Projektarbeit'),
        ('FL', 'Forschungslabor'),
    ]

    student_id = models.ForeignKey('Student', on_delete=models.CASCADE, verbose_name='Student')
    supervisor_id = models.ManyToManyField('IKVassistant.Assistant', verbose_name="Betreuer")
    title = models.CharField(max_length=400, verbose_name='Titel')
    type = models.CharField(max_length=2, verbose_name='Art der Arbeit', choices=TYPE, blank=True)
    release_date = models.DateField(verbose_name='Erscheinungsdatum', null=True, blank=True)


class MeanPrice(models.Model):
    mean_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Mittlerer Finanzierungswert", default=0)
    shk_07 = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    shk_08 = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    shk_09 = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    shk_10 = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    shk_11 = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    shk_12 = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    shk_13 = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    shk_14 = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    shk_15 = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    shk_16 = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    shk_17 = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    shk_18 = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    shk_19 = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    whk_07 = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    whk_08 = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    whk_09 = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    whk_10 = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    whk_11 = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    whk_12 = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    whk_13 = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    whk_14 = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    whk_15 = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    whk_16 = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    whk_17 = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    whk_18 = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    whk_19 = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return str(self.mean_price)
