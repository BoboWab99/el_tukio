from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib import messages
from django.utils.decorators import method_decorator

from el_tukio.forms import PlannerRegForm
from el_tukio.models import User
from el_tukio.utils.decorators import planner_required


# @method_decorator(planner_required, name='dispatch')
class Register(CreateView):
    # model = User
    form_class = PlannerRegForm
    template_name = 'main/register/register.html'
    extra_context = {'title': 'Event planner Registration'}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Login successful!')
        return redirect('planner-dashboard')


@planner_required
def dashboard(request):
    return render(request, 'planner/dashboard.html')
