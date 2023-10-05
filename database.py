import psycopg2
from SecretConfig import HOST, DATABASE, USER, PASSWORD, PORT

def create_connection():
    return psycopg2.connect(host=HOST, dbname=DATABASE, user=USER, password=PASSWORD, port=PORT)

def setUp(self):
        self.connection = create_connection()
        self.cursor = self.connection.cursor()

        # Eliminamos todas las tarjetas de la tabla
        self.cursor.execute("DELETE FROM credit_card")
        self.connection.commit()

def tearDown(self):
        self.connection.close()

