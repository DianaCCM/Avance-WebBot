from flask import Flask, request, jsonify, json, Response
import time
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

@app.route('/api/web-bot/aprender/baile', methods=['POST'])
def bailar():
    ritmo = request.json['ritmo']
    paso1 = request.json['paso1']
    paso2 = request.json['paso2']
    resultado = '¡Acabo de aprender: ' + ritmo +'! Primero debes' + paso1 +', y luego '+ paso2
    js = json.dumps(resultado)
    resp = Response(js, status=200, content_type='application/json')
    return resp



import gdata.youtube
import gdata.youtube.service

def informacionDeVideo(video):  # Si se le suministra un objeto video mostrara por pantalla cierta informacion de este
    nombreVideo = video.media.title.text

youtubeService = gdata.youtube.service.YouTubeService() # Se inicializa el objeto YouTubeService
feedDeVideos = youtubeService.GetMostViewedVideoFeed() # Se obtiene el feed de los videos mas vistos
for video in  feedDeVideos.entry: # Para cada video dentro del feed ...
  informacionDeVideo(video)


if __name__ == '__main__':
    app.run()

#{"ritmo":"cumbia","paso1":"levantar el brazo", "paso2":"brincar"}