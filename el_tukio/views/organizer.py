from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import login
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.db.models import F
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

import json
import datetime as DT

from el_tukio.forms import OrganizerRegForm, EventForm, TaskForm, TaskGroupForm, TaskContentUpdateForm, TaskDueDateUpdateForm
from el_tukio.models import Organizer, Event, Contract, User, Task, TaskGroup
from el_tukio.utils.decorators import organizer_required
from el_tukio.utils.main import print_form_values
from el_tukio.utils.messages import msg


class Register(CreateView):
    form_class = OrganizerRegForm
    template_name = 'main/register/register.html'
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
    
    def form_valid(self, form):
        event = Event.objects.create(
            organizer=self.request.user.organizer,
            event_name=form.cleaned_data['event_name'],
            event_date=form.cleaned_data['event_date'],
            event_budget=form.cleaned_data['event_budget'],
            event_location=form.cleaned_data['event_location'],
            guest_size=form.cleaned_data['guest_size']
        )
        event.save()
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


@organizer_required
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


@organizer_required
def event_team(request, event_id):
    event = Event.objects.get(id=event_id)
    team_ids = Contract.objects.filter(event_id=event_id, status=Contract.Status.ACCEPTED).values_list('contractee_id')
    team = User.objects.filter(id__in=team_ids)
    context = {
        'team': team, 
        'event': event,
        'active': 'team'
    }
    return render(request, 'organizer/event-team.html', context)


@organizer_required
def tasks(request, event_id, group_id=None):
    TASK_FORM_PREFIX = 'task_form'
    TASK_UPDATE_FORM_PREFIX = 'task_u_form'
    TASK_GROUP_FORM_PREFIX = 'group_form'

    event = Event.objects.get(id=event_id)
    task_form = TaskForm(event_date=event.event_date, prefix=TASK_FORM_PREFIX)
    task_ct_update_form = TaskContentUpdateForm(prefix=TASK_UPDATE_FORM_PREFIX)
    task_dd_update_form = TaskDueDateUpdateForm(event_date=event.event_date, prefix=TASK_UPDATE_FORM_PREFIX)
    task_group_form = TaskGroupForm(prefix=TASK_GROUP_FORM_PREFIX)
    tasks = Task.objects.filter(event_id=event_id)
    task_groups = TaskGroup.objects.filter(event_id=event_id)
    all_count = Task.objects.filter(event_id=event_id).count()
    active_group = 'all'
    page_title = 'Event Tasks'

    if group_id:
        task_group = TaskGroup.objects.get(id=group_id)
        tasks = Task.objects.filter(event_id=event_id, task_group_id=task_group.id)
        active_group = group_id
        page_title = task_group.name

    if not request.method == 'POST':      
        context = {
            'event': event,
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

    # js fetch api
    if (request.headers.get('X-Requested-With') == 'XMLHttpRequest'):
        data = json.loads(request.body)
        form_type = data['form_type']
        form = None

        if form_type == TASK_FORM_PREFIX:
            form = TaskForm(data, event_date=event.event_date, prefix=TASK_FORM_PREFIX)
            if not form.is_valid():
                return JsonResponse(msg.error('Form NOT valid!'))

            task = Task.objects.create(
                event_id=event.id,
                task=form.cleaned_data['task'],
                due_date=form.cleaned_data['due_date'],
                created_by_id=request.user.id
            )

            if group_id:
                task.task_group = TaskGroup.objects.get(id=group_id)

            task.save()
            new_task = Task.objects.filter(id=task.id).values(
                'id',
                'task',
                'due_date',
                'completed'
            ).annotate(
                task_group=F('task_group__name')
            )[0]
            _msg = msg.success('New task added!')
            return JsonResponse({'task': new_task, 'msg': _msg})    

        elif form_type == TASK_GROUP_FORM_PREFIX:
            form = TaskGroupForm(data, prefix=TASK_GROUP_FORM_PREFIX)
            if not form.is_valid():
                return JsonResponse(msg.error('Form NOT valid!'))
            
            task_group = TaskGroup.objects.create(
                event_id=event.id,
                name=form.cleaned_data['name']
            )
            task_group.save()
            return JsonResponse(msg.success('Task group created!'))

        elif form_type == TASK_UPDATE_FORM_PREFIX:
            task_id = int(data['task_id'])
            task = Task.objects.get(id=task_id)

            if f'{TASK_UPDATE_FORM_PREFIX}-task' in data:
                form = TaskContentUpdateForm(data, prefix=TASK_UPDATE_FORM_PREFIX)
                if form.is_valid():
                    task.task = form.cleaned_data['task']
                    
            elif f'{TASK_UPDATE_FORM_PREFIX}-due_date' in data:
                form = TaskDueDateUpdateForm(data, event_date=event.event_date, prefix=TASK_UPDATE_FORM_PREFIX)
                if form.is_valid():
                    task.due_date = form.cleaned_data['due_date']

            if not form.is_valid():
                return JsonResponse(msg.error('Form NOT valid!'))

            task.save()
            return JsonResponse(msg.info('Task updated!'))

    return JsonResponse(msg.error('Errrooorrrrr!'))


@organizer_required
def task_details(request, task_id):
    task = Task.objects.filter(id=task_id).values(
        'id',
        'task',
        'date_created',
        'due_date',
        'completed',
        'date_completed',
    ).annotate(
        created_by_fname=F('created_by__first_name'),
        created_by_lname=F('created_by__last_name'),
        assigned_to_fname=F('assigned_to__first_name'),
        assigned_to_lname=F('assigned_to__last_name'),
        completed_by_fname=F('completed_by__first_name'),
        completed_by_lname=F('completed_by__last_name')
    )[0]
    return JsonResponse(task)


@organizer_required
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


@organizer_required
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return JsonResponse(msg.success('Task deleted!'));
