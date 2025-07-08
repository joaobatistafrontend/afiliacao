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
from django.db.models import F


def get_user_profile(user):
    return get_object_or_404(UserProfile, user=user)

    
def get_vendedor():
    return Vendedora.objects.order_by('last_notified').first()


class PerfilView(LoginRequiredMixin, TemplateView):
    template_name = 'home/perfil.html'
    model = UserProfile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_user_profile(self.request.user)
        is_vendedor = Vendedora.objects.filter(user=profile.user).exists()
        context['my_recs'] = profile.get_recommended_profile()
        context ['is_vendedor'] = is_vendedor
        return context

class PainelView(LoginRequiredMixin, View):
    template_name = 'home/painel.html'

    def get(self, request, *args, **kwargs):
        profile = get_user_profile(self.request.user)
        is_vendedor = Vendedora.objects.filter(user=profile.user).exists()
        form = SolicitarSaldoForm(saldo_disponivel=profile.ponts)
        vendedor = Vendedora.objects.order_by('last_notified').first()
        indicador = None
        zap_indicador = None
    
        # Busca o perfil do indicador (quem indicou o usuário atual)
        if profile.recomended_by:
            try:
                indicador = UserProfile.objects.get(user=profile.recomended_by)
                zap_indicador = indicador.whatsapp
            except UserProfile.DoesNotExist:
                zap_indicador = None
        else:
            zap_indicador = vendedor.user.userprofile.whatsapp
                
    
        context = {
            'my_recs': profile.get_recommended_profile(),
            'ref_code': profile.code,
            'ponts': str(profile.ponts),
            'qrcode': profile.qr,
            'form': form,
            'is_vendedor': is_vendedor,
            'zap_indicador': zap_indicador,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        profile = get_user_profile(self.request.user)
        form = SolicitarSaldoForm(request.POST, saldo_disponivel=profile.ponts)

        if form.is_valid():
            instance = form.cleaned_data
            valor = form.cleaned_data['valor']

            MENSAGEM = (
                f"🎉 *Usuário solicitando R$ {valor},00 de saque!*\n\n"
                f"👤 *Usuário:* {(profile.user.get_full_name() or profile.user.username or '---')}\n"
                f"👤 *Saldo em conta:* {profile.ponts if profile.ponts is not None else '---'}\n"
                f"📧 *Email:* {profile.user.email or '---'}\n"
                f"📱 *WhatsApp:* {profile.whatsapp or '---'}\n"
                f"🚗 *Modelo do carro:* {profile.modelo_carro or '---'}\n"
                f"📅 *Ano do carro:* {profile.ano_carro or '---'}\n"
                f"🔗 *Código de Indicação:* {profile.code or '---'}\n"
                f"🙋‍♂️ *Indicado por:* "
                    f"{profile.recomended_by.get_full_name() if profile.recomended_by else '---'}\n"
                f"🗓️ *Data de Cadastro:* "
                    f"{profile.user.date_joined.strftime('%d/%m/%Y') if profile.user.date_joined else '---'}\n"
            )
            finaceiro_indicador = Finaceiro.objects.filter(responsavel=profile.recomended_by).first()
            if finaceiro_indicador:
                enviar_mensagem([finaceiro_indicador.responsavel.userprofile.whatsapp], MENSAGEM)
            else:
                finaceiro_aleatorio = Finaceiro.objects.order_by('?').first()
                if finaceiro_aleatorio:
                    enviar_mensagem([finaceiro_aleatorio.responsavel.userprofile.whatsapp], MENSAGEM)

            return redirect('painel_view')
        else:
            return render(request, 'home/painel.html', {'form': form})





class RankingView(LoginRequiredMixin, TemplateView):
    template_name = 'home/ranking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_user_profile(self.request.user)
        is_vendedor = Vendedora.objects.filter(user=profile.user).exists()
        glocal = UserProfile.objects.all()
        ranking = profile.get_recommended_global()
        context['my_recs'] = profile.get_recommended_profile()
        context['ranking'] = ranking
        context ['is_vendedor'] = is_vendedor
        return context

class IndicacaoView(LoginRequiredMixin, ListView):
    template_name = 'home/indeicacao.html'
    model = UserProfile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(UserProfile, user=self.request.user)
        is_vendedor = Vendedora.objects.filter(user=profile.user).exists()
        context['my_recs'] = profile.get_recommended_profile()
        context ['is_vendedor'] = is_vendedor
        return context


class SignUpView(View):
    template_name = 'registration/singup.html'
    form_class = SignUpForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        profile_id = request.session.get('recomended_by', None)
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save()
            user_profile = UserProfile.objects.get(user=instance)
            vendedor = Vendedora.objects.order_by('last_notified').first()
            if profile_id is not None:
                try:
                    recommended_by_profile = UserProfile.objects.get(id=profile_id)
                    vendedor_proprio = recommended_by_profile.atendido_por.all()
                    vendedor_proprio = vendedor_proprio.order_by('last_notified').first()
                    recommended_by_profile.save()
                    user_profile.recomended_by = recommended_by_profile.user
                    user_profile.save()
                    MENSAGEM = (
                        f"🎉 *Novo usuário cadastrado!*\n\n"
                        f"👤 *Usuário:* {instance.get_full_name() or instance.username}\n"
                        f"📧 *Email:* {instance.email}\n"
                        f"📱 *WhatsApp:* {user_profile.whatsapp}\n"
                        f"🚗 *Modelo do carro:* {user_profile.modelo or '---'}\n"
                        f"📅 *Ano do carro:* {user_profile.ano_carro or '---'}\n"
                        f"🔗 *Código de Indicação:* {recommended_by_profile.code}\n"
                        f"🙋‍♂️ *Indicado por:* {recommended_by_profile.user.get_full_name() or recommended_by_profile.user.username}\n"
                        f"🗓️ *Data de Cadastro:* {instance.date_joined.strftime('%d/%m/%Y')}\n"
                    )
                    vendedor_indicador = Vendedora.objects.filter(user=recommended_by_profile.user).first()
                    if vendedor_proprio:
                        enviar_mensagem([vendedor_proprio.user.userprofile.whatsapp], MENSAGEM)
                        vendedor_indicador.last_notified = timezone.now()
                        vendedor_indicador.save()
                    elif vendedor_indicador:
                        enviar_mensagem([vendedor_indicador.user.userprofile.whatsapp], MENSAGEM)
                        vendedor_indicador.last_notified = timezone.now()
                        vendedor_indicador.save()
                except UserProfile.DoesNotExist:
                    pass
            else:
                # Não veio recomendação, envia mensagem para o último vendedor
                MENSAGEM = (
                    f"🎉 *Novo usuário cadastrado!*\n\n"
                    f"👤 *Usuário:* {instance.get_full_name() or instance.username}\n"
                    f"📧 *Email:* {instance.email}\n"
                    f"📱 *WhatsApp:* {user_profile.whatsapp}\n"
                    f"🚗 *Modelo do carro:* {user_profile.modelo or '---'}\n"
                    f"📅 *Ano do carro:* {user_profile.ano_carro or '---'}\n"
                    f"🔗 *Código de Indicação:* ---\n"
                    f"🙋‍♂️ *Indicado por:* ---\n"
                    f"🗓️ *Data de Cadastro:* {instance.date_joined.strftime('%d/%m/%Y')}\n"
                )
                if vendedor:
                    enviar_mensagem([vendedor.user.userprofile.whatsapp], MENSAGEM)
                    vendedor.last_notified = timezone.now()
                    vendedor.save()
    
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
            return redirect('painel_view')
    
        return render(request, self.template_name, {'form': form})


def main_view(request, ref_code=None, *args, **kwargs):
    if ref_code:
        try:
            profile = UserProfile.objects.get(code=ref_code)
            request.session['recomended_by'] = profile.id
            print('id:', profile.id)
        except UserProfile.DoesNotExist:
            pass
    print(request.session.get_expiry_date())
    return render(request, 'main.html')