from django.db.models.signals import post_save,m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.contrib.auth import get_user_model
User=get_user_model()
@receiver(post_save,sender=User)
def send_activation_email(sender,instance,created, **kwargs):
    if created:
        token=default_token_generator.make_token(instance)
        activate_url=f"http://127.0.0.1:8000/users/activate/{instance.id}/{token}/"
        subject="Activate your mail"
        message=f"hi {instance.username},\nplease activate your account by clicking this link\n{activate_url}"
        recepient_list=[instance.email]
        try:
            send_mail(subject,message,settings.EMAIL_HOST_USER , recepient_list)
        except Exception as e:
            print(f"failded to sent email to {instance.email}, due to {str(e)}")


# @receiver(post_save,sender=User)
# def assign_role(sender,instance,created,**kwargs):
#     if created:
#         participant,created=Group.objects.get_or_create(name='participant')
#         instance.groups.add(participant)
#         instance.save()
    
@receiver(post_save, sender=User)
def assign_role(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.is_superuser:
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        instance.groups.add(admin_group)
    else:
        participant_group, _ = Group.objects.get_or_create(name='participant')
        instance.groups.add(participant_group)


# @receiver(post_save,sender=User)
# def create_or_update_profile(sender,instance,created,**kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)
    