# Generated by Django 4.1.1 on 2022-09-24 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('el_tukio', '0005_alter_event_event_budget_alter_event_guest_size_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='date_signed',
            field=models.DateTimeField(blank=True, help_text='Time the contractee signs the contract', null=True),
        ),
    ]
