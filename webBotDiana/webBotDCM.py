# Módulos necesarios para el desarrollo
from bson.objectid import ObjectId
from flask import Flask, request, json, Response
import time
from pymongo import MongoClient
import socket
from RAMBOT import RAM
from quickstart import main

# Inicialización de Flask
app = Flask(__name__)  # Instancia de Flask

conexionMongo = MongoClient('127.0.0.1', 27017)  # Conectar con MongoDB (localhost, puerto)

baseDatos = conexionMongo.WebBotDB  # Definir Base de datos
log = baseDatos.LOG  # Dentro de WebBotDB, crear la colección lOG
ram = baseDatos.RAM  # Dentro de WebBotDB, crear la colección RAM


# (con botón solo debe correr una vez)
@app.route('/api/web-bot/<name>', methods=['GET'])
def informacionGeneral(name):  # Muestra "datos personales" del web-bot

    fechaNac = time.strftime("%c")  # módulo time importado para tomar fecha y hora del equipo
    valorParaId = hash(fechaNac)  # Generar hash a partir de la fecha
    bot_id = abs(valorParaId)  # Valor absoluto del hash anterior asignado como ID del bot
    creadora = "DianaCM"

    return "¡Hola, mi nombres es " + name + "! Soy un web-bot... " \
           + "Acabo de nacer (" + fechaNac + \
           "), y me han asignado el id: " + str(bot_id) + \
           ". Mi creadora es: " + creadora


@app.route('/api/web-bot/default', methods=['POST'])  # Ruta para lo que el bot sabe hacer
def default():  # Lo que el bot hace por defecto desde que inicia

    tipoOperacion = request.json["tipo"]  # Seleccionar en el Json lo que contiene la clave tipo
    # Tipo A es para sumas y multiplicaciones, B para restas y divisiones

    operacion = request.json['operacion']  # Seleccionar en el Json lo que contiene la clave operación

    # Tipo "A" es para operaciones con más de dos números (sumas y multiplicaciones)
    if (tipoOperacion == "A"):
        numeros = request.json['numeros']  # Seleccionar en el Json lo que contiene la clave numeros
        if (operacion == "suma"):  # Si la operación es suma, ingresa al método de suma
            total = suma(numeros)
        if (operacion == "multiplica"):  # Si la operación es suma, ingresa al método de multiplica
            total = multiplica(numeros)

    # Tipo "B" es para operaciones  de dos números (restas y divisiones)
    if (tipoOperacion == "B"):
        num1 = request.json['num1']  # Seleccionar en el Json lo que contiene la clave num1
        num2 = request.json['num2']  # Seleccionar en el Json lo que contiene la clave num2
        if (operacion == "resta"):  # Si la operación es suma, ingresa al método de resta
            total = resta(num1, num2)
        if (operacion == "divide"):  # Si la operación es suma, ingresa al método de divide
            total = divide(num1, num2)

    operacion = {"Resultado ": total}  # Resultado

    codificarJson = json.dumps(operacion)  # Codificar Json
    resp = Response(codificarJson, content_type='application/json')

    accion = "Operacion Default"  # Acción que se almacenará en log
    guardar(accion)  # Va a método para  guardar en Log

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
    try:
        rest = num1 - num2
        return rest
    except:
        return "Imposible resolver"


def divide(num1, num2):  # Método para dividir dos numeros recibidos anteriormente
    try:
        div = num1 / num2
        return div
    except:
        return "Imposible resolver"


@app.route('/api/web-bot/aprender', methods=['POST'])
def aprende():
    action = request.json["action"]  # Seleccionar en el Json lo que contiene la clave action
    codigo = request.json["code"]  # Seleccionar en el Json lo que contiene la clave code

    resultado = {'He aprendido a ': action}  # Respuesta Json
    codifica = json.dumps(resultado)  # Codificar resultado para respuesta

    resp = Response(codifica, status=200, content_type='application/json')  # Configuración de la respuesta
    resp.headers['Link'] = "www.GrootBot.com"

    accion = ("Aprender " + action)  # Acción que será guardada en log
    guardar(accion)  # Ir al método guardar para almacenar la información en historial

    # Lista de Objetos (contendrá códigos a ejecutar)
    accionGuardar = [
        RAM(codigo)
    ]

    for insertar in accionGuardar:  # Ciclo para ir insertando los objetos a la coleccion RAM
        ram.insert(insertar.toRAM())
        exec(codigo)  # Ejecutar código recibido

    return resp


@app.route('/api/web-bot/calendario', methods=['GET'])
def calendarioGoogle():
    exec(str(main())) # Ejecutar quickstart (código de Google)

    archLectura = open('events.txt', 'r')  # Abrir archivo .txt para leer
    obtener = archLectura.read()  # Leer
    archLectura.close()  # Cerrarlo

    accion = "Uso de API "  # Acción que se almacenará en log
    guardar(accion)

    return obtener


@app.route('/api/web-bot/mostrar/estados')
def muestra_estados():  # Método para mostrar historial

    accion = "Mostrar estados (LOG)"  # Acción que se almacenará en log
    guardar(accion)

    archEscritura = open('log.txt', 'w')  # Abrir archivo .txt para escribir
    for cursor in log.find({}):  # Recorrer lo que hay en log
        archEscritura.write(str(cursor) + " FIN \n")  # Se escriben todos los datos del log en un archivo txt

    archEscritura.close()  # Cerrar archivo
    archLectura = open('log.txt', 'r')  # Abrir archivo .txt para leer
    obtener = archLectura.read()  # Leer
    archLectura.close()  # Cerrarlo

    # Como respuesta a petición, se envía lo leído en el .txt
    return obtener


@app.route('/api/web-bot/mostrar/conocimientos')
def muestra_memoria():  # Método para mostrar lo que hay en RAM

    accion = "Mostrar conocimientos (RAM)"  # Acción que se almacenará en log
    guardar(accion)

    archEscritura = open('ram.txt', 'w')  # Abrir archivo .txt para escribir
    for cursor in baseDatos.RAM.find({}):  # Recorrer lo que hay en ram
        archEscritura.write(str(cursor) + " FIN \n")  # Se escriben todos los datos del log en un archivo txt

    archEscritura.close()  # Cerrar archivo
    archLectura = open('ram.txt', 'r')  # Abrir archivo .txt para leer
    obtener = archLectura.read()
    archLectura.close()

    # Como respuesta a petición, se envía lo leído en el .txt
    return obtener


@app.route('/api/web-bot/olvidar', methods=['POST'])
def borra():
    in_args = request.args # Obtener los parámetros
    ident = in_args['id'] # Seleccionar el parámetro que contenga la clave ID

    baseDatos.RAM.remove(ObjectId(ident))  # Borrar con remove el documento con el ID recibido (es un Object_Id)

    resp = Response('Eliminado', status=200, content_type='application/json') # Respuesta

    accion = "Desaprender " + str(ObjectId())  # Acción que se almacenará en log
    guardar(accion)

    return resp


def guardar(accion):  # Método para guardar en log
    fecha = time.strftime("%c")  # Obtener fecha y hora en que se realizó la accion
    usuario = socket.gethostname()  # Obtener nombre de la máquina de usuario

    guardarLog = {"Accion": accion, "por: ": usuario, "fecha: ": fecha}  # Datos a guardar en log
    log.insert(guardarLog)  # Insertar datos de historial en el LOG


# Manejo de errores Flask
@app.errorhandler(404)
def page_not_found(error):
    return 'No es posible resolver la petición, revise el URL', 404


@app.errorhandler(500)
def special_exception_handler(error):
    return 'No es posible resolver la petición', 500


if __name__ == '__main__':
    app.run(port=8000, host='0.0.0.0')


#Para Postman (Ejemplos)
# {"tipo":"A","operacion":"suma","numeros": [1,2,3]}
# {"tipo":"B","operacion":"resta","num1": 8, "num2": 2}

# {"code": "@app.route('/api/web-bot/aprender/cocina', methods=['POST']) \ndef cocinar(): \t\n nombreReceta = request.json['nombreReceta'] \t\n ingredientes = request.json['ingredientes'] \t\n preparacion = request.json['preparacion'] \t\n resultado = '¡Acabo de aprender la receta: ' + nombreReceta +'! Para prepararla se necesita ' + ingredientes +'. Se debe '+ preparacion \t\n js = json.dumps(resultado) \t\n resp = Response(js, status=200, content_type='application/json') \t\n return resp","action":"cocina"}
# {"code":"@app.route('/api/web-bot/aprender/baile', methods=['POST'])\ndef bailar(): \t\n ritmo = request.json['ritmo'] \t\n paso1 = request.json['paso1'] \t\n paso2 = request.json['paso2'] \t\n resultado = '¡Acabo de aprender: ' + ritmo +'! Primero debes' + paso1 +', y luego '+ paso2 \t\n js = json.dumps(resultado) \t\n resp = Response(js, status=200, content_type='application/json')\t\n return resp","action":"bailar"}
