from django.http import HttpResponse


def organizer_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_organizer:
            return view_func(request, *args, **kwargs)
        else:
            error_msg = 'Unauthorised action. You must be an event organizer to access this page!'
            return HttpResponse(error_msg)
    return wrapper_func


def planner_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_planner:
            return view_func(request, *args, **kwargs)
        else:
            error_msg = 'Unauthorised action. You must be an event planner to access this page!'
            return HttpResponse(error_msg)
    return wrapper_func


def vendor_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_vendor:
            return view_func(request, *args, **kwargs)
        else:
            error_msg = 'Unauthorised action. You must be a vendor to access this page!'
            return HttpResponse(error_msg)
    return wrapper_func


def planner_or_organizer_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_planner or request.user.is_organizer):
            return view_func(request, *args, **kwargs)
        else:
            error_msg = 'Unauthorised action. You must be an event planner or organizer to access this page!'
            return HttpResponse(error_msg)
    return wrapper_func



def planner_or_vendor_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_vendor or request.user.is_planner):
            return view_func(request, *args, **kwargs)
        else:
            error_msg = 'Error! You must be a vendor or event planner to access this page!'
            return HttpResponse(error_msg)
    return wrapper_func