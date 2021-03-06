# Generated by Django 3.0.2 on 2020-07-17 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('IKVassistant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeanPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mean_price', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Mittlerer Finanzierungswert')),
                ('shk_07', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('shk_08', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('shk_09', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('shk_10', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('shk_11', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('shk_12', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('shk_13', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('shk_14', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('shk_15', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('shk_16', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('shk_17', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('shk_18', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('shk_19', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('whk_07', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('whk_08', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('whk_09', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('whk_10', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('whk_11', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('whk_12', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('whk_13', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('whk_14', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('whk_15', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('whk_16', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('whk_17', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('whk_18', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('whk_19', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=200, verbose_name='Vorname')),
                ('lastname', models.CharField(max_length=200, verbose_name='Nachname')),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Studenten',
            },
        ),
        migrations.CreateModel(
            name='Thesis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=400, verbose_name='Titel')),
                ('type', models.CharField(blank=True, choices=[('MA', 'Masterarbeit'), ('BA', 'Bachelorarbeit'), ('PA', 'Projektarbeit'), ('FL', 'Forschungslabor')], max_length=2, verbose_name='Art der Arbeit')),
                ('release_date', models.DateField(blank=True, null=True, verbose_name='Erscheinungsdatum')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IKVstudents.Student', verbose_name='Student')),
                ('supervisor_id', models.ManyToManyField(to='IKVassistant.Assistant', verbose_name='Betreuer')),
            ],
        ),
        migrations.CreateModel(
            name='StudentAssistant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('SHK', 'SHK'), ('WHB', 'WHB')], max_length=3, verbose_name='Status')),
                ('hours', models.IntegerField(verbose_name='Stunden pro Woche')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('start', models.DateField(verbose_name='Start')),
                ('end', models.DateField(verbose_name='Ende')),
                ('assistant_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IKVassistant.Assistant', verbose_name='Assistent')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IKVstudents.Student', verbose_name='Student')),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Studenten',
            },
        ),
    ]
