# Generated by Django 4.1.2 on 2022-11-07 11:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('el_tukio', '0012_expense_check_total_cost_vs_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='date_deleted',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='expense',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='task',
            name='date_deleted',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/')),
                ('date_uploaded', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=500)),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='expense',
            name='comments',
            field=models.ManyToManyField(related_name='expense_comments', to='el_tukio.comment'),
        ),
        migrations.AddField(
            model_name='expense',
            name='files',
            field=models.ManyToManyField(related_name='expense_files', to='el_tukio.fileupload'),
        ),
        migrations.AddField(
            model_name='task',
            name='comments',
            field=models.ManyToManyField(related_name='task_comments', to='el_tukio.comment'),
        ),
        migrations.AddField(
            model_name='task',
            name='files',
            field=models.ManyToManyField(related_name='task_files', to='el_tukio.fileupload'),
        ),
    ]