from django.db import models
from django.contrib.auth.models import User

# ==========================================
# 1. CONFIGURAÇÕES DO SISTEMA (Geridas pelo Admin)
# ==========================================

class ServiceType(models.Model):
    """
    Define os tipos de vistos/serviços disponíveis (ex: Visto D7, CPLP).
    Isto permite criar novos tipos de visto sem mexer no código.
    """
    name = models.CharField(max_length=100, verbose_name="Nome do Serviço")
    description = models.TextField(verbose_name="Descrição do Requisito")
    estimated_wait_time = models.IntegerField(default=30, verbose_name="Tempo Estimado (Dias)")

    class Meta:
        verbose_name = "Tipo de Serviço"
        verbose_name_plural = "Tipos de Serviço"

    def __str__(self):
        return self.name


class RequiredDoc(models.Model):
    """
    Checklist de documentos necessários para CADA tipo de serviço.
    Ex: O Visto D7 precisa de 'Extrato Bancário', o CPLP precisa de 'Certificado Criminal'.
    """
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, related_name='requirements')
    doc_name = models.CharField(max_length=100, verbose_name="Nome do Documento")
    is_mandatory = models.BooleanField(default=True, verbose_name="É Obrigatório?")

    class Meta:
        verbose_name = "Documento Necessário"
        verbose_name_plural = "Documentos Necessários"

    def __str__(self):
        return f"{self.doc_name} ({self.service_type.name})"


# ==========================================
# 2. DADOS DO UTILIZADOR (PERFIL)
# ==========================================

class Profile(models.Model):
    """
    Estende o utilizador padrão do Django para guardar dados extra de imigração.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Dados de Identificação
    passport = models.CharField(max_length=20, verbose_name="Número de Passaporte")
    nif = models.CharField(max_length=9, blank=True, null=True, verbose_name="NIF")
    nationality = models.CharField(max_length=100, blank=True, verbose_name="Nacionalidade")
    
    # Dados de Contacto
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telemóvel")
    address = models.TextField(blank=True, null=True, verbose_name="Morada Completa")

    def __str__(self):
        # Tenta mostrar o nome completo, se não tiver, mostra o username
        return f"Perfil de {self.user.get_full_name() or self.user.username}"


# ==========================================
# 3. O PROCESSO DE IMIGRAÇÃO (CORE)
# ==========================================

class Process(models.Model):
    """
    Representa um pedido de visto feito por um utilizador.
    """
    STATUS_CHOICES = [
        ('draft', 'Rascunho (Em Preenchimento)'),
        ('submitted', 'Submetido (Aguardar Análise)'),
        ('review', 'Em Análise Técnica'),
        ('approved', 'Aprovado (Pronto p/ Agendar)'),
        ('rejected', 'Rejeitado / Devolvido'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='processes')
    service_type = models.ForeignKey(ServiceType, on_delete=models.PROTECT, verbose_name="Tipo de Visto")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Estado Atual")
    
    # Datas de controlo
    submission_date = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")

    class Meta:
        verbose_name = "Processo de Imigração"
        verbose_name_plural = "Processos de Imigração"
        ordering = ['-submission_date'] # Mostra os mais recentes primeiro

    def __str__(self):
        return f"Processo #{self.id:04d} - {self.service_type.name}"


class Attachment(models.Model):
    """
    Ficheiros (PDFs/Imagens) enviados pelo utilizador para cumprir um Requisito.
    """
    STATUS_CHOICES = [
        ('pending', 'Pendente de Validação'),
        ('valid', 'Válido / Aceite'),
        ('invalid', 'Inválido / Rejeitado'),
    ]

    process = models.ForeignKey(Process, on_delete=models.CASCADE, related_name='attachments')
    required_doc = models.ForeignKey(RequiredDoc, on_delete=models.PROTECT, verbose_name="Requisito")
    
    # Upload organizado por ano/mês para não encher uma pasta só
    file = models.FileField(upload_to='documents/%Y/%m/', verbose_name="Ficheiro")
    
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Envio")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_feedback = models.TextField(blank=True, null=True, verbose_name="Motivo da Rejeição", help_text="Preencher apenas se rejeitar o documento.")

    class Meta:
        verbose_name = "Documento Anexado"
        verbose_name_plural = "Documentos Anexados"

    def __str__(self):
        return f"Doc: {self.required_doc.doc_name} (Proc #{self.process.id})"


# ==========================================
# 4. AGENDAMENTO FINAL (TICKET)
# ==========================================

class Appointment(models.Model):
    """
    Marcação presencial gerada automaticamente após o processo ser 'approved'.
    """
    process = models.OneToOneField(Process, on_delete=models.CASCADE, verbose_name="Processo Associado")
    appointment_date = models.DateTimeField(verbose_name="Data e Hora do Agendamento")
    location = models.CharField(max_length=100, default="Loja AIMA Lisboa - Campus Justiça")
    ticket_number = models.CharField(max_length=20, unique=True, verbose_name="Senha Digital")

    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"

    def __str__(self):
        return f"Senha {self.ticket_number} - {self.appointment_date.strftime('%d/%m/%Y')}"