# Automação de Testes para Plataforma

## Visão Geral
Este projeto implementa testes automatizados para diversos fluxos na plataforma, utilizando Selenium WebDriver e seguindo o padrão Page Object Model (POM).

## Tecnologias Utilizadas
- **Python**: Linguagem de programação principal
- **Selenium**: Framework para automação de navegadores web
- **POM (Page Object Model)**: Padrão de design que separa a lógica de teste da lógica de interação com a página
- **unittest**: Framework de testes unitários do Python
- **pytest**: Framework de testes com recursos adicionais e geração de relatórios
- **logging**: Módulo para registro de logs estruturados durante a execução dos testes

## Estrutura do Projeto

### Diretório `core/`

#### auxiliar.py
Fornece funções auxiliares para os testes de automação:
- Funções de interação com elementos da interface
- Função de verificação de chamadas API
- Configuração do sistema de logging em console
- Tratamento de exceções e timeouts

#### Pages.py
Implementa o padrão Page Object Model para automação da plataforma:
- **LoginPage**: Manipula a página de login e autenticação
- **MainWebPage**: Manipula a navegação da página principal (troca de organização, área)
- **Backoffice**: Manipula a página de backoffice e navegação entre suas áreas
- **BackofficeCriarAssinatura**: Manipula o formulário de criação de assinaturas

### Testes Implementados

#### NavegacaoWeb.py
Implementa testes para verificar a navegação entre diferentes áreas da plataforma:
- Teste de navegação para a área de mapas
- Teste de navegação para o backoffice
- Teste de navegação para workspaces
- Teste de navegação para dashboards

#### Assinaturas.py
Implementa testes para o fluxo de criação de assinaturas para usuarios existentes:
- Criação de assinaturas do tipo Venda+, Standard e Professional
- Suporte a configurações com e sem integração Asaas

## Como Executar os Testes
Para executar os testes e gerar um relatório HTML:

```bash
# Para testes de navegação
pytest NavegacaoWeb.py --html=core/TestSuit_report.html

# Para testes de assinaturas
pytest Assinaturas.py --html=core/TestSuit_report.html
```

### Execução em Paralelo
Para executar os testes em paralelo, utilize o pytest-xdist:

```bash
pytest <file_name>.py -n auto --html=core/TestSuit_report.html
```

## Instalação de Dependências
Para instalar todas as dependências necessárias, execute o seguinte comando no terminal:

```bash
pip install -r requirements.txt
```

Este comando instalará todas as bibliotecas Python listadas no arquivo requirements.txt, incluindo:
- selenium
- selenium-wire
- pytest
- pytest-html
- pytest-xdist
- webdriver-manager
- blinker
