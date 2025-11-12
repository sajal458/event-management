from django.urls import path
from .views import view_task,create_task,show_dashboard,home,update_event,delete_event,event_detail,add_category,rsvp,dashboard,Create_Event,Event_detail,Update_Event
urlpatterns = [
    path('show/',view_task),
    # path("create-task/",create_task,name="create"),
    path("create-task/",Create_Event.as_view(),name="create"),
    path("dashboard/",show_dashboard,name="dashboard"),
    path("home/",home,name='home'),
    # path("update-event/<int:id>/",update_event,name="update_event"),
    path("update-event/<int:id>/",Update_Event.as_view(),name="update_event"),
    path("delete-event/<int:id>/",delete_event,name="delete_event"),
    # path("details/<int:id>/",event_detail,name="details"),
    path("details/<int:id>/",Event_detail.as_view(),name="details"),
    #path("add-participant/", add_participant, name="add_participant"),
    path("add-category/", add_category, name="add_category"),
    path('rsvp/<int:event_id>/',rsvp,name='rsvp'),
    path('select-dashboard',dashboard,name='select-dashboard')
    
]
