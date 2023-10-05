from payment_plan_t4 import PaymentPlan
import psycopg2
from database import HOST, DATABASE, USER, PASSWORD, PORT 
from datetime import datetime, timedelta
from decimal import Decimal 

def calculate_total_monthly_payments(self, start_date, end_date):
        total_payments = 0

        # Convertir las fechas de inicio y finalización en objetos datetime
        start_date = datetime.strptime(start_date, "%d-%b")
        end_date = datetime.strptime(end_date, "%d-%b")

        # Realizar una consulta SQL para obtener las filas relevantes de la tabla de amortización
        connection = psycopg2.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            port=PORT
        )

        cursor = connection.cursor()

        cursor.execute(
            "SELECT payment_date, payment_amount FROM amortization_table WHERE payment_date >= %s AND payment_date <= %s",
            (start_date, end_date)
        )

        rows = cursor.fetchall()

        # Calcular la suma de las cuotas mensuales
        for row in rows:
            total_payments += Decimal(row[1])

        connection.close()

        print(round(total_payments, 2)) 
def calculate_and_store_monthly_payments(self, annual_interest_rate, num_installments):
        # Calcular las cuotas mensuales y almacenarlas en la base de datos
        if self.payment_date is not None:
            current_date = datetime.strptime(self.payment_date, "%d/%m/%Y")
            monthly_installment, total_interest = self.calculate_installment_interest(
                annual_interest_rate, num_installments)

            for _ in range(num_installments):
                # Insertar cada cuota mensual en la base de datos
                self.cursor.execute(
                    "INSERT INTO payments (payment_date, payment_amount, card_number) VALUES (%s, %s, %s)",
                    (current_date.strftime("%Y-%m-%d"), monthly_installment, self.card_number)
                )
                self.connection.commit()  # Commit the transaction

                # Avanzar al siguiente mes
                current_date += timedelta(days=30)

        else:
            raise ValueError("Error: la fecha de pago es requerida")
