from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator

import datetime as DT

from setup.settings import LOGIN_URL, HOME_URL
from el_tukio.models import User, Planner, Vendor, Contract, Event
from el_tukio.forms import UsernameUpdateForm, FullNameUpdateForm, EmailUpdateForm, PasswordUpdateForm, ContractForm
from el_tukio.utils.decorators import planner_or_organizer_required, planner_or_vendor_required
from el_tukio.utils.main import print_form_values


def index(request):
    return render(request, 'main/index.html')


def register(request):
    return render(request, 'main/register/index.html')


def user_login(request):
    if not request.method == 'POST':
        if request.user.is_authenticated:
            messages.info(request, 'You are already logged in!')
            return redirect(request.META.get('HTTP_REFERER', '/'))

        login_form = AuthenticationForm()
        return render(request, 'main/login.html', context={'form': login_form})

    form = AuthenticationForm(data=request.POST)
    if not form.is_valid():
        # messages.error(request, form.errors)
        messages.error(request, 'Invalid username or password!')
        print('\n\nLogin Form invalid!\n\n')
        return redirect(LOGIN_URL)

    username = form.cleaned_data['username']
    password = form.cleaned_data['password']
    user = authenticate(username=username, password=password)

    if (user is None):
        print('\n\nUser = null!\n\n')
        messages.error(request, 'Invalid username or password!')
        return redirect(LOGIN_URL)

    login(request, user)
    messages.success(request, 'Login successful')

    if user.is_organizer:
        return redirect('organizer-dashboard')

    if user.is_planner:
        return redirect('planner-dashboard')

    if user.is_vendor:
        return redirect('vendor-dashboard')

    if user.is_superuser:
        return redirect('admin:index')


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect(HOME_URL)


@login_required
def user_account(request):
    return render(request, 'main/user-account.html')


@method_decorator(login_required, name='dispatch')
class UsernameUpdate(UpdateView):
    form_class = UsernameUpdateForm
    template_name = 'main/update/username.html'

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Username updated!')
        return redirect('user-account')


@method_decorator(login_required, name='dispatch')
class NameUpdate(UpdateView):
    form_class = FullNameUpdateForm
    template_name = 'main/update/fullname.html'

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Name updated!')
        return redirect('user-account')


@method_decorator(login_required, name='dispatch')
class EmailUpdate(UpdateView):
    form_class = EmailUpdateForm
    template_name = 'main/update/email.html'

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Email updated!')
        return redirect('user-account')


@method_decorator(login_required, name='dispatch')
class PasswordUpdate(UpdateView):
    form_class = PasswordUpdateForm
    template_name = 'main/update/password.html'

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Password updated!')
        return redirect('user-account')


def planners(request):
    context = {'planners': Planner.objects.all()}
    return render(request, 'main/planners.html', context)


def planner_details(request, planner_id):
    context = {'seller' : Planner.objects.get(user_id=planner_id)}
    return render(request, 'main/seller-details.html', context)


def vendors(request):
    context = {'vendors': Vendor.objects.all()}
    return render(request, 'main/vendors.html', context)


def vendor_details(request, vendor_id):
    context = {'seller' : Vendor.objects.get(user_id=vendor_id)}
    return render(request, 'main/seller-details.html', context)


@planner_or_organizer_required
def bookmark(request, user_id):
    bookmark = User.objects.get(pk=user_id)
    if(request.user.is_organizer):
        request.user.organizer.bookmarks.add(bookmark)
        messages.success(request, 'User bookmarked')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    elif(request.user.is_planner):
        request.user.planner.bookmarks.add(bookmark)
        messages.success(request, 'User bookmarked')
        return redirect(request.META.get('HTTP_REFERER', '/'))

    messages.warning(request, 'User NOT bookmarked')
    return redirect(request.META.get('HTTP_REFERER', '/'))


@planner_or_organizer_required
def remove_bookmark(request, user_id):
    bookmark = User.objects.get(pk=user_id)
    if (request.user.is_organizer):
        request.user.organizer.bookmarks.remove(bookmark)
        messages.success(request, 'Bookmark removed!')
        return redirect(request.META.get('HTTP_REFERER', '/'))

    elif (request.user.is_planner):
        request.user.planner.bookmarks.remove(bookmark)
        messages.success(request, 'Bookmark removed!')
        return redirect(request.META.get('HTTP_REFERER', '/'))

    messages.warning(request, 'Bookmark NOT removed!')
    return redirect(request.META.get('HTTP_REFERER', '/'))


@planner_or_organizer_required
def bookmarks(request, user_type):
    context = {}
    bookmarked_ids = list()
    if (request.user.is_organizer):
        bookmarked_ids = list(request.user.organizer.bookmarks.all().values('id'))

    elif (request.user.is_planner):
        bookmarked_ids = list(request.user.planner.bookmarks.all().values('id'))

    bookmarked_ids = tuple([x['id'] for x in bookmarked_ids])
    context['bookmarks'] = list(Planner.objects.filter(user_id__in=bookmarked_ids))
    context['bookmarks'] += list(Vendor.objects.filter(user_id__in=bookmarked_ids))
    return render(request, 'main/bookmarks.html', context)


@planner_or_organizer_required
def hire_seller(request, user_id):
    if not request.method == 'POST':
        form = ContractForm()
        seller = User.objects.get(id=user_id)
        seller = Vendor.objects.get(user_id=user_id) if seller.is_vendor else Planner.objects.get(user_id=user_id)
        context = {'form': form, 'seller': seller}
        return render(request, 'main/hire-seller.html', context)

    form = ContractForm(request.POST)
    if not form.is_valid():
        messages.warning(request, 'Form NOT valid!')
        return redirect(request.META.get('HTTP_REFERER', '/'))

    contract = Contract.objects.create(
        event=form.cleaned_data['event'],
        contractor_id=request.user.id,
        contractee_id=user_id,
        terms=form.cleaned_data['terms']
    )
    contract.save()
    messages.success(request, 'Contract sent!')
    return redirect(request.META.get('HTTP_REFERER', '/'))


@planner_or_vendor_required
def current_deals(request, status='pending'):
    _status = Contract.Status[status.upper()]
    mydeals = Contract.objects.filter(contractee_id=request.user.id, status=_status)
    context = {'mydeals': mydeals, 'active': status}
    return render(request, 'main/current-deals.html', context)


@planner_or_vendor_required
def sign_contract(request, deal_id, action):
    if action in ['accept', 'decline']:
        contract = Contract.objects.get(id=deal_id)
        status = Contract.Status.ACCEPTED if action == 'accept' else Contract.Status.DECLINED
        date_signed = DT.datetime.now()
        contract.status = status
        contract.date_signed = date_signed
        contract.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))


def get_csrf(request):
    return JsonResponse({'csrf_token': get_token(request)}, status=200)
