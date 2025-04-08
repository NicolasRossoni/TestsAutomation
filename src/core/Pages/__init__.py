"""
Classes de Page Object Model para interação com a interface.

Coloque as paginas que serão utilizadas nos testes nesse arquivo. Para depois só importar a pasta Pages.
exemplo:
import Pages
"""

# Importando classes da Web
from core.Pages.Web.Login import Login
from core.Pages.Web.Web import Web

# Importando classes do Backoffice
from core.Pages.Backoffice.Backoffice import Backoffice
from core.Pages.Backoffice.CriarAssinatura import CriarAssinatura 