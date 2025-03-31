import unittest
from time import sleep

class TestExemplo(unittest.TestCase):
    
    def setUp(self):
        print("🛠️ Configurando ambiente para o teste")

    def test_um(self):
        sleep(5)
        print("✅ Teste um executado")
        
    def test_dois(self):
        sleep(6)
        print("✅ Teste dois executado")
        
    def test_tres(self):
        sleep(7)
        print("✅ Teste três executado")
        
    def tearDown(self):
        print("🔄 Limpando ambiente após o teste")

if __name__ == "__main__":
    unittest.main()
    
# Vale notar a diferença de tempo de execução entre os testes.
# python3 -m pytest main.py --html=main.html
# python3 -m pytest main.py -n auto --html=main.html