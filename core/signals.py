from .models import UserProfile
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


#funcao que cria o perfil do usuario quando o usuario for criado
@receiver(post_save, sender=User)
def post_save_create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    
    