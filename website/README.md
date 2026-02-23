# 🌍 ImigraÁgil - Gestão AIMA Simplificada

**ImigraÁgil** é um portal web desenvolvido em Django para simplificar e digitalizar o processo de renovação de autorizações de residência e agendamentos com a AIMA (Agência para a Integração, Migrações e Asilo).

## Funcionalidades Principais

Portal do Imigrante: Registo seguro e login de utilizadores.
Gestão de Processos: Submissão digital de pedidos de vistos/renovações com upload seguro de documentos (Passaportes, Registo Criminal, etc.).
Dashboard Inteligente: Acompanhamento em tempo real do estado do processo (Rascunho, Em Análise, Aprovado, Rejeitado).
Agendamentos: Geração automática de senhas para recolha presencial após aprovação do processo.
Geração de PDF: Exportação do comprovativo oficial de agendamento em PDF.
Backoffice (Admin): Painel de controlo executivo para os funcionários da AIMA gerirem os processos e visualizarem estatísticas do sistema.

## Tecnologias Utilizadas

Backend: Python 3, Django 6
Frontend: HTML5, Bootstrap 5 (CSS/JS), Bootstrap Icons
Base de Dados: SQLite (Desenvolvimento)
Geração de PDF: `xhtml2pdf`

## Como correr o projeto localmente

Siga os passos abaixo para testar o projeto no seu computador:

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/SEU-USERNAME/imigraagil.git](https://github.com/SEU-USERNAME/imigraagil.git)
   cd imigraagil

2. Crie e ative o ambiente virtual:

    python -m venv .venv
    # No Windows:
    .venv\Scripts\activate
    # No Mac/Linux:
    source .venv/bin/activate

3. Instale as dependências:

    Bash
    pip install -r requirements.txt

4. Aplique as migrações da base de dados:

    python manage.py migrate

5. Crie um superutilizador (para aceder ao backoffice):

    python manage.py createsuperuser

6. Inicie o servidor local:

    python manage.py runserver

7. Aceda no navegador:

Portal Público: http://127.0.0.1:8000/

Backoffice AIMA: http://127.0.0.1:8000/admin/

Desenvolvido como projeto de gestão documental e imigração digital.

