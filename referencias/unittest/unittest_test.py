import unittest

class TestExemplo(unittest.TestCase):
    
    def setUp(self):
        print("🛠️ Configurando ambiente para o teste")

    def test_um(self):
        print(2/ 0)

    def test_dois(self):
        print("✅ Executando test_dois")

    def tearDown(self):
        print("🔄 Limpando ambiente após o teste")

if __name__ == "__main__":
    unittest.main() 
# Para gerar relatorio
# pytest code_ref/unittest/unittest_test.py --html=code_ref/unittest/report_unittest_test.html