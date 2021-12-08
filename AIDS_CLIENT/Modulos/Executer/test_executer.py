import unittest
from Executer import Executer

class TestManejarEntrada(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.comando = ["ScanPort 443 www.google.com", "String invalido"]
        self.r = Executer()
        self.r.setEntrada(self.comando[0])

    #Prueba para probar el funcionamientode los get y set
    def test_set_entrada(self):
        self.r.setEntrada("TEST")
        self.assertAlmostEqual(self.r.getEntrada(),str("TEST"))

    #Prueba para verificar que solo se ejecuten las funciones con el formato correcto
    def test_manejar_entrada(self):
        self.r.setEntrada(self.comando[0])
        self.assertAlmostEqual(self.r.manageEntry(),"[['ScanPort', '443', 'www.google.com']]")
        self.r.setEntrada(self.comando[1])
        self.assertAlmostEqual(self.r.manageEntry(), "Formato de entrada incorrecto")

    #Prueba para verificar el funcionamineto de getFlag
    def test_get_flag(self):
        self.assertAlmostEqual(self.r.getFlag("ClosePort"), "-c")
        self.assertAlmostEqual(self.r.getFlag("Texto no valido"),"error")
        self.assertAlmostEqual(self.r.getFlag("openport"),"error")
        self.assertAlmostEqual(self.r.getFlag("BlockIp"),"-B")

    #Prueba para verificar el correcto funcionamiento de decode
    def test_decode(self):
        self.assertAlmostEqual(self.r.decode("https,ClosePort.BlockIP"), str("ClosePort 443;BlockIP 443;"))
        self.assertAlmostEqual(self.r.decode("500,ClosePort.BlockIP;200,CUARENTENA;1000,BlockIP"), str("ClosePort 500;BlockIP 500;CUARENTENA 200;BlockIP 1000;"))


if __name__ == '__main__':
    unittest.main()