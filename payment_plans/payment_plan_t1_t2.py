# payment_plan.py
import psycopg2
from exceptions import PurchaseAmountError, CardNotFoundError,  NumInstallmentsError
from database_info.database import HOST, DATABASE, USER, PASSWORD, PORT

class PaymentPlan:
    def __init__(self, card_number: str, purchase_date: str, purchase_amount: float, payment_date, payment_amount, interest_amount, capital_amount, balance):
        if purchase_amount <= 0:
            raise PurchaseAmountError(
                "Error: el monto de compra debe ser superior a cero")
        # Eliminar el nombre del banco y guardar solo los últimos 4 dígitos
        self.card_number = card_number[-4:]
        self.purchase_date = purchase_date
        self.purchase_amount = purchase_amount
        self.payment_date = payment_date
        self.payment_amount = payment_amount
        self.interest_amount = interest_amount
        self.capital_amount = capital_amount
        self.balance = balance
        self.amortization_plan = []

    def calculate_installment_interest(self, annual_interest_rate: float, num_installments: int):
        # Verificar si la tarjeta existe en la base de datos antes de calcular el interés
        connection = psycopg2.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            port=PORT
        )

        cursor = connection.cursor()

        # Antes de realizar la inserción, eliminar registros existentes con el mismo número de tarjeta
        cursor.execute(
            "DELETE FROM credit_card WHERE card_number = %s", (self.card_number,))
        connection.commit()  # Commit the transaction

        # Luego, realizar la inserción del nuevo registro
        cursor.execute(
            "INSERT INTO credit_card (card_number) VALUES (%s)", (self.card_number,))
        connection.commit()  # Commit the transaction

        # Verificar si la tarjeta existe en la base de datos
        cursor.execute(
            "SELECT COUNT(*) FROM credit_card WHERE card_number = %s", (self.card_number,))
        card_count = cursor.fetchone()[0]
        if card_count == 0:
            connection.close()
            raise CardNotFoundError("Error Tarjeta no Existe")
        # Continuar con el cálculo del interés aquí...

        if annual_interest_rate == 0:
            # Si la tasa de interés es cero, la cuota mensual es simplemente el monto de compra dividido por el número de cuotas
            monthly_installment = self.purchase_amount / num_installments
            total_interest = 0  # En este caso, el interés total es cero
        elif num_installments <= 0:
            raise NumInstallmentsError(
                "Error: el número de cuotas debe ser mayor a cero")
        else:
            monthly_interest_rate = annual_interest_rate / 12 / 100
            monthly_installment = (self.purchase_amount * monthly_interest_rate) / (
                1 - (1 + monthly_interest_rate) ** -num_installments)
            total_interest = (monthly_installment *
                              num_installments) - self.purchase_amount

        connection.close()

        return monthly_installment, total_interest

    def get_monthly_payments_in_range(self, start_date: str, end_date: str) :
        # Conéctate a la base de datos
        connection = psycopg2.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            port=PORT
        )

        try:
            # Crea un cursor para interactuar con la base de datos
            cursor = connection.cursor()

            # Define la consulta SQL para obtener los pagos mensuales dentro del rango
            query = """
            SELECT payment_date, payment_amount
            FROM payments
            WHERE payment_date BETWEEN %s AND %s
            AND card_number = %s
            """

            # Ejecuta la consulta con los parámetros proporcionados
            cursor.execute(query, (start_date, end_date, self.card_number))

            # Obtiene todos los registros resultantes de la consulta
            monthly_payments = cursor.fetchall()

            # Crea una lista para almacenar los resultados formateados
            formatted_payments = []

            # Itera sobre los resultados y los formatea
            for payment in monthly_payments:
                formatted_payment = {
                    'payment_date': payment[0],
                    'payment_amount': payment[1]
                }
                formatted_payments.append(formatted_payment)

            return formatted_payments

        finally:
            # Cierra el cursor y la conexión, independientemente de si hubo una excepción
            cursor.close()
            connection.close()

    def store_amortization_plan(self, amortization_plan):
            # Almacena el plan de amortización de la compra
            self.amortization_plan = amortization_plan

    def store_payment_schedule(self, payment_schedule):
            # Almacena las fechas y valores de cada cuota
            self.payment_schedule = payment_schedule

    def get_amortization_plan(self):
            # Devuelve el plan de amortización almacenado
            return self