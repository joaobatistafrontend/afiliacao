from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'input-field'}))
    whatsapp = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'input-field'}))
    chave_pix = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'input-field'}))
    banco = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'input-field'}))
    ano_carro = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'input-field'}))
    modelo = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'input-field'}))

    class Meta:
        model = User
        fields = ('username','email','whatsapp','password1','password2')

    def save(self, commit=True, ref_code=None):
        user = super().save(commit=commit)
        user.email = self.cleaned_data['email']
        user.save()
        # Create or update profile
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.whatsapp = self.cleaned_data['whatsapp']
        profile.chave_pix = self.cleaned_data['chave_pix']
        profile.banco = self.cleaned_data['banco']
        profile.email = self.cleaned_data['email']
        profile.ano_carro = self.cleaned_data['ano_carro']
        profile.modelo = self.cleaned_data['modelo']

        if ref_code:
            # atribuir recomendador via código
            try:
                recom = UserProfile.objects.get(code=ref_code)
                profile.recomended_by = recom.user
            except UserProfile.DoesNotExist:
                pass
        profile.save()
        return user


class SolicitarSaldoForm(forms.Form):
    valor = forms.DecimalField(
        label='Valor',
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'input-solicitar',
            'placeholder': 'Ex: 100.00',
            'step': '0.01',
            'min': '0'
        })
    )

    def __init__(self, *args, **kwargs):
        self.saldo_disponivel = kwargs.pop('saldo_disponivel', 0)
        super().__init__(*args, **kwargs)

    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        if valor is None:
            return valor
        if valor > self.saldo_disponivel:
            raise forms.ValidationError("Valor solicitado excede seu saldo disponível.")
        return valor
