from django.urls import path,include
from Users.views import sign_up,sign_in,activate_user,admin_dashboard,assigned_role,create_group,group_list,sign_out,Sign_in,Sign_out,Profileview,ChangePassword,PasswordChangeDoneView,CustomPasswordReset,PasswordConfirmResetview,EditProfileView,delete_user
from Event.views import EventUpdateView,EventDeleteView,event_list
urlpatterns = [
    path('sign-up/',sign_up,name='sign-up'),
    path('sign-in/',sign_in,name='sign-in'),
    # path('sign-in/',Sign_in.as_view(),name='sign-in'),
    # path('sign-out/',sign_out,name='sign-out'),
    path('sign-out/',Sign_out.as_view(),name='sign-out'),    
    path('activate/<int:user_id>/<str:token>/',activate_user),
    path('admin/dashboard/',admin_dashboard,name='admin-dashboard'),
    path('delete-user/<int:id>/', delete_user, name='delete-user'),
    path('admin/<int:user_id>/assign-role',assigned_role,name='assign-role'),
    path('admin/create-group/',create_group,name='create-group'),
    path('admin/group-list',group_list,name='group-list'),
    path('profile/',Profileview.as_view(),name='profile'),
    path('password-change/',ChangePassword.as_view(),name='change-password'),
    path('password-change/done/',PasswordChangeDoneView.as_view(template_name="password_change_done.html"),name='password-change-done'),
    path('password-reset/',CustomPasswordReset.as_view(),name='password-reset'),
    path('password-reset/confirm/<uidb64>/<token>/',PasswordConfirmResetview.as_view(),name='password_reset_confirm'),
    path('edit-profile/',EditProfileView.as_view(),name='edit-profile'),
    path('event/edit/<int:pk>/', EventUpdateView.as_view(), name='event-edit'),
    path('event/delete/<int:pk>/', EventDeleteView.as_view(), name='event-delete'),
    path('events/', event_list, name='event-list'),
]
