import unittest
from payment_plans import payment_test_r3

class TestSavingsPlan(unittest.TestCase):
    def test_savings_plan(self):
        # Caso Normal
        sp = payment_test_r3.SavingsPlan('1234567890123456', 200000, 28)
        for _ in range(28):  # Simular 28 meses de ahorro
            sp.save()
        self.assertAlmostEqual(sp.get_balance(), 200000, places=2)

    def test_savings_plan_2(self):
        # Caso Normal 2
        sp = payment_test_r3.SavingsPlan('1234567890123456', 850000, 20)
        for _ in range(20):  # Simular 20 meses de ahorro
            sp.save()
        self.assertAlmostEqual(sp.get_balance(), 850000, places=2)

    def test_savings_plan_3(self):
        # Tasa cero
        sp = payment_test_r3.SavingsPlan('1234567890123456', 480000, 41)
        for _ in range(41):  # Simular 41 meses de ahorro
            sp.save()
        self.assertAlmostEqual(sp.get_balance(), 480000, places=2)

    def test_savings_plan_4(self):
        # Caso Normal
        sp = payment_test_r3.SavingsPlan('1234567890123456', 90000, 1)  # Cuota única, 1 mes de ahorro
        sp.save()  # Simular 1 mes de ahorro
        self.assertAlmostEqual(sp.get_balance(), 90810, places=2)  # Verificar el saldo después de 1 mes

    

if __name__ == '__main__':
    unittest.main()
