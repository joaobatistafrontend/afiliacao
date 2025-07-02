from django.urls import path, re_path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('singup/', SignUpView.as_view(), name='sing_view'),
    path('painel/', PainelView.as_view(), name='painel_view'),
    path('ranking/', RankingView.as_view(), name='ranking_view'),
    path('indicacao/', IndicacaoView.as_view(), name='indicacao_view'),
    path('perfil/', PerfilView.as_view(), name='perfil_view'),
    re_path(r'^(?P<ref_code>[\w\-]+)?/?$', main_view, name='main_view'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)