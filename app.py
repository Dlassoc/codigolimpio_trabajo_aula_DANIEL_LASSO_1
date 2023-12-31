from flask import Flask, request, jsonify, render_template
from credit_card_module import CreditCard
from database_info.database import create_connection
from decimal import Decimal
from datetime import datetime
from dateutil.relativedelta import relativedelta


"""
#ENTREGA 2 WEB SERVICE
def card_exists(card_number):
    # Verificar si la tarjeta ya existe en la base de datos
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM credit_card WHERE card_number = %s", (card_number,))
    card_count = cursor.fetchone()[0]
    connection.close()
    return card_count > 0
app = Flask(__name__)

@app.route('/api/cards/new')
def register_credit_card_via_web_service():
    
    try:
        # Recuperar los datos de la tarjeta del request utilizando request.args
        card = CreditCard(
            card_number=request.args['card_number'],
            owner_id=request.args['owner_id'],
            owner_name=request.args['owner_name'],
            bank_name=request.args['bank_name'],
            due_date=request.args['due_date'],
            franchise=request.args['franchise'],
            payment_day=request.args['payment_day'],
            monthly_fee=request.args['monthly_fee'],
            interest_rate=request.args['interest_rate']
        )

        # Crear una conexión a la base de datos
        connection = create_connection()
        cursor = connection.cursor()

        # Comprobar si la tarjeta ya existe en la base de datos
        cursor.execute("SELECT COUNT(*) FROM credit_card WHERE card_number = %s", (card.card_number,))
        card_count = cursor.fetchone()[0]

        # Si la tarjeta ya existe, retornar un mensaje de error
        if card_count > 0:
            connection.close()
            return jsonify({'status': 'error', 'message': 'Tarjeta ya existe en la base de datos'}), 400

        # Insertar la tarjeta en la base de datos
        cursor.execute(
            "INSERT INTO credit_card (card_number, owner_id, owner_name, bank_name, due_date, franchise, payment_day, monthly_fee, interest_rate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                card.card_number,
                card.owner_id,
                card.owner_name,
                card.bank_name,
                card.due_date,
                card.franchise,
                card.payment_day,
                card.monthly_fee,
                card.interest_rate,
            ),
        )
        connection.commit()
        connection.close()

        # Retornar un mensaje de éxito
        return jsonify({'status': 'ok', 'message': 'Tarjeta guardada exitosamente'})
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 400

@app.route('/api/simulate/purchase')
def calculate_installment():
    try:
        # Obtener los datos de la tarjeta de crédito y la compra
        card_number = request.args['card_number']
        purchase_amount = int(request.args['purchase_amount'])
        num_installments = int(request.args['num_installments'])

        # Consultar la tasa de interés de la tarjeta de crédito desde la base de datos
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT interest_rate FROM credit_card WHERE card_number = %s", (card_number,))
        interest_rate = cursor.fetchone()

        if interest_rate is None:
            connection.close()
            return jsonify({'status': 'error', 'message': 'Tarjeta no encontrada'}), 404

        interest_rate = interest_rate[0]  # Extraer el valor de la tasa de interés

        # Calcular la cuota mensual y el total de intereses
        monthly_interest_rate = interest_rate / 12 / 100

        if purchase_amount % num_installments == 0:
            # Cuando la compra es divisible entre el número de cuotas, se calcula la cuota fija
            monthly_installment = purchase_amount // num_installments
            total_interests = 0
        else:
            # Cuando la compra no es divisible, se calcula con interés
            monthly_installment = (purchase_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -num_installments)
            total_interests = (monthly_installment * num_installments) - purchase_amount

        connection.close()

        return jsonify({'status': 'ok', 'monthly_installment': round(monthly_installment, 2), 'total_interests': round(total_interests, 2)})
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 400

@app.route('/api/simulate/saving')
def suggest_savings_plan():
    try:
        # Obtener los datos de la simulación desde el request
        purchase_amount = float(request.args.get('purchase_amount'))
        monthly_payment = float(request.args.get('monthly_payment'))
        interest_rate = float(request.args.get('interest_rate'))

        if monthly_payment <= 0:
            return jsonify({'status': 'error', 'message': 'El pago mensual debe ser mayor que cero'}), 400

        if interest_rate < 0:
            return jsonify({'status': 'error', 'message': 'La tasa de interés no puede ser negativa'}), 400

        if interest_rate == 0:
            # Si la tasa de interés es cero, calcular sin intereses
            if monthly_payment <= 0:
                return jsonify({'status': 'error', 'message': 'El pago mensual debe ser mayor que cero'}), 400

            months_needed = int(purchase_amount / monthly_payment)
        else:
            # Calcular la cantidad de meses necesarios para ahorrar el monto de la compra
            months_needed = 0
            remaining_amount = purchase_amount
            while remaining_amount > 0:
                remaining_amount += (remaining_amount * interest_rate / 12 / 100)  # Calcular el aumento mensual
                remaining_amount -= monthly_payment  # Restar el pago mensual
                months_needed += 1

        return jsonify({'status': 'ok', 'months': months_needed})
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 400

@app.route('/api/purchase/new')
def register_purchase():
    try:
        # Obtener los datos de la compra desde el request
        card_number = request.args.get('card_number')
        purchase_amount = float(request.args.get('purchase_amount'))
        payments = int(request.args.get('payments'))
        purchase_date = request.args.get('purchase_date')

        # Verificar si la tarjeta existe en la base de datos
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT card_number FROM credit_card WHERE card_number = %s", (card_number,))
        card_number_result = cursor.fetchone()
        connection.close()

        if card_number_result is None:
            return jsonify({'status': 'error', 'message': 'Tarjeta no encontrada'}), 404

        # Calcular el plan de amortización
        monthly_payment = purchase_amount / payments

        # Almacenar el plan de amortización y la información de la compra en la base de datos
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO purchase (card_number, purchase_amount, payments, purchase_date) VALUES (%s, %s, %s, %s) RETURNING purchase_id",
            (card_number, purchase_amount, payments, purchase_date),
        )
        purchase_id = cursor.fetchone()[0]

        for month in range(payments):
            cursor.execute(
                "INSERT INTO payment_schedule (purchase_id, payment_date, payment_amount) VALUES (%s, %s, %s)",
                (purchase_id, purchase_date, monthly_payment),
            )

            # Calcular la fecha de pago del próximo mes
            year, month, day = map(int, purchase_date.split("-"))
            if month == 12:
                year += 1
                month = 1
            else:
                month += 1
            purchase_date = f"{year}-{month:02d}-{day}"

        connection.commit()
        connection.close()

        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 400

@app.route('/api/cards/card_info', methods=['POST'])
def get_credit_card_info():
    card_number = request.form['card_number']

    if not card_number:
        return jsonify({'status': 'error', 'message': 'Por favor, ingrese un número de tarjeta válido'}), 400

    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM credit_card WHERE card_number = %s", (card_number,))
    card_info = cursor.fetchone()
    connection.close()

    if card_info is not None:
        card_info_dict = {
            'card_number': card_info[0],
            'owner_id': card_info[1],
            'owner_name': card_info[2],
            'bank_name': card_info[3],
            'due_date': card_info[4],
            'franchise': card_info[5],
            'payment_day': card_info[6],
            'monthly_fee': float(card_info[7]),
            'interest_rate': float(card_info[8])
        }

        return render_template('credit_card_info.html', card_info=card_info_dict)
    else:
        return jsonify({'status': 'error', 'message': 'Tarjeta no encontrada'}), 404
"""

#ENTREGA FINAL APP WEB
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")



@app.route('/register_card', methods=['GET', 'POST'])
def register_credit_card_service():
    if request.method == 'POST':

        try:
            # Recuperar los datos de la tarjeta del request utilizando request.args
            card = CreditCard(
                card_number=request.form['card_number'],
                owner_id=request.form['owner_id'],
                owner_name=request.form['owner_name'],
                bank_name=request.form['bank_name'],
                due_date=request.form['due_date'],
                franchise=request.form['franchise'],
                payment_day=request.form['payment_day'],
                monthly_fee=request.form['monthly_fee'],
                interest_rate=request.form['interest_rate']
            )

            # Crear una conexión a la base de datos
            connection = create_connection()
            cursor = connection.cursor()

            # Comprobar si la tarjeta ya existe en la base de datos
            cursor.execute("SELECT COUNT(*) FROM credit_card WHERE card_number = %s", (card.card_number,))
            card_count = cursor.fetchone()[0]

            # Si la tarjeta ya existe, retornar un mensaje de error
            if card_count > 0:
                connection.close()
                return render_template('registration_error.html', message="La tarjeta ya existe en la base de datos"), 400

            # Insertar la tarjeta en la base de datos
            cursor.execute(
                "INSERT INTO credit_card (card_number, owner_id, owner_name, bank_name, due_date, franchise, payment_day, monthly_fee, interest_rate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    card.card_number,
                    card.owner_id,
                    card.owner_name,
                    card.bank_name,
                    card.due_date,
                    card.franchise,
                    card.payment_day,
                    card.monthly_fee,
                    card.interest_rate,
                ),
            )
            connection.commit()
            connection.close()

            # Retornar un mensaje de éxito
            return render_template('registration_success.html', message='Tarjeta guardada exitosamente')
        except Exception as e:
                return render_template('registration_error.html', message=str(e)), 400
    return render_template("regist_credit_card.html")

@app.route('/save_money_plan', methods=['GET', 'POST'])
def save_money_suggestion():
    if request.method == 'POST':
        try:
            purchase_amount = Decimal(request.form['purchase_amount'])
            monthly_payment = Decimal(request.form['monthly_payment'])
            interest_rate = Decimal(request.form['interest_rate'])

            if monthly_payment <= 0:
                return render_template('save_money_suggestion_error.html', message='El pago mensual debe ser mayor que cero'), 400

            if interest_rate < 0:
                return render_template('save_money_suggestion_error.html', message='La tasa de interés no puede ser negativa'), 400

            if interest_rate == 0:
                # Si la tasa de interés es cero, calcular sin intereses
                if monthly_payment <= 0:
                    return render_template('save_money_suggestion_error.html', message='El pago mensual debe ser mayor que cero'), 400

                months_needed = int(purchase_amount / monthly_payment)
            else:
                # Calcular la cantidad de meses necesarios para ahorrar el monto de la compra
                months_needed = 0
                remaining_amount = purchase_amount
                while remaining_amount > 0:
                    remaining_amount += (remaining_amount * interest_rate / 12 / 100)  # Calcular el aumento mensual
                    remaining_amount -= monthly_payment  # Restar el pago mensual
                    months_needed += 1

            return render_template('save_money_suggestion_result.html', months_needed=months_needed)
        except Exception as e:
            return render_template('save_money_suggestion_error.html', message=str(e)), 400

    # Si se llega al formulario a través de GET, mostrar el formulario de sugerencia de ahorro
    return render_template('save_money_suggestion_form.html')

@app.route('/simulate_purchase', methods=['GET', 'POST'])
def simulate_purchase():
    if request.method == 'POST':
        try:
            card_number = request.form['card_number']
            purchase_amount = Decimal(request.form['purchase_amount'])
            num_installments = int(request.form['num_installments'])

            # Consultar la tasa de interés de la tarjeta de crédito desde la base de datos
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT interest_rate FROM credit_card WHERE card_number = %s", (card_number,))
            interest_rate = cursor.fetchone()

            if interest_rate is None:
                connection.close()
                return render_template('purchase_simulation_error.html', message='Tarjeta no encontrada'), 404

            interest_rate = Decimal(interest_rate[0])

            monthly_interest_rate = interest_rate / 12 / 100  # Tasa de interés mensual

            if monthly_interest_rate == 0:
                monthly_installment = purchase_amount / num_installments
                total_interests = Decimal(0)
            else:
                monthly_installment = (purchase_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -num_installments)
                total_interests = (monthly_installment * num_installments) - purchase_amount

            connection.close()

            return render_template('purchase_simulation_result.html', monthly_installment=round(monthly_installment, 2), total_interests=round(total_interests, 2))
        except Exception as e:
            return render_template('purchase_simulation_error.html', message=str(e)), 400

    # Si se llega al formulario a través de GET, mostrar el formulario de simulación de compra
    return render_template('purchase_simulation_form.html')



@app.route('/register_purchase', methods=['GET', 'POST'])
def register_purchase_web():
    if request.method == 'POST':
        try:
            card_number = request.form['card_number']
            purchase_amount = Decimal(request.form['purchase_amount'])
            payments = int(request.form['payments'])
            purchase_date = request.form['purchase_date']

            # Verificar si la tarjeta existe en la base de datos y obtener su tasa de interés
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT interest_rate FROM credit_card WHERE card_number = %s", (card_number,))
            interest_rate = cursor.fetchone()

            if interest_rate is None:
                connection.close()
                return render_template('purchase_registration_error.html', message='Tarjeta no encontrada'), 404

            interest_rate = Decimal(interest_rate[0])  # Obtener el valor de la tasa de interés desde la consulta

            # Calcular la tasa de interés mensual
            monthly_interest_rate = interest_rate / 12 / 100

            # Inicializar el saldo pendiente y la lista de pagos
            remaining_balance = purchase_amount
            payment_schedule_data = []

            # Convertir la fecha de compra a un objeto de fecha
            purchase_date = datetime.strptime(purchase_date, "%Y-%m-%d")

            for _ in range(payments):
                # Calcular la cuota mensual
                monthly_payment = remaining_balance * (monthly_interest_rate * (1 + monthly_interest_rate) ** payments) / ((1 + monthly_interest_rate) ** payments - 1)

                # Agregar el pago a la lista
                payment_schedule_data.append((purchase_date.strftime("%Y-%m-%d"), monthly_payment, remaining_balance))

                # Actualizar el saldo pendiente
                remaining_balance -= monthly_payment

                # Calcular la fecha de pago del próximo mes
                purchase_date = purchase_date.replace(day=1)  # Ajustar al primer día del mes
                purchase_date = purchase_date + relativedelta(months=1)  # Añadir un mes

            # Almacenar el plan de amortización y la información de la compra en la base de datos
            cursor.execute(
                "INSERT INTO purchase (card_number, purchase_amount, payments, purchase_date) VALUES (%s, %s, %s, %s) RETURNING purchase_id",
                (card_number, purchase_amount, payments, purchase_date),
            )
            purchase_id = cursor.fetchone()[0]

            for payment_data in payment_schedule_data:
                cursor.execute(
                    "INSERT INTO payment_schedule (purchase_id, payment_date, payment_amount) VALUES (%s, %s, %s)",
                    (purchase_id, payment_data[0], payment_data[1]),
                )

            connection.commit()
            connection.close()

            return render_template('purchase_registration_success.html')
        except Exception as e:
            return render_template('purchase_registration_error.html', message=str(e)), 400

    # Si se llega al formulario a través de GET, mostrar el formulario de registro de compra
    return render_template('purchase_registration_form.html')


@app.route('/payment_schedule', methods=['GET', 'POST'])
def payment_schedule_web():
    if request.method == 'POST':
        try:
            card_number = request.form['card_number']

            # Verificar si la tarjeta existe en la base de datos
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT card_number FROM credit_card WHERE card_number = %s", (card_number,))
            card_number_result = cursor.fetchone()

            if card_number_result is None:
                connection.close()
                return render_template('payment_schedule_error.html', message='Tarjeta no encontrada'), 404

            # Consultar la información de los pagos basada en el número de tarjeta
            cursor.execute(
                "SELECT p.purchase_date, ps.payment_date, ps.payment_amount "
                "FROM purchase AS p "
                "INNER JOIN payment_schedule AS ps ON p.purchase_id = ps.purchase_id "
                "WHERE p.card_number = %s",
                (card_number,),
            )

            payment_schedule_data = cursor.fetchall()

            connection.close()

            # Realizar un seguimiento del saldo pendiente
            remaining_balance = Decimal(0)
            updated_payment_schedule_data = []

            for i in range(len(payment_schedule_data)):
                purchase_date, payment_date, payment_amount = payment_schedule_data[i]
                remaining_balance += payment_amount  # Agregar el monto del pago al saldo pendiente
                updated_payment_schedule_data.append((purchase_date, payment_date, round(payment_amount, 2), round(remaining_balance, 2)))
                remaining_balance -= payment_amount  # Restar el monto del pago al saldo pendiente

            return render_template('payment_schedule_report.html', payment_schedule_data=updated_payment_schedule_data)

        except Exception as e:
            return render_template('payment_schedule_error.html', message=str(e)), 400

    # Si se llega al formulario a través de GET, mostrar el formulario de programación de pagos
    return render_template('payment_schedule_form.html')

#REQUISITO SORPRESA
@app.route('/delete_card', methods=['GET', 'POST'])
def delete_card():
    if request.method == 'POST':
        try:
            card_number = request.form['card_number']

            # Verificar si la tarjeta existe en la base de datos
            connection = create_connection()
            cursor = connection.cursor()

            # Verificar si la tarjeta existe en la base de datos
            cursor.execute("SELECT card_number FROM credit_card WHERE card_number = %s", (card_number,))
            card_number_result = cursor.fetchone()

            if card_number_result is None:
                connection.close()
                return render_template('delete_card_error.html', message='Tarjeta no encontrada'), 404

            # Si la tarjeta existe, elimínala de la base de datos
            cursor.execute("DELETE FROM credit_card WHERE card_number = %s", (card_number,))
            connection.commit()
            connection.close()

            return render_template('delete_card_success.html')

        except Exception as e:
            return render_template('delete_card_error.html', message=str(e)), 400

    # Si se llega a la vista a través de GET, mostrar el formulario para eliminar la tarjeta
    return render_template('delete_card_form.html')


if __name__ == '__main__':
    app.run(debug=True) 