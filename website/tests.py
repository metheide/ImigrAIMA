from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import ServiceType

class ImigraAgilTests(TestCase):
    
    def setUp(self):
        # Cria um utilizador de teste
        self.user = User.objects.create_user(username='testuser', password='password123')
        # Cria um tipo de serviço
        self.service = ServiceType.objects.create(name='Visto Teste', description='Teste')

    def test_homepage_loads(self):
        """Verifica se a página inicial abre (Código 200)"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_loads(self):
        """Verifica se a página de login existe"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)