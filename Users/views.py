from django.shortcuts import render,redirect,HttpResponse
from Users.forms import CustomRegistration,LoginForm,AssignRoleForm,CreateGroup,CustomPasswordChnage,CustomResetPasswordForm,CustomSetPassword,EditProfileform
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
# Create your views here.
from django.contrib.auth.views import LoginView ,LogoutView,PasswordChangeView,PasswordChangeDoneView,PasswordResetView,PasswordResetConfirmView
from django.views import View
from django.views.generic import TemplateView,UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
User=get_user_model()








def is_admin(user):
    return user.groups.filter(name='Admin').exists()



# class EditProfileView(UpdateView):
#     model=User
#     form_class=EditProfileform
#     template_name='update.html'
#     def get_object(self):
#         return self.request.user
#     def get_form_kwargs(self):
#         kwargs= super().get_form_kwargs()
        
#         kwargs['userprofile'] = UserProfile.objects.get(user=self.request.user)
#         return kwargs
#     def get_context_data(self, **kwargs):
#         context= super().get_context_data(**kwargs)
#         userprofile = UserProfile.objects.get(user=self.request.user)
#         context['form']=self.form_class(instance=self.object,userprofile=userprofile)
#         return context
#     def form_valid(self,form):
#         form.save(commit=True)
#         return redirect('profile')



# class EditProfileView(UpdateView):
#     model = User
#     form_class = EditProfileform
#     template_name = 'update.html'

#     def get_object(self):
#         return self.request.user

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['userprofile'] = UserProfile.objects.get(user=self.request.user)
#         return kwargs

#     def form_valid(self, form):
#         form.save(commit=True)
#         return redirect('profile')


class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileform
    template_name = 'update.html'
    context_object_name='form'

    def get_object(self):
        return self.request.user



    def form_valid(self, form):
        form.save(commit=True)
        return redirect('profile')



class CustomPasswordReset(PasswordResetView):
    form_class=CustomResetPasswordForm
    template_name='reset_password.html'
    success_url=reverse_lazy('sign-in')
    def form_valid(self, form):
        messages.success(self.request,'A reset email sent. check yoyr email')
        return super().form_valid(form)
    
class PasswordConfirmResetview(PasswordResetConfirmView):
    form_class=CustomSetPassword
    template_name='reset_password.html'
    success_url=reverse_lazy('sign-in')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["protocol"] = 'https' if self.request.is_secure() else 'http'
        self.request.get_host()
        return context
    
    def form_valid(self, form):
        messages.success(self.request,'password reset successfully')
        return super().form_valid(form)


class Profileview(TemplateView):
    template_name='profile.html'
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        user=self.request.user
        context['username']=user.username
        context['email']=user.email
        context['name']=f"{user.first_name} {user.last_name}"
        context['profile_image']=user.profile_image
        context['phone_number']=user.phone_number
        return context


class ChangePassword(PasswordChangeView):

    template_name='changepassword.html'
    form_class=CustomPasswordChnage


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
                print("does not exist")
            return redirect('select-dashboard')
        else:
            print('form is not valid')
        

    return render(request,"login.html",{'form':form})

class Sign_in(LoginView):
    form_class=LoginForm
    template_name="login.html"
    def get_success_url(self):
        next_url=self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()

# @login_required
# def sign_out(request):
#     if request.method=='POST':
#         logout(request)
#         return redirect('sign-in')
@login_required
def sign_out(request):
    logout(request)
    return redirect('sign-in')
class Sign_out(View):
    def get(self, request):
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
