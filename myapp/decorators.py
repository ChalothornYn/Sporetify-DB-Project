from django.http import HttpResponse
from django.shortcuts import redirect

# ---------------------------------- Customer Authotization ----------------------------------
def unauthenticated_customer(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/userprofile/')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def customer_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        
        if group == 'customer':
            return view_func(request, *args, **kwargs)

        if group == 'entertainment':
            return redirect('enDashboard')    
        
        if group == 'admin':
            return redirect('adminProfile') 
    return wrapper_func





# ---------------------------------- Entertainment Authotization ----------------------------------
def unauthenticated_entertainment(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('enDashboard')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def entertainment_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        
        if group == 'customer':
            return redirect('/userprofile/')

        if group == 'entertainment':
            return view_func(request, *args, **kwargs)     
        
        if group == 'admin':
            return redirect('adminProfile') 
    return wrapper_func




# ---------------------------------- Admin Authorization ----------------------------------
def unauthenticated_admin(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('adminProfile')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        
        if group == 'customer':
            return redirect('/userprofile/')

        if group == 'entertainment':
            return redirect('enDashboard')    
        
        if group == 'admin':
            return view_func(request, *args, **kwargs)    
    return wrapper_func