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

class PerfilView(LoginRequiredMixin, TemplateView):
    template_name = 'home/perfil.html'
    model = UserProfile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(UserProfile, user=self.request.user)
        context['my_recs'] = profile.get_recommended_profile()
        return context

class PainelView(LoginRequiredMixin, View):
    template_name = 'home/painel.html'

    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(UserProfile, user=request.user)
        is_vendedor = Vendedora.objects.filter(user=profile.user).exists()
        form = SolicitarSaldoForm(saldo_disponivel=profile.ponts)
        context = {
            'my_recs': profile.get_recommended_profile(),
            'ref_code': profile.code,
            'ponts': str(profile.ponts),
            'qrcode': profile.qr,
            'form': form,
            'is_vendedor': is_vendedor,
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
                f"👤 *Usuário:* {(profile.user.get_full_name() or profile.user.username or '---')}\n"
                f"👤 *Saldo em conta:* {profile.ponts if profile.ponts is not None else '---'}\n"
                f"📧 *Email:* {profile.user.email or '---'}\n"
                f"📱 *WhatsApp:* {profile.whatsapp or '---'}\n"
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


class SignUpView(View):
    template_name = 'registration/singup.html'
    form_class = SignUpForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        code = str(kwargs.get('ref_code'))
        profile_id = request.session.get('recomended_by', None)
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save()
            user_profile = UserProfile.objects.get(user=instance)
            #ultimo vendedor que pegou a venda
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
                        # Atualize o campo last_notified para agora
                        vendedor_indicador.last_notified = timezone.now()
                        vendedor_indicador.save()
                    elif vendedor:
                        enviar_mensagem([vendedor.user.userprofile.whatsapp], MENSAGEM)
                        vendedor.last_notified = timezone.now()
                        vendedor.save()
                except UserProfile.DoesNotExist:
                    pass

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