# Generated by Django 4.1.2 on 2022-11-19 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('el_tukio', '0020_legaldocument_location_user_account_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='maps_url',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
