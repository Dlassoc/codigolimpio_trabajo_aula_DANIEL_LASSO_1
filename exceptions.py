# exceptions.py
class PurchaseAmountError(ValueError):
    def __init__(self, message="Error: el monto de compra debe ser superior a cero"):
        self.message = message
        super().__init__(self.message)

class NumInstallmentsError(Exception):
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
