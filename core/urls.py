from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', main_view, name='main_view'),
    path('singup/', singup_view, name='sing_view'),
    path('<str:ref_code>', main_view, name='main_view'),
    path('painel/', PainelView.as_view(), name='painel_view'),
    path('ranking/', RankingView.as_view(), name='ranking_view'),
    path('indicacao/', IndicacaoView.as_view(), name='indicacao_view'),
    path('perfil/', PerfilView.as_view(), name='perfil_view'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
