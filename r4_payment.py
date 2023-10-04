from payment_plan import PaymentPlan
class Purchase:
    def __init__(self, card_number, payment_plan):
        # Eliminar el nombre del banco y guardar solo los últimos 4 dígitos
        self.card_number = card_number[-4:]
        self.payment_plan = payment_plan  # Una instancia de la clase PaymentPlan

    def get_monthly_payments(self):
        # Esta función devuelve un diccionario donde las claves son las fechas de pago
        # y los valores son los montos de pago
        return {payment_date: payment_amount for payment_date, payment_amount in zip(self.payment_plan.payment_date, self.payment_plan.payment_amounts)}
