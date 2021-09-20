from django.db import models
from django.urls import reverse


# Create your models here.
class Publication(models.Model):
    publicproject_id = models.ForeignKey('IKVpublic.Public', on_delete=models.CASCADE, verbose_name='Öffentliches Projekt', blank=True, null=True)
    assistant_id = models.ManyToManyField('IKVassistant.Assistant', verbose_name='Assistent', blank=True)
    author_id = models.ManyToManyField('Author', verbose_name='Weitere Autoren', blank=True)
    title = models.CharField(max_length=400, verbose_name='Titel')
    journal = models.ForeignKey('Journal', on_delete=models.CASCADE, verbose_name='Journal')

    STATUS =[
        ('PL', 'geplant'),
        ('CR', 'eingereicht'),
        ('GO', 'erschienen'),
    ]

    REV = [
        ('revj', 'rez. Journal'),
        ('jour', 'Zeitschrift'),
        ('revc', 'rez. Konferenz'),
        ('conf', 'Konferenz'),
        ('othe', 'Sonstige'),
    ]
    status = models.CharField(max_length=2, verbose_name='Status', choices=STATUS)
    reviewed = models.CharField(max_length=4, verbose_name='Art der Veröffentlichung', choices=REV)
    release_date = models.DateField(verbose_name='Erscheinungsdatum')

    def get_absolute_url(self):
        return reverse('IKVpublication:list')

    def __str__(self):
        return str(self.title)
    
    class Meta:
        verbose_name = 'Veröffentlichung'
        verbose_name_plural = 'Veröffentlichungen'


class Author(models.Model):
    firstname = models.CharField(max_length=200, verbose_name='Vorname')
    lastname = models.CharField(max_length=200, verbose_name='Nachname')

    def __str__(self):
        return str(self.lastname) + ', ' + str(self.firstname[0]) + '.'

    class Meta:
        verbose_name = 'Weiterer Autor'
        verbose_name_plural = 'Weitere Autoren'


class Journal(models.Model):
    name = models.CharField(max_length=400, verbose_name='Journal')

    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name = 'Journal'
        verbose_name_plural = 'Journals'