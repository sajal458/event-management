from django.shortcuts import render,redirect
from django.http import HttpResponse
from Event.forms import TaskModel, CategoryForm
from Event.models import Category,Event
from django.db.models import Count,Q
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User
from Event.models import Category, Event
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from django.views import View
from django.views.generic import ListView,DetailView,UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin


# Create your views here.
def view_task(request):
    return HttpResponse("hello")



def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

def is_participant(user):
    return user.groups.filter(name='Participant').exists()

def is_admin(user):
    return user.groups.filter(name='Admin').exists()



# def create_task(request):
#     participant = Participant.objects.all()
#     category = Category.objects.all()
#     form = TaskModel(participant=participant, category=category)

#     if request.method == "POST":
#         form = TaskModel(request.POST, participant=participant, category=category)
#         if form.is_valid():
#             data = form.cleaned_data
#             event = Event.objects.create(
#                 name=data["name"],
#                 description=data["description"],
#                 date=data["date"],
#                 time=data["time"],
#                 location=data["location"],
#                 category=Category.objects.get(id=data["category"])
#             )
            
#             event.participant.add(*Participant.objects.filter(id__in=data["participant"]))
#             messages.success(request, 'Event added successfully')
#             return redirect('dashboard')

#     return render(request, "form.html", {"form": form})


@login_required
@permission_required("Event.add_event",login_url='no-permission')
def create_task(request):
    if request.method == "POST":
        form = TaskModel(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event added successfully")
            return redirect("dashboard")
    else:
        form = TaskModel()

    return render(request, "form.html", {"form": form})

create_decorator=[login_required,permission_required("Event.add_event",login_url='no-permission')]


class Create_Event(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required="Event.add_event"
    login_url="no-permission"
    def get(self,request,*args, **kwargs):
        form = TaskModel()
        return render(request, "form.html", {"form": form})
    def post(self,request,*args, **kwargs):
        form = TaskModel(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event added successfully")
            return redirect("dashboard")



# def update_event(request, id):
#     events = Event.objects.get(id=id)
#     participant = Participant.objects.all()
#     category = Category.objects.all()

#     if request.method == "POST":
#         form = TaskModel(request.POST, participant=participant, category=category)
#         if form.is_valid():
#             data = form.cleaned_data
#             events.name = data["name"]
#             events.description = data["description"]
#             events.date = data["date"]
#             events.time = data["time"]
#             events.location = data["location"]
#             events.category = Category.objects.get(id=data["category"])
#             events.save()

#             events.participant.set(Participant.objects.filter(id__in=data["participant"]))
#             messages.success(request, 'The event was edited successfully')
#             return redirect('dashboard')
#     else:
#         form = TaskModel(
#             participant=participant,
#             category=category,
#             initial={
#                 'name': events.name,
#                 'description': events.description,
#                 'date': events.date,
#                 'time': events.time,
#                 'location': events.location,
#                 'category': events.category.id,
#                 'participant': events.participant.values_list('id', flat=True)
#             }
#         )

#     return render(request, "form.html", {"form": form})

@login_required
@permission_required("Event.change_event",login_url='no-permission')
def update_event(request, id):
    event = Event.objects.get(id=id)
    if request.method == "POST":
        form = TaskModel(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "The event was edited successfully")
            return redirect("dashboard")
    else:
        form = TaskModel(instance=event)

    return render(request, "form.html", {"form": form})


class Update_Event(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    model=Event    
    template_name="form.html"
    form_class=TaskModel
    pk_url_kwarg='id'
    def post(self, request, *args, **kwargs):
        self.object=self.get_object()
        form = TaskModel(request.POST, instance=self.get_object())
        if form.is_valid():
            form.save()
            messages.success(request, "The event was edited successfully")
            return redirect("update_event",self.object.id)

        return redirect('update_event',self.object.id)
        

@login_required
@permission_required("Event.delete_event",login_url='no-permission')
def delete_event(request,id):
    if request.method =="POST":
        event=Event.objects.get(id=id)
        event.delete()
        messages.success(request,'the event deleted successfully')
        return redirect('dashboard')
    


# def show_dashboard(request):
#     type=request.GET.get('type','all')
#     today=timezone.now().date()
    
    
#     base_query=Event.objects.prefetch_related('participant').select_related('category')
#     if type=="upcoming":
#         event=base_query.filter(date__gt=today)
#         event_condition="upcoming events"
#     elif type =="past":
#         event_condition="past events"
#         event=base_query.filter(date__lt=today)
#     elif type=="all_event":
#         event_condition="all events"
#         event=base_query.all()
#     elif type=="all":
#         event_condition="Todays events"
#         event=base_query.filter(date=today)

    
#     counts = Event.objects.annotate(num_participants=Count('participant')).aggregate(
#         total=Count('id', distinct=True),
#         participant_count=Count('participant', distinct=True),
#         upcoming=Count('id', filter=Q(date__gte=today), distinct=True),
#         past=Count('id', filter=Q(date__lt=today), distinct=True)
#     )
#     context={
#         "events":event,
#         "count":counts,
#         "event_condition": event_condition
#     }
#     return render(request,'dashboard.html',context)

@login_required
@permission_required("Event.add_event",login_url='no-permission')
def show_dashboard(request):
    type = request.GET.get("type", "all")
    today = timezone.now().date()

    base_query = Event.objects.prefetch_related("participants").select_related("category")
    if type == "upcoming":
        event = base_query.filter(date__gt=today)
        event_condition = "upcoming events"
    elif type == "past":
        event_condition = "past events"
        event = base_query.filter(date__lt=today)
    elif type == "all_event":
        event_condition = "all events"
        event = base_query.all()
    elif type == "all":
        event_condition = "Todays events"
        event = base_query.filter(date=today)

    counts = Event.objects.annotate(num_participants=Count("participants")).aggregate(
        total=Count("id", distinct=True),
        participant_count=Count("participants", distinct=True),
        upcoming=Count("id", filter=Q(date__gte=today), distinct=True),
        past=Count("id", filter=Q(date__lt=today), distinct=True),
    )
    context = {
        "events": event,
        "count": counts,
        "event_condition": event_condition,
    }
    return render(request, "dashboard.html", context)



# def home(request):
    
#     events=Event.objects.prefetch_related('participant').select_related('category').all()
    
    

#     type=request.GET.get('type','all')
#     if type == 'technology':

#         events=Event.objects.filter(category__name='Technology')
#     elif type =='social':
#         events=Event.objects.filter(category__name='social event')
    


#     if request.method =='POST':
#         start_date=request.POST.get('start_date')
#         end_date=request.POST.get('end_date')
        
#         events=Event.objects.filter(date__range=(start_date, end_date))
    
#     query = request.GET.get('search')  
#     if query:
#         events = events.filter(
#             Q(name__icontains=query) |
#             Q(location__icontains=query)
#         )

    
#     count = Event.objects.aggregate(
#         technology_count=Count('id', filter=Q(category__name__iexact='Technology')),
#         social_count=Count('id', filter=Q(category__name__iexact='social event'))
#     )

#     context={

#             "events": events,
#             "count": count,
#         }
#     return render(request,'home.html',context)
  
@login_required
def home(request):
    events = Event.objects.prefetch_related("participants").select_related("category").all()

    type = request.GET.get("type", "all")
    if type == "technology":
        events = Event.objects.filter(category__name="Technology")
    elif type == "social":
        #events = Event.objects.filter(category__name="social event")
        events = Event.objects.filter(category__name="Social")

    if request.method == "POST":
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        events = Event.objects.filter(date__range=(start_date, end_date))

    query = request.GET.get("search")
    if query:
        events = events.filter(
            Q(name__icontains=query) |
            Q(location__icontains=query)
        )

    count = Event.objects.aggregate(
        technology_count=Count("id", filter=Q(category__name__iexact="Technology")),
        social_count=Count("id", filter=Q(category__name__iexact="Social")),
    )

    context = {
        "events": events,
        "count": count,
    }
    return render(request, "home.html", context)



    


@login_required
def event_detail(request,id):
    event=Event.objects.get(id=id)
    context={
        "event":event
    }
    return render(request,'details.html',context)
class Event_detail(DetailView,LoginRequiredMixin):
    model=Event
    template_name="details.html"
    context_object_name="event"
    pk_url_kwarg='id'

    

@login_required
def rsvp(request,event_id):
    event=Event.objects.get(id=event_id)
    if request.user in event.participants.all():
        return HttpResponse("You have already rsvp")
    else:
        event.participants.add(request.user)
        subject="Rsvp events"
        message=f"hi {request.user.first_name}\n you rsvp for {event}"
        recepient_list=[request.user.email]
        send_mail(subject,message,settings.EMAIL_HOST_USER , recepient_list)
        messages.success(request,"you have rsvp succesfully\ncheck your mail")
        return redirect('home')



# def add_participant(request):
#     if request.method == "POST":
#         form = ParticipantForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Participant added successfully.")
#             return redirect('dashboard')  
#     else:
#         form = ParticipantForm()
#     return render(request, "add_participant.html", {"form": form})
@login_required
@permission_required("Event.add_category",login_url='no-permission')
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully.")
            return redirect('dashboard')
    else:
        form = CategoryForm()
    return render(request, "add_category.html", {"form": form})


@login_required
def dashboard(request):
    if is_participant(request.user):
        return redirect('home')
    elif is_organizer(request.user):
        return redirect('dashboard')
    elif is_admin(request.user):
        return redirect('admin-dashboard')