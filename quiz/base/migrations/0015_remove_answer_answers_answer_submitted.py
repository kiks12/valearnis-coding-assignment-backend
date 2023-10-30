# Generated by Django 4.2.6 on 2023-10-26 05:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_remove_submittedanswer_answer_answer_answers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='answers',
        ),
        migrations.AddField(
            model_name='answer',
            name='submitted',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submitted', to='base.submittedanswer'),
        ),
    ]