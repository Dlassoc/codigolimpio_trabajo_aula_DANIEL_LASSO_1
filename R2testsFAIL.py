"""import unittest
from payment_plan import PaymentPlan, PurchaseAmountError, NumInstallmentsError, CardNotFoundError
from credit_card_module import CreditCard
class TestPaymentPlan(unittest.TestCase):
     
    def test_calculate_installment_interest_bancolombia(self):
        # Caso normal para Bancolombia 556677
        payment_plan = PaymentPlan(
            card_number="Bancolombia 556677",
            purchase_date="2023-08-04",
            purchase_amount=200000,
            payment_date=None,
            payment_amount=None,
            interest_amount=None,
            capital_amount=None,
            balance=200000,
            )

        monthly_installment, total_interest = payment_plan.calculate_installment_interest(annual_interest_rate=37, num_installments=36)

        # Redondear los valores a la cantidad de decimales necesarios
        monthly_installment = round(monthly_installment, 4)
        total_interest = round(total_interest, 2)

        self.assertAlmostEqual(monthly_installment, 9275.0216, places=4)
        self.assertAlmostEqual(total_interest, 133900.78, places=2)

    def test_calculate_installment_interest_falabella(self):
        # Crear una tarjeta en la base de datos antes de ejecutar la prueba
            self.test_insert_card(
                card=CreditCard(
                    card_number="Falabella 223344",
                    owner_id="123456789",
                    owner_name="Juan Perez",
                    bank_name="Falabella",
                    due_date="31/12/2025",
                    franchise="VISA",
                    payment_day=10,
                    monthly_fee=10000,
                    interest_rate=3.0
                )
            )

            # Caso normal para Falabella 223344
            payment_plan = PaymentPlan(
                card_number="Falabella 223344",
                purchase_date="2023-08-04",
                purchase_amount=850000,
                payment_date=None,
                payment_amount=None,
                interest_amount=None,
                capital_amount=None,
                balance=850000,  # Actualización del balance
            )

            monthly_installment, total_interest = payment_plan.calculate_installment_interest(annual_interest_rate=40, num_installments=24)

            # Redondear los valores a la cantidad de decimales necesarios
            monthly_installment = round(monthly_installment, 4)
            total_interest = round(total_interest, 2)

            self.assertAlmostEqual(monthly_installment, 52009.5752, places=4)
            self.assertAlmostEqual(total_interest, 398229.8, places=2)


    def test_calculate_installment_interest_zero_interest(self):
        # Caso con tasa de interés cero
        payment_plan = PaymentPlan(
            card_number="BBVA 445566",
            purchase_date="2023-08-04",
            purchase_amount=480000,
            payment_date=None,
            payment_amount=None,
            interest_amount=None,
            capital_amount=None,
            balance=480000,  # Actualización del balance
        )

        monthly_installment, total_interest = payment_plan.calculate_installment_interest(annual_interest_rate=0, num_installments=48)

        # Redondear los valores a la cantidad de decimales necesarios
        monthly_installment = round(monthly_installment, 4)
        total_interest = round(total_interest, 2)
        "print(monthly_installment)"
        self.assertAlmostEqual(monthly_installment, 10000.0, places=4)
        self.assertAlmostEqual(total_interest, 0.0, places=2)

    def test_calculate_installment_interest_single_payment(self):
        # Caso Cuota única
        payment_plan = PaymentPlan(
            card_number="BBVA 445566",
            purchase_date="2023-08-04",
            purchase_amount=90000,
            payment_date=None,
            payment_amount=None,
            interest_amount=None,
            capital_amount=None,
            balance=90000,  # El saldo coincide con el monto de compra en este caso
        )

        monthly_installment, total_interest = payment_plan.calculate_installment_interest(annual_interest_rate=0, num_installments=1)

        # Verificar que la cuota única sea igual al monto de compra y el interés total sea cero
        self.assertAlmostEqual(monthly_installment, 90000, places=2)
        self.assertAlmostEqual(total_interest, 0, places=2)

    def test_purchase_amount_error(self):
        # Caso de error en el monto de compra
        with self.assertRaises(PurchaseAmountError) as context:
            payment_plan = PaymentPlan(
                card_number="Falabella 223344",
                purchase_date="2023-08-04",
                purchase_amount=0,  # Monto igual a cero, debería lanzar la excepción
                payment_date=None,
                payment_amount=None,
                interest_amount=None,
                capital_amount=None,
                balance=200000,
            )

        # Verificar que el mensaje de la excepción sea igual al mensaje esperado
        expected_message = "Error: el monto de compra debe ser superior a cero"
        self.assertEqual(str(context.exception), expected_message)


    def test_negative_num_installments_error(self):
        # Caso de error en el número de cuotas (negativo)
        with self.assertRaises(NumInstallmentsError) as context:
            payment_plan = PaymentPlan(
                card_number="Bancolombia 556677",
                purchase_date="2023-08-04",
                purchase_amount=50000,
                payment_date=None,
                payment_amount=None,
                interest_amount=None,
                capital_amount=None,
                balance=50000,
            )
            # Establecer el número de cuotas como un valor negativo
            payment_plan.calculate_installment_interest(annual_interest_rate=10, num_installments=-10)

        # Verificar que el mensaje de la excepción sea igual al mensaje esperado
        expected_message = "Error: el número de cuotas debe ser mayor a cero"
        self.assertEqual(str(context.exception), expected_message)

    def test_card_not_found_error(self):
            # Caso de error cuando la tarjeta no existe
            with self.assertRaises(CardNotFoundError) as context:
                payment_plan = PaymentPlan(
                    card_number="885522",  # Número de tarjeta que no existe
                    purchase_date="2023-08-04",
                    purchase_amount=50000,
                    payment_date=None,
                    payment_amount=None,
                    interest_amount=None,
                    capital_amount=None,
                    balance=0,  # Saldo cero porque la tarjeta no existe
                )
                # Establecer el número de cuotas
                payment_plan.calculate_installment_interest(annual_interest_rate=10, num_installments=10)

            # Verificar que el mensaje de la excepción sea igual al mensaje esperado
            expected_message = "Error: La tarjeta indicada no existe"
            self.assertEqual(str(context.exception), expected_message)
if __name__ == "__main__":
    unittest.main()
"""