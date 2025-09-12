from django.urls import path,include
from Users.views import sign_up,sign_in,activate_user,admin_dashboard,assigned_role,create_group,group_list,sign_out
urlpatterns = [
    path('sign-up/',sign_up,name='sign-up'),
    path('sign-in/',sign_in,name='sign-in'),
    path('sign-out/',sign_out,name='sign-out'),
    path('activate/<int:user_id>/<str:token>/',activate_user),
    path('admin/dashboard/',admin_dashboard,name='admin-dashboard'),
    path('admin/<int:user_id>/assign-role',assigned_role,name='assign-role'),
    path('admin/create-group/',create_group,name='create-group'),
    path('admin/group-list',group_list,name='group-list')
]
