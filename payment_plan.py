import psycopg2
from SecretConfig import HOST, DATABASE, USER, PASSWORD, PORT


class PaymentPlan:
    def __init__(self, card_number, purchase_date, purchase_amount, payment_date, payment_amount, interest_amount, capital_amount, balance):
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

    def calculate_installment_interest(self, annual_interest_rate, num_installments):
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
    

    def store_amortization_plan(self, amortization_plan):
        # Almacena el plan de amortización de la compra
        self.amortization_plan = amortization_plan

    def store_payment_schedule(self, payment_schedule):
        # Almacena las fechas y valores de cada cuota
        self.payment_schedule = payment_schedule

    def get_amortization_plan(self):
        # Devuelve el plan de amortización almacenado
        return self.amortization_plan

    def get_card_used(self):
        # Devuelve la identidad de la tarjeta utilizada
        return self.card_used

    def get_payment_schedule(self):
        # Devuelve las fechas y valores de cada cuota almacenados
        return self.payment_schedule

    def calculate_installment_interest(self):
        if self.annual_interest_rate == 0:
            # Si la tasa de interés es cero, la cuota mensual es simplemente el monto de compra dividido por el número de cuotas
            monthly_installment = self.purchase_amount / self.num_installments
            total_interest = 0  # En este caso, el interés total es cero
        elif self.num_installments <= 0:
            raise NumInstallmentsError("Error: el número de cuotas debe ser mayor a cero")
        else:
            monthly_interest_rate = self.annual_interest_rate / 12 / 100
            monthly_installment = (self.purchase_amount * monthly_interest_rate) / (
                1 - (1 + monthly_interest_rate) ** -self.num_installments
            )
            total_interest = (monthly_installment * self.num_installments) - self.purchase_amount

        return round(monthly_installment, 2), round(total_interest, 2)

    def calculate_savings_plan(self):
        monthly_installment, total_interest = self.calculate_installment_interest()
        total_savings_needed = self.purchase_amount + total_interest
        return round(total_interest, 2), round(total_savings_needed, 2)

    def suggest_savings_plan(self):
        total_interest, total_savings_needed = self.calculate_savings_plan()
        monthly_savings = total_savings_needed / self.num_installments
        return f"Para evitar pagar {total_interest} en intereses, le sugerimos ahorrar {monthly_savings} mensuales y comprar de contado."


class PurchaseAmountError(ValueError):
    def __init__(self, message="Error: el monto debe ser superior a cero"):
        self.message = message
        super().__init__(self.message)


class NumInstallmentsError(Exception):
    def __init__(self, message="Error: el número de cuotas debe ser mayor a cero"):
        self.message = message
        super().__init__(self.message)

class PurchaseAmountError(ValueError):
    def __init__(self, message="Error: el monto de compra debe ser superior a cero"):
        self.message = message
        super().__init__(self.message)

class NumInstallmentsError(ValueError):
    def __init__(self, message="Error: el número de cuotas debe ser mayor a cero"):
        self.message = message
        super().__init__(self.message)

class CardNotFoundError(Exception):
    def __init__(self, message="Error: La tarjeta indicada no existe"):
        self.message = message
        super().__init__(self.message)

class UsuryError(Exception):
    def __init__(self, message="Error: La tasa de interés supera el límite legal"):
        self.message = message
        super().__init__(self.message)


