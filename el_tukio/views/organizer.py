from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import login
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, F
from django.db import transaction

import json
import datetime as DT

from el_tukio.forms import *
from el_tukio.models import *
from el_tukio.utils.decorators import *
from el_tukio.utils.main import *
from el_tukio.utils.messages import *


class Register(CreateView):
    form_class = OrganizerRegForm
    template_name = 'main/register/organizer.html'
    extra_context = {'title': 'Event organizer Registration'}

    def form_valid(self, form):
        print_form_values(form)
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Login successful!')
        return redirect('organizer-dashboard')


@organizer_required
def dashboard(request):
    return render(request, 'organizer/dashboard.html')


@organizer_required
def events(request):
    context = {'events': Event.objects.filter(organizer_id=request.user.organizer.user_id)}
    return render(request, 'organizer/events.html', context)


@method_decorator(organizer_required, name='dispatch')
class Events(CreateView):
    form_class = EventForm
    template_name = 'organizer/events.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = Event.objects.filter(organizer_id=self.request.user.organizer.user_id)
        return context
    
    @transaction.atomic
    def form_valid(self, form):
        event = Event.objects.create(
            organizer=self.request.user.organizer,
            event_name=form.cleaned_data['event_name'],
            event_date=form.cleaned_data['event_date'],
            event_budget=form.cleaned_data['event_budget'],
            event_location=form.cleaned_data['event_location'],
            guest_size=form.cleaned_data['guest_size']
        )
        # create event chatroom
        chatroom = ChatRoom.objects.create(
            name=f'{event.event_name} chatroom',
            type=ChatRoom.Type.GROUP
        )
        # add organizer to chatroom
        chatroom.members.add(self.request.user)
        event.chatroom = chatroom
        event.save()
        # done
        messages.success(self.request, 'New event created!')
        return redirect(self.request.META.get('HTTP_REFERER', '/'))


@method_decorator(organizer_required, name='dispatch')
class EventUpdate(UpdateView):
    form_class = EventForm
    template_name = 'organizer/event-update.html'

    def get_object(self):
        return get_object_or_404(Organizer, pk=self.request.user.pk)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Event details updated!')
        return redirect('organizer-events')


@login_required
def event_details(request, event_id):
    event = Event.objects.get(pk=event_id)
    context = {
        'event': event,
        'active': 'details'
    }
    return render(request, 'organizer/event-details.html', context)


@organizer_required
def event_update(request, event_id):
    event = Event.objects.get(pk=event_id)
    if not request.method == 'POST':
        form = EventForm(instance=event)
        return render(request, 'organizer/event-update.html', {'form': form})

    form = EventForm(request.POST, instance=event)
    if not form.is_valid():
        messages.warning(request, form.errors)
        return redirect(request.META.get('HTTP_REFERER'))

    form.save()
    messages.success(request, 'Event details updated!')
    return redirect('organizer-events')


@planner_or_organizer_required
def event_team(request, event_id):
    event = Event.objects.get(id=event_id)
    event_team = event.event_team.all()
    contracts = Contract.objects.filter(event_id=event_id).exclude(status=Contract.Status.ACCEPTED)
    context = {
        'event': event,
        'team': event_team,
        'contracts': contracts,
        'active': 'team'
    }
    return render(request, 'organizer/event-team.html', context)


@planner_or_organizer_required
def tasks(request, event_id, group_id=None):
    TASK_FORM_PREFIX = 'task_form'
    TASK_U_FORM_PREFIX = 'task_u_form'
    TASK_GRP_FORM_PREFIX = 'group_form'

    event = Event.objects.get(id=event_id)
    task_form = TaskForm(event_date=event.event_date, prefix=TASK_FORM_PREFIX)
    task_ct_update_form = TaskContentUpdateForm(prefix=TASK_U_FORM_PREFIX)
    task_dd_update_form = TaskDueDateUpdateForm(event_date=event.event_date, prefix=TASK_U_FORM_PREFIX)
    task_group_form = TaskGroupForm(prefix=TASK_GRP_FORM_PREFIX)
    tasks = Task.objects.filter(event_id=event_id).order_by('completed').exclude(deleted=True)
    task_groups = TaskGroup.objects.filter(event_id=event_id)
    all_count = Task.objects.filter(event_id=event_id).count()
    active_group = 0
    page_title = 'Event Tasks'

    team_ids = Contract.objects.filter(event_id=event_id, status=Contract.Status.ACCEPTED).values_list('contractee_id')
    event_team = User.objects.filter(id__in=team_ids)

    if group_id:
        task_group = TaskGroup.objects.get(id=group_id)
        tasks = Task.objects.filter(event_id=event_id, task_group_id=task_group.id).order_by('completed')
        active_group = task_group.id
        page_title = task_group.name

    if not request.method == 'POST':      
        context = {
            'event': event,
            'event_team': event_team,
            'task_form': task_form,
            'task_ct_update_form': task_ct_update_form,
            'task_dd_update_form': task_dd_update_form,
            'task_group_form': task_group_form,
            'tasks': tasks,
            'task_groups': task_groups,
            'all_count': all_count,
            'active': 'plan',
            'active_group': active_group,
            'page_title': page_title
        }
        return render(request, 'organizer/tasks.html', context)

    # post using fetch api?
    using_fetch_api = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if not using_fetch_api:
        form_type = request.POST['form_type']

        if form_type == TASK_FORM_PREFIX:
            form = TaskForm(request.POST, event_date=event.event_date, prefix=TASK_FORM_PREFIX)
            if not form.is_valid():
                messages.success(request, 'Form NOT valid!')
                return redirect(request.META.get('HTTP_REFERER', '/'))

            task = Task.objects.create(
                event_id=event.id,
                task=form.cleaned_data['task'],
                due_date=form.cleaned_data['due_date'],
                created_by_id=request.user.id
            )

            if group_id:
                task.task_group = TaskGroup.objects.get(id=group_id)
                task.save()
                
            messages.success(request, 'New task added!')
            return redirect(request.META.get('HTTP_REFERER', '/'))

        elif form_type == TASK_GRP_FORM_PREFIX:
            form = TaskGroupForm(request.POST, prefix=TASK_GRP_FORM_PREFIX)
            if not form.is_valid():
                messages.success(request, 'Form NOT valid!')
                return redirect(request.META.get('HTTP_REFERER', '/'))
            
            task_group = TaskGroup.objects.create(
                event_id=event.id,
                name=form.cleaned_data['name']
            )
            task_group.save()
            messages.success(request, 'Task group created!')
            return redirect(request.META.get('HTTP_REFERER', '/'))

    # using js fetch api
    else:
        form_data = json.loads(request.body)
        form_type = form_data['form_type']
        form = None

        if form_type == TASK_U_FORM_PREFIX:
            task_id = int(form_data['task_id'])
            task = Task.objects.get(id=task_id)

            if f'{TASK_U_FORM_PREFIX}-task' in form_data:
                form = TaskContentUpdateForm(form_data, prefix=TASK_U_FORM_PREFIX)
                if form.is_valid():
                    task.task = form.cleaned_data['task']
                    
            elif f'{TASK_U_FORM_PREFIX}-due_date' in form_data:
                form = TaskDueDateUpdateForm(form_data, event_date=event.event_date, prefix=TASK_U_FORM_PREFIX)
                if form.is_valid():
                    task.due_date = form.cleaned_data['due_date']

            if not form.is_valid():
                return JsonResponse(msg.error('Form NOT valid!'))

            task.save()
            return JsonResponse(msg.info('Task updated!'))

        # task group name update
        elif form_type == TASK_GRP_FORM_PREFIX:
            if task_group_id := form_data['task_group_id']:
                task_group = TaskGroup.objects.get(id=task_group_id)
                form = TaskGroupForm(form_data, instance=task_group, prefix=TASK_GRP_FORM_PREFIX)
                if form.is_valid():
                    form.save()
                    return JsonResponse(msg.success('Updated!'))
                else:
                    return JsonResponse(msg.error('Error!'))


# @organizer_required
def task_details(request, task_id):
    task = Task.objects.filter(id=task_id)
    taskValues = task.values(
        'id',
        'task',
        'date_created',
        'due_date',
        'completed',
        'date_completed',
    ).annotate(
        created_by_fname=F('created_by__first_name'),
        created_by_lname=F('created_by__last_name'),
        assigned_to_id=F('assigned_to__id'),
        assigned_to_fname=F('assigned_to__first_name'),
        assigned_to_lname=F('assigned_to__last_name'),
        assigned_to_phone=F('assigned_to__phone_number'),
        completed_by_fname=F('completed_by__first_name'),
        completed_by_lname=F('completed_by__last_name')
    )[0]
    task = task[0]
    if task.assigned_to:
        taskValues['assigned_to_business'] = task.assigned_to.user_role
    return JsonResponse(taskValues)


# @organizer_required
def complete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if task.completed:
        task.completed = False
        task.date_completed = None
        task.completed_by = None
    else:
        task.completed = True
        task.date_completed = DT.datetime.now()
        task.completed_by = request.user
    task.save()
    return JsonResponse(msg.success('Task status changed!'))


# @organizer_required
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.deleted = True
    task.date_deleted = DT.datetime.now()
    task.save()
    return JsonResponse(msg.success('Task deleted!'))


@planner_or_organizer_required
def assign_to(request, task_id, member_id):
    task = Task.objects.get(id=task_id)
    task.assigned_to = User.objects.get(id=member_id)
    task.save()
    return JsonResponse(msg.success('Task assigned!'))


@planner_or_organizer_required
def assign_to_remove(request, task_id):
    task = Task.objects.get(id=task_id)
    task.assigned_to = None
    task.save()
    return JsonResponse(msg.success('Task updated!'))


# @organizer_required
def delete_task_group(request, event_id, group_id, tasks_included='No'):
    group = TaskGroup.objects.get(id=group_id, event_id=event_id)

    if tasks_included and tasks_included == 'Yes':
        tasks = Task.objects.filter(task_group_id=group.id)
        for task in tasks:
            task.delete()

    group.delete()
    return redirect('organizer-event-tasks', event_id=event_id)


# budget tracker

@planner_or_organizer_required
def budget_tracker(request, event_id):
    EXPENSE_FORM_PREFIX = 'exp_form'
    EXPENSE_U_FORM_PREFIX = 'exp_u_form'
    EXPENSE_CAT_FORM_PREFIX = 'exp_cat_form'

    exp_categories = ExpenseCategory.objects.filter(Q(event__isnull=True) | Q(event_id=event_id)).values_list('id', 'name').order_by('-event')

    event = Event.objects.get(id=event_id)
    expenses = Expense.objects.filter(event_id=event_id)
    expense_form = ExpenseForm(prefix=EXPENSE_FORM_PREFIX, exp_categories=exp_categories)
    expense_u_form = ExpenseUpdateForm(prefix=EXPENSE_U_FORM_PREFIX, exp_categories=exp_categories)
    expense_cat_form = ExpenseCategoryForm(prefix=EXPENSE_CAT_FORM_PREFIX)

    if not request.method == 'POST':
        context = {
            'event': event,
            'expenses': expenses,
            'expense_form': expense_form,
            'expense_u_form': expense_u_form,
            'expense_cat_form': expense_cat_form,
            'active': 'expenses'
        }
        return render(request, 'organizer/expenses.html', context)

    form_data = request.POST    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form_data = json.loads(request.body)
        
    form_type = form_data['form_type']

    if form_type == EXPENSE_FORM_PREFIX:
        form = ExpenseForm(form_data, prefix=EXPENSE_FORM_PREFIX)
        if not form.is_valid():
            messages.add_message(request, messages.WARNING, 'Form NOT valid!')
            return redirect(request.META.get('HTTP_REFERER', '/'))
        
        expense = Expense.objects.create(
            event_id=event.id,
            description=form.cleaned_data['description'],
            expense_category=form.cleaned_data['expense_category'],
            total_cost=form.cleaned_data['total_cost'],
            budgeted_by = request.user
        )
        expense.save()
        messages.success(request, 'Expense recorded!')
        return redirect(request.META.get('HTTP_REFERER', '/'))

    if form_type == EXPENSE_U_FORM_PREFIX:
        exp_id = form_data['expense_id']
        exp = Expense.objects.get(id=exp_id)
        form = ExpenseUpdateForm(form_data, instance=exp, prefix=EXPENSE_U_FORM_PREFIX)
        if  not form.is_valid():
            error = form.errors.as_data()['__all__'][0]
            return JsonResponse(msg.error(f'Ooops! {error}'))

        form.save()
        return JsonResponse(msg.success('Updated!'))


# @organizer_required
def expense_details(request, exp_id):
    exp = Expense.objects.filter(id=exp_id).values(
        'id',
        'description',
        'total_cost',
        'total_paid',
        'date_budgeted'
    ).annotate(
        budgeted_by_fname=F('budgeted_by__first_name'),
        budgeted_by_lname=F('budgeted_by__last_name')
    )[0]
    return JsonResponse(exp, safe=False)


# @organizer_required
def delete_expense(request, id):
    Expense.objects.get(id=id).delete()
    return JsonResponse(msg.success('Deleted!'))
