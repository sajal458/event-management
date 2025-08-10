from django.shortcuts import render,redirect
from django.http import HttpResponse
from Event.forms import TaskModel,ParticipantForm, CategoryForm
from Event.models import Participant,Category,Event
from django.db.models import Count,Q
from django.utils import timezone
from django.contrib import messages

# Create your views here.
def view_task(request):
    return HttpResponse("hello")


# def create_task(request):
#     participant=Participant.objects.all()
#     category=Category.objects.all()
#     form=TaskModel(participant=participant,category=category)
#     if request.method == "POST":
#         form=TaskModel(request.POST,participant=participant,category=category)
       
#         if form.is_valid():
#            data=form.cleaned_data
#            name=data.get("name")
#            description = data.get('description')
#            date=data.get("date")
#            time=data.get("time")
#            location = data.get("location")
#            category_id=data.get("category")
#            participant=data.get("participant")
#            event=Event.objects.create(name=name,description=description,date =date,time=time,location=location,category=Category.objects.get(id=category_id))
#            for p_id in participant:
#                par=Participant.objects.get(id=p_id)
#                event.participant.add(par)
#            messages.success(request,'event added successfully')
#            return redirect('dashboard')
               


#     context={
#         "form":form
#     }
#     return render(request,"form.html",context)

def create_task(request):
    participant = Participant.objects.all()
    category = Category.objects.all()
    form = TaskModel(participant=participant, category=category)

    if request.method == "POST":
        form = TaskModel(request.POST, participant=participant, category=category)
        if form.is_valid():
            data = form.cleaned_data
            event = Event.objects.create(
                name=data["name"],
                description=data["description"],
                date=data["date"],
                time=data["time"],
                location=data["location"],
                category=Category.objects.get(id=data["category"])
            )
            
            event.participant.add(*Participant.objects.filter(id__in=data["participant"]))
            messages.success(request, 'Event added successfully')
            return redirect('dashboard')

    return render(request, "form.html", {"form": form})


# def update_event(request, id):
#     events = Event.objects.get(id=id)
#     participant = Participant.objects.all()
#     category = Category.objects.all()

#     if request.method == "POST":
#         form = TaskModel(request.POST, participant=participant, category=category)
#         if form.is_valid():
#             data = form.cleaned_data
#             name = data.get("name")
#             description = data.get('description')
#             date = data.get("date")
#             time = data.get("time")
#             location = data.get("location")
#             category_id = data.get("category")
#             participant_ids = data.get("participant")

        
#             events.name = name
#             events.description = description
#             events.date = date
#             events.time = time
#             events.location = location
#             events.category = Category.objects.get(id=category_id)
#             events.save()

#             events.participant.set([Participant.objects.get(id=p_id) for p_id in participant_ids])
#             messages.success(request,'the event edited successfully')
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
#                 'participant': [p.id for p in events.participant.all()]
#             }
#         )

                


#     context={
#         "form":form
#     }
#     return render(request,"form.html",context)



def update_event(request, id):
    events = Event.objects.get(id=id)
    participant = Participant.objects.all()
    category = Category.objects.all()

    if request.method == "POST":
        form = TaskModel(request.POST, participant=participant, category=category)
        if form.is_valid():
            data = form.cleaned_data
            events.name = data["name"]
            events.description = data["description"]
            events.date = data["date"]
            events.time = data["time"]
            events.location = data["location"]
            events.category = Category.objects.get(id=data["category"])
            events.save()

            events.participant.set(Participant.objects.filter(id__in=data["participant"]))
            messages.success(request, 'The event was edited successfully')
            return redirect('dashboard')
    else:
        form = TaskModel(
            participant=participant,
            category=category,
            initial={
                'name': events.name,
                'description': events.description,
                'date': events.date,
                'time': events.time,
                'location': events.location,
                'category': events.category.id,
                'participant': events.participant.values_list('id', flat=True)
            }
        )

    return render(request, "form.html", {"form": form})

def delete_event(request,id):
    if request.method =="POST":
        event=Event.objects.get(id=id)
        event.delete()
        messages.success(request,'the event deleted successfully')
        return redirect('dashboard')
    


def show_dashboard(request):
    type=request.GET.get('type','all')
    today=timezone.now().date()
    
    
    base_query=Event.objects.prefetch_related('participant').select_related('category')
    if type=="upcoming":
        event=base_query.filter(date__gt=today)
        event_condition="upcoming events"
    elif type =="past":
        event_condition="past events"
        event=base_query.filter(date__lt=today)
    elif type=="all_event":
        event_condition="all events"
        event=base_query.all()
    elif type=="all":
        event_condition="Todays events"
        event=base_query.filter(date=today)

    
    counts = Event.objects.annotate(num_participants=Count('participant')).aggregate(
        total=Count('id', distinct=True),
        participant_count=Count('participant', distinct=True),
        upcoming=Count('id', filter=Q(date__gte=today), distinct=True),
        past=Count('id', filter=Q(date__lt=today), distinct=True)
    )
    context={
        "events":event,
        "count":counts,
        "event_condition": event_condition
    }
    return render(request,'dashboard.html',context)


def home(request):
    
    events=Event.objects.prefetch_related('participant').select_related('category').all()
    
    

    type=request.GET.get('type','all')
    if type == 'technology':

        events=Event.objects.filter(category__name='Technology')
    elif type =='social':
        events=Event.objects.filter(category__name='social event')
    


    if request.method =='POST':
        start_date=request.POST.get('start_date')
        end_date=request.POST.get('end_date')
        
        events=Event.objects.filter(date__range=(start_date, end_date))
    
    query = request.GET.get('search')  
    if query:
        events = events.filter(
            Q(name__icontains=query) |
            Q(location__icontains=query)
        )

    
    count = Event.objects.aggregate(
        technology_count=Count('id', filter=Q(category__name__iexact='Technology')),
        social_count=Count('id', filter=Q(category__name__iexact='Social'))
    )

    context={

            "events": events,
            "count": count,
        }
    return render(request,'home.html',context)
  
    
    
def event_detail(request,id):
    event=Event.objects.get(id=id)
    context={
        "event":event
    }
    return render(request,'details.html',context)






def add_participant(request):
    if request.method == "POST":
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Participant added successfully.")
            return redirect('dashboard')  
    else:
        form = ParticipantForm()
    return render(request, "add_participant.html", {"form": form})

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