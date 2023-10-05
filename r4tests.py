import unittest
from payment_plan_t4 import PaymentPlan
import psycopg2
from database import HOST, DATABASE, USER, PASSWORD, PORT 
from datetime import datetime
from decimal import Decimal 
class TestPaymentPlan(unittest.TestCase):
    def setUp(self):
        # Establecer la conexión y el cursor antes de cada prueba
        self.connection = psycopg2.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            port=PORT
        )
        self.cursor = self.connection.cursor()

        # Limpiar los registros existentes en la tabla antes de cada prueba
        self.cursor.execute("DELETE FROM amortization_table")
        self.connection.commit()

    def tearDown(self):
        # Cerrar el cursor si está abierto
        if self.cursor is not None:
            self.cursor.close()
        
        # Cerrar la conexión si está abierta
        if self.connection is not None:
            self.connection.close()


    def test_case_1(self):

        # Datos de prueba
        card_number = "556677 Bancolombia"
        purchase_date = "22-Sep"
        purchase_amount = 200000
        annual_interest_rate = 37
        num_installments = 36
        payment_due_date = 10

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

    def test_case_2(self):


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
            card_number=card_number,
            payment_due_date=payment_due_date
        )

        # Verificar que la longitud del plan de amortización sea igual a num_installments
        self.assertEqual(len(amortization_schedule), num_installments)

    def test_case_3(self):


        # Datos de prueba
        card_number = "445566 BBVA"
        purchase_date = "29-Sep"
        purchase_amount = 480000
        annual_interest_rate = 0.0# Tasa de interés 0%
        num_installments = 48
        payment_due_date = 5

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

    def test_case_4(self):


        # Datos de prueba
        card_number = "445566 BBVA"
        purchase_date = "17-Nov"
        purchase_amount = 90000
        annual_interest_rate = 0.0  # Tasa de interés 0%
        num_installments = 1
        payment_due_date = 5

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


if __name__ == "__main__":
    unittest.main()
