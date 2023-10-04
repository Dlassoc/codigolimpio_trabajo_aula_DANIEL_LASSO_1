class CreditCard:
    def __init__(self, card_number, owner_id, owner_name, bank_name, due_date,
                 franchise, payment_day, monthly_fee, interest_rate):
        self.card_number = card_number
        self.owner_id = owner_id
        self.owner_name = owner_name
        self.bank_name = bank_name
        self.due_date = due_date
        self.franchise = franchise
        self.payment_day = payment_day
        self.monthly_fee = monthly_fee
        self.interest_rate = interest_rate
