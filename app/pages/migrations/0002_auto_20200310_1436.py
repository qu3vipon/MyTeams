# Generated by Django 2.2.10 on 2020-03-10 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='match',
            options={'ordering': ['datetime'], 'verbose_name': 'match', 'verbose_name_plural': 'matches'},
        ),
        migrations.AddIndex(
            model_name='match',
            index=models.Index(fields=['datetime'], name='pages_match_datetim_3922fd_idx'),
        ),
    ]