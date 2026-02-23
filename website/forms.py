from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Process, Profile

# ==============================================================================
# 1. INICIAR NOVO PROCESSO
# ==============================================================================

class ProcessForm(forms.ModelForm):
    """
    Formulário simples para iniciar um processo.
    Apenas pede o tipo de serviço; o resto é preenchido depois.
    """
    class Meta:
        model = Process
        fields = ['service_type']
        labels = {
            'service_type': 'Qual o tipo de Visto ou Serviço?',
        }
        # Widgets para aplicar estilo específico (Select Menu)
        widgets = {
            'service_type': forms.Select(attrs={'class': 'form-select form-select-lg'}),
        }


# ==============================================================================
# 2. REGISTO DE NOVA CONTA (SIGN UP)
# ==============================================================================

class CustomUserCreationForm(UserCreationForm):
    """
    Estende o formulário padrão do Django para pedir Nome e Email logo no registo.
    """
    first_name = forms.CharField(max_length=30, required=True, label="Primeiro Nome")
    last_name = forms.CharField(max_length=30, required=True, label="Último Nome")
    email = forms.EmailField(required=True, label="Endereço de Email")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # Loop Mágico: Aplica estilo Bootstrap a TODOS os campos deste form
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


# ==============================================================================
# 3. EDITAR DADOS DE LOGIN (User)
# ==============================================================================

class UserUpdateForm(forms.ModelForm):
    """
    Permite alterar nome e email (mas não a password ou username aqui).
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


# ==============================================================================
# 4. EDITAR PERFIL DE IMIGRANTE (Profile)
# ==============================================================================

class ProfileUpdateForm(forms.ModelForm):
    """
    Formulário para os dados específicos de imigração.
    Agora inclui 'nationality' que estava em falta.
    """
    class Meta:
        model = Profile
        # Campos alinhados com o novo models.py
        fields = ['passport', 'nif', 'nationality', 'phone', 'address']
        
        labels = {
            'passport': 'Número de Passaporte',
            'nif': 'NIF (Número de Contribuinte)',
            'nationality': 'Nacionalidade',
            'phone': 'Contacto Telefónico',
            'address': 'Morada Completa em Portugal'
        }
        
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        # Aplica estilo Bootstrap a todos os campos
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})