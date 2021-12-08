import unittest
import Analyzer

class TestAnalyzer(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.a = Analyzer.Analyzer()
    
    #prueba para probar el funcionamineto de __analizarVentana
    def test_analizar_ventana(self):
        #Testeando por día
        self.a.setToleranciaTiempo("DoS", (3, "D"))
        self.assertAlmostEqual(self.a.analizarVentana("30/10/2020", "3/11/2020", "DoS"), True)
        self.assertAlmostEqual(self.a.analizarVentana("1/10/2020", "2/10/2020", "DoS"), False)
        self.assertAlmostEqual(self.a.analizarVentana("1/10/2020", "10/10/2020", "DoS"), True)
        self.assertAlmostEqual(self.a.analizarVentana("31/8/2020", "2/9/2020", "DoS"), True)
        self.assertAlmostEqual(self.a.analizarVentana("29/2/2020", "1/3/2020", "DoS"), False)

        #Testendo por mes
        self.a.setToleranciaTiempo("Worms", (1, "M"))
        self.assertAlmostEqual(self.a.analizarVentana("10/10/2020", "10/12/2020", "Worms"), True)
        self.assertAlmostEqual(self.a.analizarVentana("30/8/2020", "6/9/2020", "Worms"), False)
        self.assertAlmostEqual(self.a.analizarVentana("3/2/2020", "1/3/2020", "Worms"), False)
        self.assertAlmostEqual(self.a.analizarVentana("20/8/2020", "20/9/2020", "Worms"), True)
        self.a.setToleranciaTiempo("Worms", (2, "M"))
        self.assertAlmostEqual(self.a.analizarVentana("20/3/2020", "13/5/2020", "Worms"), False)
        self.assertAlmostEqual(self.a.analizarVentana("20/3/2020", "21/5/2020", "Worms"), True)

        #Testeando por semana
        self.a.setToleranciaTiempo("Exploits", (1, "S"))
        self.assertAlmostEqual(self.a.analizarVentana("1/10/2020", "2/10/2020", "Exploits"), False)
        self.assertAlmostEqual(self.a.analizarVentana("1/10/2020", "8/10/2020", "Exploits"), True)
        self.assertAlmostEqual(self.a.analizarVentana("30/8/2020", "6/9/2020", "Exploits"), True)
        self.a.setToleranciaTiempo("Exploits", (4, "S"))
        self.assertAlmostEqual(self.a.analizarVentana("2/4/2020", "1/5/2020", "Exploits"), True)
        self.assertAlmostEqual(self.a.analizarVentana("1/1/2020", "20/1/2020", "Exploits"), False)
        self.a.setToleranciaTiempo("Exploits", (3, "S"))
        self.assertAlmostEqual(self.a.analizarVentana("1/1/2020", "22/1/2020", "Exploits"), True)

        #Testeando por año
        self.a.setToleranciaTiempo("Shellcode", (1, "A"))
        self.assertAlmostEqual(self.a.analizarVentana("10/10/2020", "10/ 9/2021", "Shellcode"), False)
        self.assertAlmostEqual(self.a.analizarVentana("30/10/2020", "20/10/2021", "Shellcode"), False)
        self.assertAlmostEqual(self.a.analizarVentana("10/10/2020", "10/11/2021", "Shellcode"), True)
    #prueba para probar algoritmo de detección de año biciesto
    def test_isBiciesto(self):
        self.assertAlmostEqual(self.a.isBiciesto(1992), True)
        self.assertAlmostEqual(self.a.isBiciesto(1996), True)
        self.assertAlmostEqual(self.a.isBiciesto(2002), False)
        self.assertAlmostEqual(self.a.isBiciesto(2006), False)
        self.assertAlmostEqual(self.a.isBiciesto(2012), True)
        self.assertAlmostEqual(self.a.isBiciesto(2016), True)
        self.assertAlmostEqual(self.a.isBiciesto(2018), False)
        self.assertAlmostEqual(self.a.isBiciesto(2024), True)
        self.assertAlmostEqual(self.a.isBiciesto(2039), False)
        self.assertAlmostEqual(self.a.isBiciesto(2035), False)



if __name__ == '__main__':
    unittest.main()