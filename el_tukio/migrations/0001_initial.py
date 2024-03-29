# Generated by Django 4.1.1 on 2022-09-14 14:57

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.SmallIntegerField(blank=True, choices=[(None, '(Unkown)'), (0, 'Organizer'), (1, 'Planner'), (3, 'Vendor')], null=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, unique=True)),
                ('profile', models.ImageField(default='default.jpg', upload_to='profile_pics')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='VendorCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Select a category (EG: Venues)', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='Organizer', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('bookmarks', models.ManyToManyField(blank=True, null=True, related_name='organizer_bookmarks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='Vendor', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('business_name', models.CharField(max_length=100)),
                ('description', models.TextField(help_text='Brief description of your business', max_length=5000)),
                ('services_offered', models.TextField(help_text='List the particular services your business offers', max_length=5000)),
                ('city', models.CharField(help_text='City in which your business is located', max_length=100)),
                ('location', models.CharField(help_text='EG: Ole Sangale Rd, Madaraka', max_length=200)),
                ('open_hours', models.CharField(default='24/7', help_text='Business service (working) times', max_length=500)),
                ('up_for_business', models.BooleanField(default=True, help_text='Ready to take business at the moment?')),
                ('category', models.ForeignKey(blank=True, help_text='Select a category for your business.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='el_tukio.vendorcategory')),
            ],
        ),
        migrations.CreateModel(
            name='VendorImageUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='vendor_img_uploads')),
                ('caption', models.CharField(blank=True, max_length=500, null=True)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='el_tukio.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(help_text='Your comment on the business services', max_length=500)),
                ('stars', models.SmallIntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('rated_user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='rated_planner_or_vendor', to=settings.AUTH_USER_MODEL)),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='el_tukio.organizer')),
            ],
        ),
        migrations.CreateModel(
            name='Planner',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='Planner', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('description', models.TextField(help_text='Brief description of your business', max_length=5000)),
                ('services_offered', models.TextField(help_text='List the particular services your business offers', max_length=5000)),
                ('city', models.CharField(help_text='Primary (Current) city of residence', max_length=100)),
                ('location', models.CharField(help_text='EG: Ole Sangale Rd, Madaraka', max_length=200)),
                ('up_for_business', models.BooleanField(default=True, help_text='Ready to take business at the moment?')),
                ('bookmarks', models.ManyToManyField(blank=True, null=True, related_name='planner_bookmarks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=100)),
                ('event_date', models.DateField(help_text='When will this event be held?')),
                ('event_budget', models.FloatField(help_text='What  is the budget for this event')),
                ('event_location', models.CharField(blank=True, max_length=100, null=True)),
                ('guest_size', models.IntegerField(help_text='Expected number of guests at the event')),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='el_tukio.organizer')),
                ('planners', models.ManyToManyField(blank=True, null=True, to='el_tukio.planner')),
                ('vendors', models.ManyToManyField(blank=True, null=True, to='el_tukio.vendor')),
            ],
        ),
    ]
