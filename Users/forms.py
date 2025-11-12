
from django.contrib.auth.models import Permission,Group
from django import forms
import re
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from Users.models import CustomUser
from django.contrib.auth import get_user_model
User=get_user_model()
class Style_Mixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style_widget()
    default_classes = "border-2 border-gray-300 w-full rounded-lg shadow-sm p-3 focus:outline-none focus:border-rose-500 focus:ring-rose-500"

    def apply_style_widget(self):
        for field_name, field in self.fields.items():
            
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class':self.default_classes,
                    'placeholder':f"enter {field.label.lower()}"
                })
            elif isinstance(field.widget,forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class': "border-2 border-gray-300  rounded-lg shadow-sm focus:border-rose-300", 'row':5,

                })
            elif isinstance(field.widget,forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    
                })
            else:
                print("Inside else")
                field.widget.attrs.update({
                    'class': self.default_classes
                })




class CustomRegistration(Style_Mixin,forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    Confirm_password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username' ,'first_name','last_name','password','Confirm_password','email']
        help_texts = {   
            'username': None,
        }

    def clean_email(self):
            email = self.cleaned_data.get('email') 
            email_exist=User.objects.filter(email=email).exists()
            if email_exist:
                raise forms.ValidationError("emmail already exist")
            return email

    def clean_password(self):
            password = self.cleaned_data.get('password')

            if len(password) < 8:
                raise forms.ValidationError('Password must be at least 8 characters')

            
            if not re.search(r'[A-Z]', password):
                raise forms.ValidationError("Password must contain at least one uppercase letter")
            if not re.search(r'[a-z]', password):
                raise forms.ValidationError("Password must contain at least one lowercase letter")
            if not re.search(r'\d', password):
                raise forms.ValidationError("Password must contain at least one digit")
            if not re.search(r'[@#$%^&*()_+=!]', password):
                raise forms.ValidationError("Password must contain at least one special character")

            return password
        
    def clean(self):
            cleaned_data=super().clean()
            password=cleaned_data.get('password')
            Confirm_password=cleaned_data.get('Confirm_password')
            if password and Confirm_password and password != Confirm_password:
                raise forms.ValidationError("password did not match")
            return cleaned_data
  


class LoginForm(Style_Mixin,AuthenticationForm):
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AssignRoleForm(Style_Mixin,forms.Form):
    role=forms.ModelChoiceField(
          queryset=Group.objects.all(),
          empty_label="Select role"
     )
     

     
class CreateGroup(Style_Mixin,forms.ModelForm):
     permissions=forms.ModelMultipleChoiceField(
          queryset=Permission.objects.all(),
          widget=forms.CheckboxSelectMultiple,
          required=False,
          label='Assigned Permission'


     )
     class Meta:
          model=Group
          fields=['name','permissions']

class CustomPasswordChnage(Style_Mixin,PasswordChangeForm):
     pass
class CustomResetPasswordForm(Style_Mixin,PasswordResetForm):
     pass
class CustomSetPassword(Style_Mixin,SetPasswordForm):
     pass

class EditProfileform(Style_Mixin,forms.ModelForm):
    class Meta:
         model=CustomUser
         fields=['email', 'first_name','last_name','phone_number','profile_image']     
         

# class EditProfileform(Style_Mixin, forms.ModelForm):
#     phone_number = forms.CharField(required=False, label='Phone number')
#     profile_image = forms.ImageField(required=False, label='Image')

#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name']

#     def __init__(self, *args, **kwargs):
#         self.userprofile = kwargs.pop('userprofile', None)
#         super().__init__(*args, **kwargs)

#         if self.userprofile:
#             self.fields['profile_image'].initial = self.userprofile.profile_image
#             self.fields['phone_number'].initial = self.userprofile.phone_number

#     def save(self, commit=True):
#         user = super().save(commit)
#         if self.userprofile:
#             self.userprofile.phone_number = self.cleaned_data.get('phone_number')
#             self.userprofile.profile_image = self.cleaned_data.get('profile_image')
#             if commit:
#                 self.userprofile.save()
#         return user
# class EditProfileform(Style_Mixin, forms.ModelForm):
#     phone_number = forms.CharField(required=False, label='Phone number')
#     profile_image = forms.ImageField(required=False, label='Profile image')

#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name']

#     def __init__(self, *args, **kwargs):
#         self.userprofile = kwargs.pop('userprofile', None)
#         super().__init__(*args, **kwargs)
#         if self.userprofile:
#             self.fields['phone_number'].initial = self.userprofile.phone_number
#             self.fields['profile_image'].initial = self.userprofile.profile_image

#     def save(self, commit=True):
#         user = super().save(commit)
#         if self.userprofile:
#             self.userprofile.phone_number = self.cleaned_data.get('phone_number')
#             if self.cleaned_data.get('profile_image'):
#                 self.userprofile.profile_image = self.cleaned_data.get('profile_image')
#             if commit:
#                 self.userprofile.save()
#         return user