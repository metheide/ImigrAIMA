from django.contrib import admin
from .models import ServiceType, RequiredDoc, Profile, Process, Attachment, Appointment

# 1. Configuração dos Tipos de Serviço
class RequiredDocInline(admin.TabularInline):
    model = RequiredDoc
    extra = 1

@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'estimated_wait_time')
    inlines = [RequiredDocInline]

# 2. Configuração do Perfil (AQUI ESTAVA O ERRO)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # Removemos 'full_name' e 'passport_number'
    # Adicionamos 'passport' (o novo nome) e 'nif'
    list_display = ('user', 'passport', 'nif', 'phone', 'nationality')
    search_fields = ('user__username', 'user__first_name', 'passport', 'nif')

# 3. Configuração dos Processos
class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0
    readonly_fields = ('uploaded_at',)

@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'service_type', 'status', 'submission_date')
    list_filter = ('status', 'service_type', 'submission_date')
    search_fields = ('user__username', 'id')
    inlines = [AttachmentInline]
    
    # Ações rápidas para aprovar/rejeitar em massa
    actions = ['mark_as_approved', 'mark_as_rejected']

    @admin.action(description='Aprovar processos selecionados')
    def mark_as_approved(self, request, queryset):
        queryset.update(status='approved')

    @admin.action(description='Rejeitar processos selecionados')
    def mark_as_rejected(self, request, queryset):
        queryset.update(status='rejected')

# 4. Configuração dos Agendamentos
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('ticket_number', 'appointment_date', 'process', 'location')
    list_filter = ('location', 'appointment_date')
    search_fields = ('ticket_number', 'process__user__username')