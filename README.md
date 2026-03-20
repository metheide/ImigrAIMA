# ImigraÁgil - Gestão AIMA Simplificada 🇵🇹

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap_5-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

> Um portal web desenvolvido para simplificar e digitalizar o processo de renovação de autorizações de residência e agendamentos com a AIMA (Agência para a Integração, Migrações e Asilo).



<img width="1330" height="1496" alt="127 0 0 1_8000_ (1)" src="https://github.com/user-attachments/assets/40b66ac0-f810-4d31-9376-fe0b333a7569" />



##  Funcionalidades Principais

* **Portal do Imigrante:** Registo seguro e login de utilizadores.
* **Gestão de Processos:** Submissão digital de pedidos de vistos/renovações com upload seguro de documentos (Passaportes, Registo Criminal, etc.).
* **Dashboard Inteligente:** Acompanhamento em tempo real do estado do processo (Rascunho, Em Análise, Aprovado, Rejeitado).
* **Agendamentos:** Geração automática de senhas para recolha presencial após aprovação do processo.
* **Geração de PDF:** Exportação do comprovativo oficial de agendamento em PDF utilizando a biblioteca `xhtml2pdf`.
* **Backoffice (Admin):** Painel de controlo executivo para os funcionários da AIMA gerirem os processos e visualizarem estatísticas do sistema.

##  Tecnologias Utilizadas

* **Backend:** Python 3, Django (Framework MVT)
* **Frontend:** HTML5, CSS3, Bootstrap 5, Bootstrap Icons
* **Base de Dados:** SQLite (Ambiente de Desenvolvimento)
* **Bibliotecas Extra:** `xhtml2pdf` (para relatórios)

##  Como correr o projeto localmente

Siga os passos abaixo para testar o projeto no seu computador:

1. **Clone o repositório:**
    ```bash
    git clone https://github.com/SEU-USERNAME/imigraagil.git
    cd imigraagil
    ```

2. **Crie e ative o ambiente virtual:**
    ```bash
    python -m venv .venv
    
    # No Windows:
    .venv\Scripts\activate
    
    # No Mac/Linux:
    source .venv/bin/activate
    ```

3. **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Aplique as migrações da base de dados:**
    ```bash
    python manage.py migrate
    ```

5. **Crie um superutilizador (para aceder ao backoffice):**
    ```bash
    python manage.py createsuperuser
    ```

6. **Inicie o servidor local:**
    ```bash
    python manage.py runserver
    ```

7. **Aceda no navegador:**
    * **Portal Público:** `http://127.0.0.1:8000/`
    * **Backoffice AIMA:** `http://127.0.0.1:8000/admin/`

---

##  Sobre o Autor

Desenvolvido por **Matheus Rodrigues** como projeto de conclusão de curso (IEFP) focado em gestão documental e transição digital. 

Se procuras um Junior Software Engineer motivado e com foco em resolver problemas reais, entra em contacto:
* **LinkedIn:** https://www.linkedin.com/in/methege/
* **Email:** methegebaf@gmail.com
