from django.db import models
from django.urls import reverse


# Create your models here.
class Global(models.Model):
    year = models.IntegerField(verbose_name = 'Jahr')
    industry_goal = models.DecimalField(max_digits=10, decimal_places=2)
    is_current = models.BooleanField(editable=False, default=False)

    def get_absolute_url(self):
        return reverse('index')

    def __str__(self):
        return str(self.year)
    
    class Meta:
        verbose_name = 'Jahr'
        verbose_name_plural = 'Jahre'