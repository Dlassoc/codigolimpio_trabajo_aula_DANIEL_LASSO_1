Para esta entrega del web service usando la libreria flask de python, lo unico que tendrás que tener es
la version de python mas reciente y flask instalado, una vez cuentes con eso puedes ejecutar el 
modulo app.py.

En este modulo esta el servidor de FLASK totalmente configurado, para ejecutar las diferentes rutas con los
decoradores definidos.
IMPORTANTE: SI EL NUMERO DE TARJETA QUE PONEN EN card_number NO EXISTE EN LA BASE DE DATOS, NO PODRAN 
SIMULAR NADA, CREEN LA TARJETA EN EL R1 Y UNA VEZ CREADA, SI FUNCIONARÁ CORRECTAMENTE

Para el R1
http://localhost:5000/api/card/new?card_number=########&owner_id=######&owner_name=XXXXXXXXXX&bank_name=XXXXXX&due_date=YYYY-MM-DD&franchise=XXXX&payment_day=##&monthly_fee=#####&interest_rate=###"""

TENER EN CUENTA QUE VAN A REGISTRAR YA FUE REGISTRADA, NO DEJARÁ REGISTRARLA DE NUEVO.

Para el R2
http://localhost:5000/api/simulate/purchase?card_number=#####&purchase_amount=#####&payments=##

Para el R3
http://localhost:5000/api/simulate/saving?purchase_amount=#####&monthly_payment=#####&interest_rate=##4

Para el R4
http://localhost:5000/api/purchase/new?card_number=#####&purchase_amount=#####&payments=##&purchase_date=YYYY-MM-DD

