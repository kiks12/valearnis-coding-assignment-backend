# Generated by Django 4.2.6 on 2023-10-26 01:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_question_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]