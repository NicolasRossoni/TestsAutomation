# Automação de Testes para Plataforma

Testes automatizados para a plataforma usando Selenium e Page Object Model.

## Tecnologias
- Python, Selenium, unittest/pytest
- Page Object Model para estruturação dos testes
- Logging para registro de execução

## Estrutura do Projeto

### `src/`
- **NavegacaoWeb.py**: Testes de navegação entre áreas da plataforma
- **Assinaturas.py**: Testes de criação de assinaturas

### `src/core/`
- **auxiliar.py**: Funções auxiliares para interação com elementos e tratamento de exceções
- **Pages/**: Implementação do Page Object Model (Como um pacote python)
  - **\_\_init\_\_.py**: Centraliza importações das classes de páginas
  - **Web/**: Páginas ao Web
    - **Login.py**: Página de login
    - **Web.py**: Navegação na página principal
  - **Backoffice/**: Páginas relacionadas ao backoffice
    - **Backoffice.py**: Navegação na área do backoffice
    - **CriarAssinatura.py**: Gerencia fluxo de criação de assinaturas

## Execução
```bash
# Executar testes gerando relatorio
pytest src/<TestSuit_Name>.py --html=src/core/report.html

# Execução em paralelo
pytest src/<TestSuit_Name>.py -n auto --html=src/core/report.html
```

## Instalação de dependencias
```bash
pip install -r requirements.txt
```