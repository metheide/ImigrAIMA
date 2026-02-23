# core/urls.py (O ficheiro PRINCIPAL do projeto)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Painel de Admin do Django
    path('admin/', admin.site.urls),
    
    # As rotas da nossa aplicação 'website'
    path('', include('website.urls')),
    
    # Sistema de Login/Logout padrão do Django
    # Isto permite que o /accounts/login/ funcione automaticamente
    path('accounts/', include('django.contrib.auth.urls')), 
]

# --- IMPORTANTE: ISTO PERMITE VER OS FICHEIROS UPLOADADOS EM MODO DEBUG ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)