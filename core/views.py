from datetime import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DetailView, View, ListView
from .models import UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from core.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import *
from .utils import enviar_mensagem
# Create your views here.
from django.db.models import F

class PerfilView(LoginRequiredMixin, TemplateView):
    template_name = 'home/perfil.html'
    model = UserProfile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(UserProfile, user=self.request.user)
        context['my_recs'] = profile.get_recommended_profile()
        context['user'] = self.request.user
        context['ponts'] = str(profile.ponts)
        context['status'] = profile.status
        return context

class PainelView(LoginRequiredMixin, View):
    template_name = 'home/painel.html'

    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(UserProfile, user=request.user)
        form = SolicitarSaldoForm(saldo_disponivel=profile.ponts)
        context = {
            'my_recs': profile.get_recommended_profile(),
            'ref_code': profile.code,
            'ponts': str(profile.ponts),
            'qrcode': profile.qr,
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(UserProfile, user=request.user)
        form = SolicitarSaldoForm(request.POST, saldo_disponivel=profile.ponts)

        if form.is_valid():
            instance = form.cleaned_data
            valor = form.cleaned_data['valor']

            MENSAGEM = (
                    f"🎉 *Usuário solicitando R$ {valor},00 de saque!*\n\n"
                    f"👤 *Usuário:* {profile.user.get_full_name() or profile.user}\n"
                    f"👤 *Saldo em conta:* {profile.ponts}\n"
                    f"📧 *Email:* {profile.user.email}\n"
                    f"📱 *WhatsApp:* {profile.whatsapp}\n"
                    f"🔗 *Código de Indicação:* {profile.code}\n"
                    f"🙋‍♂️ *Indicado por:* {profile.recomended_by}\n"
                    f"🗓️ *Data de Cadastro:* {profile.user.date_joined.strftime('%d/%m/%Y')}\n"
                    )
            finaceiro_indicador = Finaceiro.objects.filter(responsavel=profile.recomended_by).first()
            if finaceiro_indicador:
                enviar_mensagem([finaceiro_indicador.responsavel.userprofile.whatsapp], MENSAGEM)
            else:
                finaceiro_aleatorio = Finaceiro.objects.order_by('?').first()
                if finaceiro_aleatorio:
                    enviar_mensagem([finaceiro_aleatorio.responsavel.userprofile.whatsapp], MENSAGEM)

            return redirect('painel_view')            
            
        return redirect('painel_view')

class RankingView(LoginRequiredMixin, TemplateView):
    template_name = 'home/ranking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(UserProfile, user=self.request.user)
        context['my_recs'] = profile.get_recommended_profile()
        glocal = UserProfile.objects.all()
        ranking = profile.get_recommended_global()
        context['ranking'] = ranking
        return context

class IndicacaoView(LoginRequiredMixin, ListView):
    template_name = 'home/indeicacao.html'
    model = UserProfile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(UserProfile, user=self.request.user)
        context['my_recs'] = profile.get_recommended_profile()
        return context

# def my_recommendations_view(request, *args, **kwargs):
#     profile = UserProfile.objects.get(user=request.user)
#     my_recs = profile.get_recommended_profile()
#     context = {
#         'my_recs': my_recs,
#     }
    
#     return render(request, 'profiles/main.html', context)



def singup_view(request, *args, **kwargs):
    code = str(kwargs.get('ref_code'))
    profile_id = request.session.get('recomended_by', None)
    # print('profile_id:', profile_id)

    form = SignUpForm(request.POST or None)
    if form.is_valid():
        instance = form.save()  # instance = novo usuário (User)

        # buscar ou garantir o perfil do usuário criado
        user_profile = UserProfile.objects.get(user=instance)
        vendedor = Vendedora.objects.order_by('last_notified').first()
        
        # se veio código de recomendação, adicione
        if profile_id is not None:
            try:
                recommended_by_profile = UserProfile.objects.get(id=profile_id)
                recommended_by_profile.save()
                user_profile.recomended_by = recommended_by_profile.user
                user_profile.save()
                MENSAGEM = (
                    f"🎉 *Novo usuário cadastrado!*\n\n"
                    f"👤 *Usuário:* {instance.get_full_name() or instance.username}\n"
                    f"📧 *Email:* {instance.email}\n"
                    f"📱 *WhatsApp:* {user_profile.whatsapp}\n"
                    f"🔗 *Código de Indicação:* {recommended_by_profile.code}\n"
                    f"🙋‍♂️ *Indicado por:* {recommended_by_profile.user.get_full_name() or recommended_by_profile.user.username}\n"
                    f"🗓️ *Data de Cadastro:* {instance.date_joined.strftime('%d/%m/%Y')}\n"
                )
                vendedor_indicador = Vendedora.objects.filter(user=recommended_by_profile.user).first()
                if vendedor_indicador:
                    # Notifica diretamente o vendedor que indicou
                    enviar_mensagem([vendedor_indicador.user.userprofile.whatsapp], MENSAGEM)
                    vendedor_indicador.last_notified = timezone.now()
                    vendedor_indicador.save()
                elif vendedor:
                    # Notifica o próximo da fila
                    enviar_mensagem([vendedor_indicador.user.userprofile.whatsapp], MENSAGEM)
                    # Atualize o campo last_notified para agora
                    vendedor.last_notified = timezone.now()
                    vendedor.save()
            except UserProfile.DoesNotExist:
                pass  # ou faça alguma ação alternativa

        # autenticar e logar
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)

        return redirect('painel_view')

    return render(request, 'registration/singup.html', {'form': form})

def main_view(request, *args, **kwargs):
    code = str(kwargs.get('ref_code'))
    try:
       profile = UserProfile.objects.get(code=code)
       request.session['recomended_by'] = profile.id
       print('id:', profile.id)
    except:
        pass
    print(request.session.get_expiry_date())
    return render(request, 'main.html')
