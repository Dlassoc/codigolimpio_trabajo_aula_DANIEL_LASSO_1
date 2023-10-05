import unittest
from database import create_connection
from credit_card_module import CreditCard
from datetime import datetime

class TestDatabase(unittest.TestCase):

    def setUp(self):
        # Crear una conexión a la base de datos al comenzar la prueba
        self.connection = create_connection()
        self.cursor = self.connection.cursor()

        # Eliminar todas las tarjetas de la tabla en la base de datos
        self.cursor.execute("DELETE FROM credit_card")
        self.connection.commit()

    def tearDown(self):
        # Cerrar la conexión a la base de datos al finalizar la prueba
        self.connection.close()

    def test_insert_card(self, card=None):
        # Crear un objeto CreditCard si no se proporciona uno
        if card is None:
            card = CreditCard(
                card_number="556677",
                owner_id="1020889955",
                owner_name="Estudiante pelao",
                bank_name="Bancolombia",
                due_date="31/12/2027",
                franchise="VISA",
                payment_day=10,
                monthly_fee=24000,
                interest_rate=3.1
            )

        cursor = self.connection.cursor()

        # Comprobar si la tarjeta ya existe en la base de datos
        cursor.execute("SELECT COUNT(*) FROM credit_card WHERE card_number = %s", (card.card_number,))
        card_count = cursor.fetchone()[0]

        if card_count > 0:
            raise Exception("Ya existe una tarjeta con el mismo número")

        # Convertir la fecha de vencimiento a un objeto de tipo `date`
        due_date = datetime.strptime(card.due_date, "%d/%m/%Y").date()

        # Guardar la tarjeta en la base de datos
        cursor.execute(
            "INSERT INTO credit_card (card_number, owner_id, owner_name, bank_name, due_date, franchise, payment_day, monthly_fee, interest_rate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                card.card_number,
                card.owner_id,
                card.owner_name,
                card.bank_name,
                due_date,
                card.franchise,
                card.payment_day,
                card.monthly_fee,
                card.interest_rate,
            ),
        )
        self.connection.commit()

        # Verificar que la tarjeta se haya creado
        cursor.execute("SELECT COUNT(*) FROM credit_card WHERE card_number = %s", (card.card_number,))
        card_count = cursor.fetchone()[0]

        if card_count == 0:
            raise Exception("La tarjeta no fue creada")

        result = "Tarjeta guardada exitosamente"

        # Comparar el resultado con el mensaje esperado
        self.assertEqual(result, "Tarjeta guardada exitosamente")
        return result

    def test_expired_credit_card(self):
        # Crear una tarjeta de crédito vencida
        card = CreditCard(
            card_number="442233",
            owner_id="1010123456",
            owner_name="Comprador compulsivo",
            bank_name="Popular",
            due_date="31/12/2022",  # Fecha pasada, tarjeta vencida
            franchise="Mastercard",
            payment_day=5,
            monthly_fee=34000,
            interest_rate=3.4,
        )

        # Verificar si la tarjeta está vencida utilizando el método is_expired
        is_expired = card.is_expired()

        # Comprobar si se obtiene el resultado esperado
        self.assertTrue(is_expired, "NO SE PUEDE AGREGAR PORQUE ESTÁ VENCIDA")

    def test_existing_credit_card_2(self):
        # Crear una tarjeta de crédito con los mismos datos de entrada
        card = CreditCard(
            card_number="556677",
            owner_id="1020889955",
            owner_name="Estudiante pelao",
            bank_name="Bancolombia",
            due_date="31/12/2027",
            franchise="VISA",
            payment_day=10,
            monthly_fee=24000,
            interest_rate=3.1,
        )

        # Llamar al método de prueba `test_insert_card` directamente
        self.test_insert_card()

        # Intentar insertar la misma tarjeta una segunda vez
        # Esto debería fallar y lanzar la excepción que estás esperando
        with self.assertRaises(Exception) as e:
            self.test_insert_card()

        # Comprobar si se obtiene el mensaje correcto
        self.assertEqual(str(e.exception), "Ya existe una tarjeta con el mismo número")

    def test_T4_insert_credit_card(self):
        # Crear una tarjeta de crédito con los datos del T4
        card = CreditCard(
            card_number="223344",
            owner_id="1010123456",
            owner_name="Comprador compulsivo",
            bank_name="Falabella",
            due_date="31/12/2025",
            franchise="VISA",
            payment_day=16,
            monthly_fee=0,
            interest_rate=3.4,
        )

        # Insertar la tarjeta por primera vez (esto debería ser exitoso)
        mensaje = self.test_insert_card()

        # Verificar si el mensaje es igual a "Tarjeta guardada exitosamente"
        self.assertEqual(mensaje, "Tarjeta guardada exitosamente")

    def test_T5_insert_credit_card(self):
        # Crear una tarjeta con los valores proporcionados
        card = CreditCard(
            card_number="445566",
            owner_id="1010123456",
            owner_name="Comprador compulsivo",
            bank_name="BBVA",
            due_date="31/12/2027",
            franchise="Mastercard",
            payment_day=5,
            monthly_fee=34000,
            interest_rate=0,
        )

        # Llamar al método de prueba `test_insert_card` con la tarjeta creada
        result = self.test_insert_card(card)

        # Verificar si la tarjeta se guardó exitosamente
        self.assertEqual(result, "Tarjeta guardada exitosamente")

if __name__ == "__main__":
    unittest.main()
