from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

import datetime as DT
from el_tukio.models import *


def vendor_categories():
    return VendorCategory.objects.all().values_list('id', 'name')


class VendorRegForm(UserCreationForm):
    """Vendor registration form"""
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)

    business_name = forms.CharField(required=True)
    category = forms.ChoiceField(
        required=True,
        choices=vendor_categories(),
    )
    description = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'rows': 5,
            'cols': 30,
        }))
    services_offered = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'rows': 5,
            'cols': 30,
        }))
    city = forms.CharField(required=True)
    location = forms.CharField(required=True)  # street code

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type = User.UserType.VENDOR
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.email = self.cleaned_data['email']
        user.save()

        vendor = Vendor.objects.create(
            user=user,
            business_name=self.cleaned_data['business_name'],
            category_id=self.cleaned_data['category'],
            description=self.cleaned_data['description'],
            services_offered=self.cleaned_data['services_offered'],
            city=self.cleaned_data['city'],
            location=self.cleaned_data['location']
        )
        vendor.save()
        return user


class OrganizerRegForm(UserCreationForm):
    """Event organizer registration form"""
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)
    account_type = forms.ChoiceField(required=True, choices=User.AccountType.choices)
    
    event_name = forms.CharField(required=True)
    event_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'min': DT.date.today(),
        }),
    )
    event_budget = forms.FloatField(required=True, min_value=0)
    event_location = forms.CharField(required=False)
    guest_size = forms.IntegerField(required=True, min_value=0)

    # location
    business_name = forms.CharField(required=False)
    route = forms.CharField(required=False)
    neighbourhood = forms.CharField(required=False)
    city = forms.CharField(required=False)
    county = forms.CharField(required=False)
    country = forms.CharField(required=False)
    postal_code = forms.CharField(required=False)
    longitude = forms.FloatField(required=False)
    latitude = forms.FloatField(required=False)
    maps_url = forms.CharField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type = User.UserType.ORGANIZER
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.email = self.cleaned_data['email']
        user.save()

        organizer = Organizer.objects.create(user=user)
        organizer.save()

        event = Event.objects.create(
            organizer=organizer,
            event_name=self.cleaned_data['event_name'],
            event_date=self.cleaned_data['event_date'],
            event_budget=self.cleaned_data['event_budget'],
            event_location=self.cleaned_data['event_location'],
            guest_size=self.cleaned_data['guest_size']
        )
        event.save()
        return user


class PlannerRegForm(UserCreationForm):
    """Event planner registration form"""
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)
    description = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'rows': 5,
            'cols': 30,
        }))
    services_offered = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'rows': 5,
            'cols': 30,
        }))
    city = forms.CharField(required=True)
    location = forms.CharField(required=True)  # street code

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type = User.UserType.PLANNER
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.email = self.cleaned_data['email']
        user.save()

        planner = Planner.objects.create(
            user=user,
            description = self.cleaned_data['description'],
            services_offered = self.cleaned_data['services_offered'],
            city = self.cleaned_data['city'],
            location = self.cleaned_data['location']
        )
        planner.save()
        return user


class UserAccountForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'profile']



class UsernameUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']


class FullNameUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class EmailUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']


class PasswordUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['password']


class BusinessProfileForm(ModelForm):
    class Meta:
        model = Vendor
        fields = ['business_name', 'category', 'description', 'services_offered', 'city', 'location', 'open_hours', 'up_for_business']


class VendorImageUploadForm(ModelForm):
    class Meta:
        model = VendorImageUpload
        fields = ['image', 'caption']


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['event_name', 'event_date', 'event_budget', 'event_location', 'guest_size']
        widgets = {
            'event_date': forms.DateInput(attrs={
                'type': 'date',
                'min': DT.date.today(),
            }),
        }


class ContractForm(ModelForm):
    class Meta:
        model = Contract
        fields = ['event', 'contract', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'row': 5,
                'col': 30,
            })
        }


class TaskForm(ModelForm):
    """Create new task form"""
    def __init__(self, *args, **kwargs):
        event_date = kwargs.pop('event_date')
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['due_date'] = forms.DateField(
            required=False,
            widget=forms.DateInput(attrs={
                'type': 'date',
                'min': DT.date.today(),
                'max': event_date,
            }))

    class Meta:
        model = Task
        fields = ['task', 'due_date']


class TaskContentUpdateForm(ModelForm):
    class Meta:
        model = Task
        fields = ['task']


class TaskDueDateUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        event_date = kwargs.pop('event_date')
        super(TaskDueDateUpdateForm, self).__init__(*args, **kwargs)
        self.fields['due_date'] = forms.DateField(
            required=False,
            widget=forms.DateInput(attrs={
                'type': 'date',
                'min': DT.date.today(),
                'max': event_date,
            }))

    class Meta:
        model = Task
        fields = ['due_date']


class TaskGroupForm(ModelForm):
    class Meta:
        model = TaskGroup
        fields = ['name']


class ExpenseCategoryForm(ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ['name']


class ExpenseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # pop out extra/custom args
        if 'exp_categories' in kwargs:
            exp_categories = kwargs.pop('exp_categories')

        # initialize form
        super(ExpenseForm, self).__init__(*args, **kwargs)

        # check if local var exists
        if 'exp_categories' in locals():
            self.fields['expense_category'] = forms.ChoiceField(
                required=False,
                choices=exp_categories
            )

    class Meta:
        model = Expense
        fields = ['description', 'expense_category', 'total_cost']


class ExpenseUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        if 'exp_categories' in kwargs:
            exp_categories = kwargs.pop('exp_categories')
        super(ExpenseUpdateForm, self).__init__(*args, **kwargs)
        if 'exp_categories' in locals():
            self.fields['expense_category'] = forms.ChoiceField(
                required=False,
                choices=exp_categories
            )
    class Meta:
        model = Expense
        fields = ['description', 'expense_category', 'total_cost', 'total_paid']


class ChatMessageForm(ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['message']
