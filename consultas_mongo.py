from mongo import Mongo
from pprint import pprint
dbMongo = Mongo()
canal = dbMongo.canal
video = dbMongo.video

# Historial de un canal en específico
nombre_canal = 'Juguetes y Colores'
print('Historial canal en especifico')
pprint(list(canal.find({"nombre": nombre_canal}, {"nombre": 1, "historial": 1, "_id": 0})))

# Historial de un vídeo en específico
nombre_video = 'Alex Aprende Trabajar Con SALÓN PELUQUERÍA JUGUETE Para Niños'
print('Historial de un vídeo especifico')
pprint(list(video.find({"nombre": nombre_video}, {"nombre": 1, "historial": 1, "_id": 0})))

# Historial de los videos de un canal
print('Historial de los videos de un canal')
id_canal = canal.find_one({"nombre": nombre_canal}, {"_id": 1})
pprint(list(video.find({"canal": id_canal}, {"nombre": 1, "historial": 1, "_id": 0})))

# Comentarios de los vídeos de un canal
print('Comentarios de vídeos de un canal')
id_canal = canal.find_one({"nombre": "Spreen"}, {"_id": 1})
pprint(list(video.find({"canal": id_canal}, {"nombre": 1, "comentarios": 1, "_id": 0, "canal": 1})))
