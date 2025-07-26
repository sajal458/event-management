from django.urls import path
from .views import view_task,create_task,show_dashboard,home,update_event,delete_event,event_detail
urlpatterns = [
    path('show/',view_task),
    path("create-task/",create_task,name="create"),
    path("dashboard/",show_dashboard,name="dashboard"),
    path("home/",home,name='home'),
    path("update-event/<int:id>/",update_event,name="update_event"),
    path("delete-event/<int:id>/",delete_event,name="delete_event"),
    path("details/<int:id>/",event_detail,name="details")

    
]
