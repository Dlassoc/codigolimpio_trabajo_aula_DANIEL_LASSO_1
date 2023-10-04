import psycopg2
import datetime
from SecretConfig import HOST, DATABASE, USER, PASSWORD, PORT

def create_connection():
    return psycopg2.connect(host=HOST, dbname=DATABASE, user=USER, password=PASSWORD, port=PORT)

def insert_card(connection, card):
    cursor = connection.cursor()

    # Verificar si la tarjeta ya existe
    cursor.execute("SELECT COUNT(*) FROM credit_card WHERE card_number = %s", (card.card_number,))
    card_count = cursor.fetchone()[0]

    if card_count > 0:
        raise Exception("Ya existe una tarjeta con el mismo número")

    # Convertir la fecha de vencimiento a un objeto de tipo `date`
    due_date = datetime.date.fromordinal(int(card.payment_day))

    # Guardar la tarjeta en la base de datos
    cursor.execute("INSERT INTO credit_cards (card_number, owner_id, owner_name, bank_name, due_date, franchise, payment_day, monthly_fee, interest_rate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (card.card_number, card.owner_id, card.owner_name, card.bank_name, due_date.strftime("%Y-%m-%d"), card.franchise, card.payment_day, card.monthly_fee, card.interest_rate))
    connection.commit()







def get_cards(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM credit_card")
    cards = cursor.fetchall()
    return cards

def edit_card(connection, card):
    cursor = connection.cursor()
    cursor.execute("UPDATE credit_card SET card_number = %s, owner_id = %s, owner_name = %s, bank_name = %s, due_date = %s, franchise = %s, payment_day = %s, monthly_fee = %s, interest_rate = %s WHERE card_card_number = %s",
               (card.card_number, card.owner_id, card.owner_name, card.bank_name, card.due_date, card.franchise, card.payment_day, card.monthly_fee, card.interest_rate, card.card_card_number))

    connection.commit()

def delete_card(connection, card_number):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM credit_card WHERE card_card_number = %s", (card_number,))
    connection.commit()
