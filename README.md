# Fluxo de Assinatura - Automação de Testes

## Visão Geral
Este projeto implementa testes automatizados para o fluxo de criação de assinaturas na plataforma EcoTX, utilizando Selenium WebDriver e seguindo o padrão Page Object Model (POM).

## Tecnologias Utilizadas
- **Python**: Linguagem de programação principal
- **Selenium WebDriver**: Framework para automação de navegadores
- **Selenium Wire**: Extensão do Selenium para monitorar requisições HTTP
- **unittest**: Framework de testes unitários do Python
- **pytest**: Framework de testes com recursos adicionais e geração de relatórios

## Estrutura do Projeto

### auxiliar.py
Fornece funções auxiliares para os testes de automação, encapsulando operações comuns do Selenium WebDriver e configurações de logging:
- Funções de interação com elementos da interface
- Configuração do sistema de logging
- Tratamento de exceções e timeouts

### Pages.py
Implementa o padrão Page Object Model para automação da plataforma, definindo classes que representam cada uma das páginas e componentes da interface:
- **LoginPage**: Manipula a página de login e autenticação
- **MainWebPage**: Manipula a navegação da página principal (troca de organização, área)
- **Backoffice**: Manipula a página de backoffice e navegação entre suas áreas
- **BackofficeCriarAssinatura**: Manipula o formulário de criação de assinaturas

### TestSuit.py
Implementa testes automatizados para o fluxo de criação de assinaturas na plataforma:
- **TestLogin**: Classe de teste que herda de unittest.TestCase
- Métodos para configuração do ambiente, execução dos testes e limpeza
- Verificação de requisições HTTP para confirmar o sucesso da criação de assinaturas
- Suporte a diferentes tipos de assinatura e configurações

## Como Executar os Testes
Para executar os testes e gerar um relatório HTML:

```bash
pytest TestSuit.py --html=TestSuit_report.html
```


### Execução em Paralelo
Para executar os testes em paralelo, utilize o pytest-xdist:

```bash
pytest TestSuit.py -n auto --html=TestSuit_report.html
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