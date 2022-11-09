# Generated by Django 4.1.2 on 2022-11-07 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('el_tukio', '0011_expensecategory_expense'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='expense',
            constraint=models.CheckConstraint(check=models.Q(('total_cost__gte', models.F('total_paid'))), name='check_total_cost_vs_paid'),
        ),
    ]
