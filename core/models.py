from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from .utils import generate_ref_code, gerar_qrcode_sobre_imagem
from django.db.models import Count

class StatusClinete(models.Model):
    status = models.CharField(max_length=60, blank=True, null=True, help_text='Status do usuário')

    def __str__(self):
        return (f'{self.status}')
    
class Planos(models.Model):
    planos = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return (f'{self.planos}') 

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=12, blank=True, help_text='codigo para compartilhar')
    recomended_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='ref_by')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    ponts = models.IntegerField(default=0, help_text='Pontos acumulados pelo usuário', blank=True, null=True)
    whatsapp = models.CharField(max_length=15, blank=True, null=True, help_text='Número de WhatsApp do usuário')

    status = models.ForeignKey(StatusClinete, on_delete=models.CASCADE, blank=True, null=True, help_text='Status do usuário')
    plano = models.ForeignKey(Planos, on_delete=models.CASCADE, blank=True, null=True, help_text='Status do usuário')
    lead_origin = models.IntegerField(default=1, help_text='Lead de Origin', blank=True, null=True)
    objservacao = models.CharField(max_length=125, blank=True, null=True, help_text='Observações')
    unit_id = models.IntegerField(default=1, help_text='Unidade Id', blank=True, null=True)


    def __str__(self):
        return (f'{self.user.username} - {self.code}')

    def get_recommended_profile(self):
        qs = UserProfile.objects.all()
        my_recs = []
        for profile in qs:
            if profile.recomended_by == self.user:
                my_recs.append(profile)

        return my_recs
    

    @classmethod
    def get_recommended_global(cls):
            # Agrupa por usuário recomendador e conta quantos indicaram
            results = (
                cls.objects
                .filter(recomended_by__isnull=False)
                .values('recomended_by')  # ID do User
                .annotate(total=Count('id'))  # Conta quantos indicados esse user tem
                .order_by('-total')[:10]  # Top 10
            )

            # Pega os nomes reais
            ranking = []
            for item in results:
                try:
                    user = User.objects.get(id=item['recomended_by'])
                    ranking.append({
                        'name': user.get_full_name() or user.username,
                        'total': item['total']
                    })
                except User.DoesNotExist:
                    continue

            return ranking
        

    def save(self, *args, **kwargs):
        if self.code == '':
            self.code = generate_ref_code()
            
        url = f"https://http://127.0.0.1:8000/{self.code}"
        caminho = 'static\img\qr.png'
        gerar_qrcode_sobre_imagem(url, self.code, caminho)
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


class Vendedora(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_notified = models.DateTimeField(default=timezone.now, help_text='Última vez que a vendedora foi notificada')
       
    def __str__(self):
        perfil = getattr(self.user, 'userprofile', None)
        whatsapp = perfil.whatsapp if perfil and perfil.whatsapp else 'Sem Telefone'
        return f'{self.user.username} - {whatsapp}'
    
    class Meta:
        verbose_name = 'Vendedora'
        verbose_name_plural = 'Vendedoras'


class Finaceiro(models.Model):
    responsavel = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        perfil = getattr(self.responsavel, 'userprofile', None)
        whatsapp = perfil.whatsapp if perfil and perfil.whatsapp else 'Sem Telefone'
        return f'{self.responsavel.username} - {whatsapp}'