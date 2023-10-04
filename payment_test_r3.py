class SavingsPlan:
    def __init__(self, card_number, target_purchase_amount, savings_period):
        if target_purchase_amount <= 0:
            raise ValueError("Error: el monto de compra objetivo debe ser superior a cero")
        if savings_period <= 0:
            raise ValueError("Error: el período de ahorro debe ser superior a cero")
        # Eliminar el nombre del banco y guardar solo los últimos 4 dígitos
        self.card_number = card_number[-4:]
        self.target_purchase_amount = target_purchase_amount
        self.savings_period = savings_period
        self.savings_amount = target_purchase_amount / savings_period  # Calcular la cantidad de ahorro mensual
        self.current_savings = 0

    def save(self):
        if self.current_savings < self.target_purchase_amount:
            self.current_savings += self.savings_amount
        else:
            print("¡Felicidades! Has alcanzado tu objetivo de ahorro.")

    def get_balance(self):
        return self.current_savings
