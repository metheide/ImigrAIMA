# ==============================================================================
# IMIGRAÁGIL - VIEWS.PY (LÓGICA DO SISTEMA)
# ==============================================================================

# --- Imports do Django (Ferramentas essenciais) ---
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.db.models import Count, Q
from django.core.paginator import Paginator # Importado no topo para organização

# --- Imports Externos ---
import random
from xhtml2pdf import pisa 

# --- Meus Imports (Modelos e Formulários) ---
from .models import Process, RequiredDoc, Attachment, Appointment, Profile, ServiceType
from .forms import ProcessForm, CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm

# ==============================================================================
# 1. ÁREA PÚBLICA & API
# ==============================================================================

def home(request):
    """
    Página inicial do site (Landing Page).
    Acessível a qualquer pessoa, mesmo sem login.
    """
    return render(request, 'home.html')

def api_get_processes(request):
    """
    API REST para integração de sistemas externos.
    Retorna uma lista JSON dos últimos 10 processos públicos (anonimizados).
    """
    processes = Process.objects.all().order_by('-submission_date')[:10]
    data = []
    for p in processes:
        data.append({
            'id': p.id,
            'service': p.service_type.name,
            'status': p.get_status_display(),
            'date': p.submission_date.strftime('%Y-%m-%d')
        })
    return JsonResponse({'results': data, 'count': len(data)})

# ==============================================================================
# 2. ÁREA DO UTILIZADOR (CONTA E DASHBOARD)
# ==============================================================================

def signup(request):
    """
    Registo de novos utilizadores.
    Se o registo for válido, faz login automático imediatamente.
    """
    if request.user.is_authenticated:
        return redirect('dashboard') # Se já estiver logado, não precisa registar de novo

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Login automático
            messages.success(request, '🎉 Conta criada com sucesso! Bem-vindo.')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def dashboard(request):
    """
    Painel Principal do Imigrante.
    Mostra os processos, permite pesquisar e verificar se pode criar novos pedidos.
    """
    # 1. Buscar processos apenas do utilizador logado
    processos = Process.objects.filter(user=request.user).order_by('-submission_date')
    
    # 2. Lógica da Pesquisa (Search Bar)
    query = request.GET.get('q')
    if query:
        # Pesquisa por Nome do Serviço OU por ID do processo
        processos = processos.filter(
            Q(service_type__name__icontains=query) | 
            Q(id__icontains=query)
        )

    # 3. Paginação (5 itens por página)
    paginator = Paginator(processos, 5)
    page = request.GET.get('page')
    processos_paginados = paginator.get_page(page)

    # 4. REGRA DE NEGÓCIO: Só pode criar novo se não tiver pendências ativas
    # (Consideramos pendência tudo o que não seja 'Rejeitado' ou 'Aprovado')
    # Assim evita-se spam de pedidos
    pode_criar_novo = not Process.objects.filter(user=request.user).exclude(status__in=['rejected', 'approved']).exists()

    context = {
        'processos': processos_paginados,
        'pode_criar_novo': pode_criar_novo
    }
    return render(request, 'dashboard.html', context)

@login_required
def edit_profile(request):
    """
    Edição de Perfil (Dados de Login + Dados Pessoais).
    """
    # Garante que o perfil existe (caso tenha sido apagado manualmente na BD)
    Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, '✅ O teu perfil foi atualizado com sucesso!')
            return redirect('dashboard')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'edit_profile.html', context)

# ==============================================================================
# 3. GESTÃO DO PROCESSO (CRIAR, DETALHES, UPLOADS, SUBMETER)
# ==============================================================================

@login_required
def create_process(request):
    """
    Inicia um novo pedido.
    """
    # Verifica novamente se já tem processos pendentes (segurança extra backend)
    tem_pendencia = Process.objects.filter(user=request.user).exclude(status__in=['rejected', 'approved']).exists()
    
    if tem_pendencia:
        messages.warning(request, '⚠️ Já tens um processo em aberto. Finaliza-o antes de criar outro.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = ProcessForm(request.POST)
        if form.is_valid():
            process = form.save(commit=False)
            process.user = request.user
            process.status = 'draft' # Força estado inicial
            process.save()
            
            messages.success(request, 'Pedido iniciado! Agora carrega os documentos necessários.')
            return redirect('process_detail', process_id=process.id)
    else:
        form = ProcessForm()

    return render(request, 'create_process.html', {'form': form})

@login_required
def process_detail(request, process_id):
    """
    Página principal do processo.
    """
    process = get_object_or_404(Process, id=process_id, user=request.user)
    
    # 1. Quais documentos este tipo de visto exige?
    required_docs = RequiredDoc.objects.filter(service_type=process.service_type)
    
    # 2. Montar a lista inteligente (Status + Ficheiro se existir)
    documents_status = []
    
    for doc_type in required_docs:
        # Tenta encontrar o ficheiro já enviado para este requisito
        attachment = Attachment.objects.filter(process=process, required_doc=doc_type).first()
        
        documents_status.append({
            'doc_type': doc_type, 
            'attachment': attachment
        })

    context = {
        'process': process,
        'documents_status': documents_status,
    }
    return render(request, 'process_detail.html', context)

@login_required
def upload_document(request, process_id):
    """
    Upload de ficheiros para o processo.
    """
    process = get_object_or_404(Process, id=process_id, user=request.user)
    
    if process.status != 'draft':
        messages.error(request, '⛔ Este processo já foi submetido. Não podes alterar documentos.')
        return redirect('process_detail', process_id=process.id)

    if request.method == 'POST':
        doc_type_id = request.POST.get('doc_type_id')
        file = request.FILES.get('file')

        if doc_type_id and file:
            doc_type = get_object_or_404(RequiredDoc, id=doc_type_id)
            
            # Remove ficheiro antigo se existir (para poupar espaço)
            Attachment.objects.filter(process=process, required_doc=doc_type).delete()
            
            # Cria o novo registo
            Attachment.objects.create(
                process=process,
                required_doc=doc_type,
                file=file
            )
            messages.success(request, '📄 Documento carregado com sucesso!')
        else:
            messages.error(request, '❌ Erro ao carregar documento.')
            
    return redirect('process_detail', process_id=process_id)

@login_required
def delete_document(request, doc_id):
    """
    Remove um documento específico.
    """
    attachment = get_object_or_404(Attachment, id=doc_id)
    
    # SEGURANÇA: Garante que o documento pertence ao utilizador logado
    if attachment.process.user != request.user:
        messages.error(request, '⛔ Acesso negado.')
        return redirect('dashboard')

    if attachment.process.status == 'draft':
        process_id = attachment.process.id
        attachment.delete()
        messages.success(request, '🗑️ Documento removido.')
        return redirect('process_detail', process_id=process_id)
    else:
        messages.error(request, '⛔ Não pode remover documentos de um processo submetido.')
        return redirect('dashboard')

@login_required
def submit_process_final(request, process_id):
    """
    AÇÃO FINAL: Transforma o Rascunho em Processo Submetido.
    """
    process = get_object_or_404(Process, id=process_id, user=request.user)
    
    if process.status == 'draft':
        # Validação: Verifica se TODOS os documentos obrigatórios foram enviados
        required_count = RequiredDoc.objects.filter(service_type=process.service_type, is_mandatory=True).count()
        uploaded_count = Attachment.objects.filter(process=process, required_doc__is_mandatory=True).count()

        if uploaded_count < required_count:
            messages.error(request, '⚠️ Faltam documentos obrigatórios! Por favor carregue todos antes de submeter.')
            return redirect('process_detail', process_id=process.id)

        process.status = 'submitted'
        process.submission_date = timezone.now() # Regista a data real do envio
        process.save()
        messages.success(request, '🎉 Processo submetido com sucesso! Aguarde a análise da AIMA.')
    
    return redirect('dashboard')

@login_required
def cancel_process(request, process_id):
    """
    Cancela e apaga um processo em Rascunho.
    """
    process = get_object_or_404(Process, id=process_id, user=request.user)
    
    if process.status == 'draft':
        process.delete()
        messages.success(request, '🗑️ O pedido foi cancelado e removido com sucesso.')
    else:
        messages.error(request, '⛔ Não é possível cancelar um processo que já foi submetido.')
    
    return redirect('dashboard')

# ==============================================================================
# 4. AGENDAMENTOS & PDF (FUNCIONALIDADES AVANÇADAS)
# ==============================================================================

@login_required
def generate_appointment(request, process_id):
    """
    Gera um agendamento automático para processos Aprovados.
    """
    process = get_object_or_404(Process, id=process_id, user=request.user)
    
    if process.status != 'approved':
        messages.error(request, '❌ Este processo ainda não foi aprovado.')
        return redirect('dashboard')
    
    # Verifica se já existe agendamento (evita duplicados)
    if hasattr(process, 'appointment'):
        messages.warning(request, '⚠️ Já tens um agendamento para este processo.')
        return redirect('dashboard')

    # Lógica de Agendamento (Simulação)
    nova_senha = f"AIMA-{random.randint(1000, 9999)}"
    data_estimada = timezone.now() + timezone.timedelta(days=random.randint(10, 30))

    Appointment.objects.create(
        process=process,
        appointment_date=data_estimada,
        ticket_number=nova_senha,
        location="Loja AIMA Lisboa - Campus de Justiça"
    )
    
    messages.success(request, f'📅 Agendamento confirmado! Senha: {nova_senha}.')
    return redirect('dashboard')

@login_required
def generate_pdf(request, appointment_id):
    """
    Gera um ficheiro PDF oficial com os dados do agendamento.
    """
    # Busca o agendamento através do ID, mas garante que o processo associado é do user logado
    # Isto previne que alguém tente sacar PDFs de outras pessoas mudando o ID na URL
    appointment = get_object_or_404(Appointment, id=appointment_id, process__user=request.user)
    
    template_path = 'ticket_pdf.html'
    context = {'appointment': appointment}
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Senha_{appointment.ticket_number}.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF: ' + html)
        
    return response

# ==============================================================================
# 5. ÁREA DE GESTÃO (BACKOFFICE)
# ==============================================================================

def is_manager(user):
    """Verifica se o utilizador é membro da equipa (Staff)."""
    return user.is_staff

@login_required
@user_passes_test(is_manager)
def manager_dashboard(request):
    """
    Dashboard exclusivo para gestores (Staff).
    """
    total_processos = Process.objects.count()
    
    labels = []
    data = []
    
    # Agrupa processos por estado para o gráfico
    queryset = Process.objects.values('status').annotate(total=Count('status'))
    
    # Mapa para traduzir códigos para texto legível
    status_map = dict(Process.STATUS_CHOICES)
    
    for entry in queryset:
        status_code = entry['status']
        status_name = status_map.get(status_code, status_code) # Tenta traduzir
        
        labels.append(status_name)
        data.append(entry['total'])
    
    return render(request, 'manager_dashboard.html', {
        'labels': labels, 
        'data': data,
        'total_processos': total_processos
    })