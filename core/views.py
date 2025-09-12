from django.shortcuts import render,redirect
from Event.views import dashboard,is_admin,is_organizer,is_participant

# Create your views here.
def homes(request):
    

    if is_participant(request.user):
        return redirect('home')
    elif is_organizer(request.user):
        return redirect('dashboard')
    elif is_admin(request.user):
        return redirect('admin-dashboard')
    else:
        return render(request,'homes.html')
def no_permission(request):
    return render(request,'no_permission.html')