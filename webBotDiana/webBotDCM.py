# Módulos necesarios para el desarrollo del programa
from bson.objectid import ObjectId
from flask import Flask, request, json, Response
import time
from pymongo import MongoClient
import socket
from RAMBOT import RAM

# Inicialización de Flask
app = Flask(__name__)

con = MongoClient('127.0.0.1', 27017)  # Conectar con MongoDB (localhost, puerto)

db = con.GrootBot  # Definir Base de datos GrootBot
log = db.logHist  # Dentro de GrootBot, crear la colección logHist
ram = db.memRam  # Dentro de GrootBot, crear la colección memRam

# (con botón solo debe correr una vez)
@app.route('/api/web-bot/<name>', methods=['PUT'])
def info(name):  # Muestra "datos personales" del web-bot

    fechaNac = time.strftime("%c")
    bot_id = hash(fechaNac)
    creadora = "DianaCM"

    return "¡Hola, mi nombres es " + name + "! Soy un web-bot... " \
           + "Acabo de nacer (" + fechaNac + \
           "), y me han asignado el id: " + str(bot_id) + \
           ". Mi creadora es: " + creadora


# load es para decodificar
@app.route('/api/web-bot', methods=['POST'])  # Ruta para lo que el bot sabe hacer
def default():  # Lo que el bot hace por defecto desde que inicia
    try:
        tipo = request.json["tipo"]  # Seleccionar en el Json lo que contiene la clave tipo
        operacion = request.json['operacion']  # Seleccionar en el Json lo que contiene la clave operación

        # Tipo "A" es para operaciones con más de dos números (sumas y multiplicaciones)
        if (tipo == "A"):
            numeros = request.json['numeros']  # Seleccionar en el Json lo que contiene la clave numeros
            if (operacion == "suma"):  # Si la operación es suma, ingresa al método de suma
                total = suma(numeros)
            if (operacion == "multiplica"):  # Si la operación es suma, ingresa al método de multiplica
                total = multiplica(numeros)

                # Tipo "B" es para operaciones  de dos números (restas y divisiones)
        if (tipo == "B"):
            num1 = request.json['num1']  # Seleccionar en el Json lo que contiene la clave num1
            num2 = request.json['num2']  # Seleccionar en el Json lo que contiene la clave num2
            if (operacion == "resta"):  # Si la operación es suma, ingresa al método de resta
                total = resta(num1, num2)
            if (operacion == "divide"):  # Si la operación es suma, ingresa al método de divide
                total = divide(num1, num2)

        operacion = {"Resultado ": total}  # Resulato

    except Exception as e:  # Excepción en caso de que lo anterior no funcione
        print(e)

    js = json.dumps(operacion)  # Codificar Json
    resp = Response(js, content_type='application/json')

    return resp


def suma(numeros):  # Método para sumar numeros recibidos anteriormente
    sum = 0
    for i in numeros:
        sum += i
    return sum


def multiplica(numeros):  # Método para multiplicar numeros recibidos anteriormente
    mult = 1
    for i in numeros:
        mult *= i
    return mult


def resta(num1, num2):  # Método para restar dos numeros recibidos anteriormente
    rest = num1 - num2
    return rest


def divide(num1, num2):  # Método para dividir dos numeros recibidos anteriormente
    div = num1 / num2
    return div


@app.route('/api/web-bot/aprender', methods=['POST'])
def aprende():
    action = request.json["action"]
    codigo = request.json["code"]  # Seleccionar en el Json lo que contiene la clave code

    resultado = {'He aprendido a ': action}  # Respuesta Json
    codificar = json.dumps(resultado)

    resp = Response(codificar, status=200, content_type='application/json')  # Configuración de la respuesta
    resp.headers['Link'] = "www.GrootBot.com"

    accion = ("Aprender " + action)
    guardar(accion)  # Ir al método guardar para almacenar la información en historial

    accionGuardar =[
        RAM(codigo)
    ]

    for insertar in accionGuardar:
       ram.insert(insertar.toMemRam())
       exec(codigo)  #Ejecutar código recibido

    return resp

@app.route('/api/web-bot/mostrar/estados')
def muestra_estados():  # Método para mostrar historial

    accion = "Mostrar estados (LOG)"
    guardar(accion)

    archEscritura = open('log.txt', 'w')
    for cursor in log.find({}):
        archEscritura.write(str(cursor) + " FIN \n")

    archEscritura.close()
    archLectura = open('log.txt', 'r')
    obtener = archLectura.read()
    archLectura.close()
    return obtener


@app.route('/api/web-bot/mostrar/conocimientos')
def muestra_memoria():  # Método para mostrar lo que hay en RAM

    accion = "Mostrar conocimientos (RAM)"
    guardar(accion)

    archEscritura = open('ram.txt', 'w')
    for cursor in db.memRam.find({}):
        archEscritura.write(str(cursor) + " FIN \n")

    archEscritura.close()
    archLectura = open('ram.txt', 'r')
    obtener = archLectura.read()
    archLectura.close()
    return obtener


@app.route('/api/web-bot/desaprender', methods=['DELETE'])
def borra():
    in_args = request.args
    ident = in_args['id']

    db.memRam.remove(ObjectId(ident))
    #db.memRam.remove(ObjectId(exit(ident)))

    resp = Response('Eliminado', status=200, content_type='application/json')

    # accion = "Desaprender "+ str(ObjectId())
    # guardar(accion)

    return resp

def guardar(accion):
    fecha = time.strftime("%c")  # Obtener fecha y hora en que se realizó la accion
    usuario = socket.gethostname()  # Obtener nombre de la máquina de usuario

    guardarLog = {"Accion": accion, "por: ": usuario, "fecha: ": fecha}  # Datos a guardar en log
    log.insert(guardarLog)  # Insertar datos de historial en el LOG


if __name__ == '__main__':
    app.run()


# {"tipo":"A","operacion":"suma","numeros": [1,2,3]}
# {"tipo":"B","operacion":"resta","num1": 8, "num2": 2}

# {"code": "@app.route('/api/web-bot/aprender/cocina', methods=['POST']) \ndef cocinar(): \t\n nombreReceta = request.json['nombreReceta'] \t\n ingredientes = request.json['ingredientes'] \t\n preparacion = request.json['preparacion'] \t\n resultado = '¡Acabo de aprender la receta: ' + nombreReceta +'! Para prepararla se necesita ' + ingredientes +'. Se debe '+ preparacion \t\n js = json.dumps(resultado) \t\n resp = Response(js, status=200, content_type='application/json') \t\n return resp","action":"cocina"}
# {"code":"@app.route('/api/web-bot/aprender/baile', methods=['POST'])\ndef bailar(): \t\n ritmo = request.json['ritmo'] \t\n paso1 = request.json['paso1'] \t\n paso2 = request.json['paso2'] \t\n resultado = '¡Acabo de aprender: ' + ritmo +'! Primero debes' + paso1 +', y luego '+ paso2 \t\n js = json.dumps(resultado) \t\n resp = Response(js, status=200, content_type='application/json')\t\n return resp","action":"bailar"}
