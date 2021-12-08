import unittest
from Planner import Planner

class TestManejarEntrada(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.file= "C:\\Users\\mcabr\\Desktop\\PT\\block-port\\AIDS\\Planner\\test.csv"
        self.p = Planner(self.file)

    #Prueba para probar la correcta asignación de medida en base al tipo de ataque
    def test_classify(self):
        self.assertAlmostEqual(self.p.classify(1,"Backdoor"), "ClosePort")
        self.assertAlmostEqual(self.p.classify(1,"DoS"), "BlockIP")
        self.assertAlmostEqual(self.p.classify(1,"Exploits"), "ClosePort")

    #prueba para probar la obtención de datos desde archivo
    def test_getFileInfo(self):
        self.assertAlmostEqual(self.p.getFileInfo(), "")



if __name__ == '__main__':
    unittest.main()