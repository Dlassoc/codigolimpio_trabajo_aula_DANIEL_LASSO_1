import unittest
from payment_plans import r5pyment_plan
import psycopg2
from database_info.database import HOST, DATABASE, USER, PASSWORD, PORT 


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

        # Crear un objeto PaymentPlan con los datos de prueba
        card_number = "556677 Bancolombia"
        purchase_date = "22-Sep"
        purchase_amount = 200000
        annual_interest_rate = 37
        num_installments = 36
        payment_due_date = 10

        self.payment_plan = r5pyment_plan.PaymentPlan(
            card_number=card_number,
            purchase_date=purchase_date,
            purchase_amount=purchase_amount,
            payment_date=None,  # Valor ficticio para payment_date
            payment_amount=None,  # Valor ficticio para payment_amount
            interest_amount=None,  # Valor ficticio para interest_amount
            capital_amount=None,  # Valor ficticio para capital_amount
            balance=None  # Valor ficticio para balance
        )

    def tearDown(self):
        # Cerrar el cursor si está abierto
        if self.cursor is not None:
            self.cursor.close()
        
        # Cerrar la conexión si está abierta
        if self.connection is not None:
            self.connection.close()
    def get_monthly_payments_in_range(self, start_date, end_date):
        # Conectarse a la base de datos y obtener los datos de cuotas mensuales en el rango de fechas
        connection = psycopg2.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            port=PORT
        )

        cursor = connection.cursor()

        # Consulta SQL para obtener las cuotas mensuales en el rango de fechas
        query = """
        SELECT month, card_number, due_date, cuota
        FROM amortization_schedule
        WHERE due_date >= %s AND due_date <= %s
        """

        cursor.execute(query, (start_date, end_date))
        monthly_payments = cursor.fetchall()

        # Cerrar la conexión a la base de datos
        cursor.close()
        connection.close()

        return monthly_payments

    def test_total_monthly_payments(self):
        # Especifica el rango de fechas para el informe
        start_date = "2023-10-01"
        end_date = "2023-10-31"

        # Obtiene los datos de cuotas mensuales para el rango de fechas
        monthly_payments = self.payment_plan.get_monthly_payments_in_range(start_date, end_date)

        # Calcula la suma total de cuotas mensuales
        total_cuota = sum(payment['cuota'] for payment in monthly_payments)

        # Valores esperados
        expected_total_cuota = 71675  

        # Verifica que la suma de las cuotas mensuales sea igual a los valores esperados
        self.assertEqual(total_cuota, expected_total_cuota)




if __name__ == "__main__":
    unittest.main()
