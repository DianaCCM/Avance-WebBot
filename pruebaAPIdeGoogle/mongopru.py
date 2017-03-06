from flask import Flask, request, jsonify, json, Response
import time
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

try:
    con = MongoClient('127.0.0.1', 27017)
    print("Conectada")

except ConnectionFailure as e:
    sys.stderr.write("No podemos conectarnos: %s" % e)
    sys.exit(1)

con.drop_database('historial')
db = con.historial
log = db.coleccion
print(con.database_names())


db = con.memoria
ram = db.coleccion

log:{
        "usuario": ObjectId,
        "fecha": time.strftime("%c"),
        "accion": "code"
    }


@app.route('/api/web-bot/aprender', methods=['POST'])
def aprende():
    codigo = request.json["code"]
    resultado = {"Resultado: ": codigo}
    js = json.dumps(resultado)
    decoded = json.loads(js)

    log.insert(decoded)

    resp = Response(decoded, status=200, content_type='application/json')
    resp.headers['Link'] = "www.mi-web-bot.com"

    print(con.database_names())

    return resp


@app.route('/api/web-bot/mostrar/estados')
def muestra_estados():
    #Muestra historial que está en bd
    #Esto es aparte de la matriz GET
    return


@app.route('/api/web-bot/mostrar/memoria')
def muestra_memoria():
    #Extaer y mostrar datos de la matriz GET
    return

@app.route('/api/web-bot/mostrar/desaprender', methods=['DELETE'])
def borra():
    Obj_id = request.json["id"]
    resultado = {"Eliminado: ": Obj_id}
    js = json.dumps(resultado)
    decoded = json.loads(js)

    ram.remove(decoded)

    resp = Response(decoded, status=200, content_type='application/json')
    resp.headers['Link'] = "www.mi-web-bot.com"

    print(con.database_names())

    return resp

    collect.remove()
    return


if __name__ == '__main__':
    app.run()


#jsons:
    #sabe
# {"tipo":"x","operacion":"suma","numeros": [1,2,3]}
# {"tipo":"y","operacion":"resta","num1": 8, "num2": 2}