from django.db import models
from django.conf import settings

# Create your models here.


from django.db import models

from django.db.models.signals import post_save,m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail

from django.contrib.auth import get_user_model
User=get_user_model()

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    asset=models.ImageField(upload_to='event_asset',blank=True,null=True,default='event_asset/default.png')
    location = models.CharField(max_length=100)
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="events"
    )
    participants = models.ManyToManyField(
        User,
        related_name="rsvp",
        blank=True
    )

    def __str__(self):
        return self.name




class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


@receiver(m2m_changed, sender=Event.participants.through)
def notify_participants_on_event_creation(sender, instance, action, **kwargs):
    if action=='post_add':
        
        assigned_emails = [participant.email for participant in instance.participants.all()]
        send_mail(
            "new event rsvp",
            f" You have been added to the event: {instance.name}.",
            "shsajal8561@gmail.com",
            assigned_emails,
            fail_silently=False,
        )





# class Event(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     date = models.DateField()
#     time = models.TimeField()
#     location = models.CharField(max_length=100)
#     category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="event")

#     def __str__(self):
#         return self.name




# class Participant(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     events = models.ManyToManyField(Event, related_name="participant", blank=True)

#     def __str__(self):
#         return self.name
    
# class Category(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()

#     def __str__(self):
#         return self.name
    
