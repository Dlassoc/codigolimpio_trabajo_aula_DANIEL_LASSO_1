import unittest
from payment_plan_t4 import PaymentPlan

class TestPaymentPlan(unittest.TestCase):
    def test_case_1(self):
        # Datos de prueba
        card_number = "556677 Bancolombia"
        purchase_date = "22-Sep"
        purchase_amount = 200000
        annual_interest_rate = 37
        num_installments = 36
        payment_due_date = 10

        # Crear un objeto PaymentPlan
        # Crear un objeto PaymentPlan
        payment_plan = PaymentPlan(
            card_number=card_number,
            purchase_date=purchase_date,
            purchase_amount=purchase_amount,
            payment_date=None,  # Valor ficticio para payment_date
            payment_amount=None,  # Valor ficticio para payment_amount
            interest_amount=None,  # Valor ficticio para interest_amount
            capital_amount=None,  # Valor ficticio para capital_amount
            balance=None  # Valor ficticio para balance
        )


        # Calcular el plan de amortización
        amortization_schedule = payment_plan.calculate_amortization_schedule(
            annual_interest_rate=annual_interest_rate,
            num_installments=num_installments,
            card_number=card_number,
            payment_due_date=payment_due_date
        )

        # Verificar que la longitud del plan de amortización sea igual a num_installments
        self.assertEqual(len(amortization_schedule), num_installments)

        # Verificar que la identidad de la tarjeta y la fecha de pago estén en cada fila del plan de amortización
        for payment_info in amortization_schedule:
            self.assertIn(card_number, payment_info)
            # Asegúrate de que la fecha de pago sea igual al valor esperado
            self.assertEqual(payment_due_date, int(payment_info[-1].split('/')[0]))




    """def test_case_2(self):
        # Datos de prueba
        card_number = "223344 Falabella"
        purchase_date = "25-Sep"
        purchase_amount = 850000
        annual_interest_rate = 3.40
        num_installments = 24
        payment_due_date = 16

        # Crear un objeto PaymentPlan
        payment_plan = PaymentPlan(
            card_number=card_number,
            purchase_date=purchase_date,
            purchase_amount=purchase_amount,
            payment_date=None,  # Valor ficticio para payment_date
            payment_amount=None,  # Valor ficticio para payment_amount
            interest_amount=None,  # Valor ficticio para interest_amount
            capital_amount=None,  # Valor ficticio para capital_amount
            balance=None  # Valor ficticio para balance
        )

        # Calcular el plan de amortización
        amortization_schedule = payment_plan.calculate_amortization_schedule(
            annual_interest_rate=annual_interest_rate,
            num_installments=num_installments,
            payment_due_date=payment_due_date
        )

        # Verificar que la longitud del plan de amortización sea igual a num_installments
        self.assertEqual(len(amortization_schedule), num_installments)"""

if __name__ == "__main__":
    unittest.main()
