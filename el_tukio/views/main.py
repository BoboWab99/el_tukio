from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.db import transaction
from django.db.models import Q, F

import datetime as DT
import calendar as CAL

from setup.settings import LOGIN_URL, HOME_URL, GOOGLE_API_KEY
from el_tukio.models import *
from el_tukio.forms import *
from el_tukio.utils.decorators import *
from el_tukio.utils.main import *


def index(request):
    return render(request, 'main/index.html', {'google_api_key': GOOGLE_API_KEY})


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
    context = {'vendors': Planner.objects.all()}
    return render(request, 'main/vendors.html', context)


# def planner_details(request, planner_id):
#     context = {'seller' : Planner.objects.get(user_id=planner_id)}
#     return render(request, 'main/seller-details.html', context)


def vendors(request):
    context = {'vendors': Vendor.objects.all()}
    return render(request, 'main/vendors.html', context)


# def vendor_details(request, vendor_id):
#     context = {'seller' : Vendor.objects.get(user_id=vendor_id)}
#     return render(request, 'main/seller-details.html', context)

def seller_details(request, user_id):
    context = {}
    user = User.objects.get(id=user_id)
    if user.is_planner:
        context['seller'] = Planner.objects.get(user_id=user_id)
    elif user.is_vendor:
        context['seller'] = Vendor.objects.get(user_id=user_id)
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
        if request.user.is_organizer:
            context['events'] = Event.objects.filter(organizer_id=request.user.id)
        elif request.user.is_planner:
            context['events'] = Event.objects.filter(event_team__id=request.user.id)
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
    return redirect('seller-details', user_id)


@planner_or_vendor_required
def current_deals(request, status='accepted'):
    _status = Contract.Status[status.upper()]
    mydeals = Contract.objects.filter(contractee_id=request.user.id, status=_status)
    context = {'mydeals': mydeals, 'active': status}
    context['pending_count'] = Contract.objects.filter(
        contractee_id=request.user.id, status=Contract.Status.PENDING).count()
    context['accepted_count'] = Contract.objects.filter(
        contractee_id=request.user.id, status=Contract.Status.ACCEPTED).count()
    context['declined_count'] = Contract.objects.filter(
        contractee_id=request.user.id, status=Contract.Status.DECLINED).count()
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

        # add user to event team & chatroom
        if contract.is_accepted:
            contract.event.event_team.add(request.user)
            contract.event.chatroom.members.add(request.user)

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
@transaction.atomic
def event_chatroom(request, event_id, chat_with=None):
    if not request.method == 'POST':
        event = Event.objects.get(id=event_id)
        chat_with_user = None

        if chat_with:
            chat_with_user = User.objects.get(id=chat_with)

        if chat_with_user:
            chatroom_personal = ChatRoom.objects.filter(
                type=ChatRoom.Type.PERSONAL, 
                members__id=request.user.id
            ).filter(
                members__id=chat_with
            )
            if chatroom_personal:
                chatroom_personal = chatroom_personal[0]
            else:
                # create new personal chatroom
                chatroom = ChatRoom.objects.create(
                    name=f'{request.user} & {chat_with_user} chatroom',
                    type=ChatRoom.Type.PERSONAL
                )
                print('Personal chatroom created!')
                chatroom.members.add(request.user)
                chatroom.members.add(chat_with_user)
                chatroom_personal = chatroom

        # Make sure a chatroom is created for every new event
        if not event.chatroom:
            chatroom = ChatRoom.objects.create(
                name=f'{event.event_name} chatroom',
                type=ChatRoom.Type.GROUP
            )
            print('Event chatroom created!')
            chatroom.members.add(event.organizer.user)
            event_team = event.event_team.all()
            for member in event_team:
                chatroom.members.add(member)            
            event.chatroom = chatroom
            event.save()

        event_chatroom = ChatRoom.objects.get(id=event.chatroom_id)
        event_chatroom.members.add(event.organizer.user)
        message_form = ChatMessageForm()

        context = {
            'event': event,
            'event_chatroom': event_chatroom,
            'active_chatroom': event_chatroom,
            'message_form': message_form,
            'active': 'chat',
            'active_chat': 0,    #chat with everyone
            'active_chatroom_id': event_chatroom.id
        }

        if chat_with_user:
            context['active_chat'] = chat_with
            context['active_chatroom'] = chatroom_personal
        return render(request, 'main/chat.html', context)

    # form submission
    message_form = ChatMessageForm(request.POST)
    if not message_form.is_valid():
        messages.warning(request, 'Form NOT valid!')
        return redirect(request.META.get('HTTP_REFERER'))

    _new = ChatMessage.objects.create(
        chatroom_id=request.POST['chatroom'],
        message=message_form.cleaned_data['message'],
        sender_id=request.user.id,
        date_sent=DT.datetime.now()
    )
    _new.save()

    # post data contains reference chat id?
    if reference_id := request.POST['reference']:
        ref_msg = ChatMessage.objects.get(id=reference_id)
        _new.reply_to = ref_msg.id
        _new.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def calendar(request, yy=None, mm=None, dd=None):
    dt = prev_year = prev_month = next_year = next_month = None

    if yy and mm and dd:        
        dt = DT.datetime(yy, mm, dd)
    elif yy and mm:
        dt = DT.datetime(yy, mm, 1)
    else:
        dt = DT.datetime.now()
        yy = dt.year
        mm = dt.month

    if 1 < mm < 12:
        prev_month = mm - 1
        next_month = mm + 1
        prev_year = next_year = yy

    elif mm == 1:
        prev_month = 12
        prev_year = yy - 1
        next_month = mm + 1
        next_year = yy

    elif mm == 12:
        prev_month = mm - 1
        prev_year = yy
        next_month = 1
        next_year = yy + 1

    # calendar
    first_day = dt.date().replace(day=1)    # first day of month
    week_pos = first_day.weekday()  # day of week
    num_skip = range(week_pos)  # number of cells to skip
    num_days = CAL.monthrange(dt.year, dt.month)[1] # number of days in month
    month_days = range(1, (num_days+1))

    # queries
    user = request.user
    due_tasks = []
    due_bills = []
 
    # tasks & bills to be paid
    if user.is_organizer:
        events = user.organizer.event_set.all()
        for event in events:
            tasks = event.task_set.all()
            expenses = event.expense_set.all()
            for task in tasks:
                if not task.completed and task.due_date == dt.date():
                    due_tasks.append(task)
            for xp in expenses:
                if not xp.balance_cleared and xp.date_budgeted.date() <= dt.date():
                    due_bills.append(xp)

    context = {
        'active_dt': dt,
        'prev_month': prev_month,
        'next_month': next_month,
        'prev_year': prev_year,
        'next_year': next_year,
        'num_skip': num_skip,
        'month_days': month_days,
    }
    if user.is_organizer:
        context['due_tasks'] = due_tasks
        context['due_bills'] = due_bills
    return render(request, 'main/calendar.html', context)


def get_csrf(request):
    return JsonResponse({'csrf_token': get_token(request)}, status=200)
