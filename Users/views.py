from django.shortcuts import render,redirect,HttpResponse
from Users.forms import CustomRegistration,LoginForm,AssignRoleForm,CreateGroup
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User,Group
from django.contrib.auth.tokens import default_token_generator
# Create your views here.


def is_admin(user):
    return user.groups.filter(name='Admin').exists()



def sign_up(request):
    form = CustomRegistration()
    if request.method == 'POST':
        form = CustomRegistration(request.POST)
        if form.is_valid(): 
            user = form.save(commit=False)            
            user.set_password(form.cleaned_data.get('password'))
            user.is_active = False
            
            user.save()
            participant_group, created = Group.objects.get_or_create(name="Participant")
            user.groups.add(participant_group)
            messages.success(
                request, 'A Confirmation mail sent. Please check your email.'
            )
            return redirect('sign-in')
        else:
            print("form is not valid", form.errors)  

    return render(request, 'registration.html', {'form': form})




def sign_in(request):
    form=LoginForm()
    if request.method=='POST':
        form=LoginForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            if user.DoesNotExist:
                print("ksfnoivof")
            return redirect('select-dashboard')
        else:
            print('form is not valid')
        

    return render(request,"login.html",{'form':form})

# @login_required
# def sign_out(request):
#     if request.method=='POST':
#         logout(request)
#         return redirect('sign-in')
@login_required
def sign_out(request):
    logout(request)
    return redirect('sign-in')
def activate_user(request,user_id,token):
    user=User.objects.get(id=user_id)
    try:
        if default_token_generator.check_token(user,token):
            user.is_active=True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse("invalid doken")
    except User.DoesNotExist:
        return HttpResponse("user not found\n")
    
@user_passes_test(is_admin,login_url='no-permission')
def admin_dashboard(request):
    user=User.objects.all()

    return render(request,'admin_dashboard.html',{'users':user})

@user_passes_test(is_admin,login_url='no-permission')
def assigned_role(request,user_id):
    user=User.objects.get(id=user_id)
    form=AssignRoleForm()
    if request.method=="POST":
        form=AssignRoleForm(request.POST)
        if form.is_valid():
            role=form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request,f"{user.username} has assigned to {role.name}")
            return redirect('admin-dashboard')
    return render(request,'assigned_role.html',{'form':form})


@user_passes_test(is_admin,login_url='no-permission')
def create_group(request):
    form=CreateGroup()
    if request.method=='POST':
        form=CreateGroup(request.POST)

        if form.is_valid():
            group=form.save()
          
            return redirect("create-group")
    return render(request,"groups.html",{"form" :form})

@user_passes_test(is_admin,login_url='no-permission')
def group_list(request):
    groups=Group.objects.all()
    return render(request,'group_list.html',{"groups":groups})
