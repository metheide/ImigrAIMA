from django.urls import path
from . import views

urlpatterns = [
    # ==========================================
    # 1. PÁGINAS PÚBLICAS & API
    # ==========================================
    path('', views.home, name='home'),
    path('api/processos/', views.api_get_processes, name='api_get_processes'),

    # ==========================================
    # 2. CONTA DE UTILIZADOR
    # ==========================================
    path('registar/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('perfil/', views.edit_profile, name='edit_profile'),

    # ==========================================
    # 3. CRIAÇÃO E GESTÃO DE PROCESSOS
    # ==========================================
    # Iniciar
    path('novo-processo/', views.create_process, name='create_process'),
    
    # Detalhes e Fluxo
    path('processo/<int:process_id>/', views.process_detail, name='process_detail'),
    path('processo/<int:process_id>/upload/', views.upload_document, name='upload_document'),
    path('processo/<int:process_id>/submeter/', views.submit_process_final, name='submit_process_final'),
    path('processo/<int:process_id>/cancelar/', views.cancel_process, name='cancel_process'),

    # Ações Específicas de Documentos
    path('documento/<int:doc_id>/apagar/', views.delete_document, name='delete_document'),

    # ==========================================
    # 4. AGENDAMENTOS & OUTPUTS (PDF)
    # ==========================================
    path('processo/<int:process_id>/agendar/', views.generate_appointment, name='generate_appointment'),
    path('agendamento/<int:appointment_id>/pdf/', views.generate_pdf, name='generate_pdf'),

    # ==========================================
    # 5. ÁREA DE GESTÃO (STAFF)
    # ==========================================
    path('gestao/', views.manager_dashboard, name='manager_dashboard'),
]