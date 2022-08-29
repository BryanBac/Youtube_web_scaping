from pymongo import MongoClient
from typing import List


class Mongo:
    def __init__(self):
        self.client = MongoClient(
            "mongodb+srv://Diego:HolaMundo@cluster0.m8f238i.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client.get_database('Proyecto')
        self.canal = self.db.Canal
        self.video = self.db.Video

    def insertar_canal(self, nombre: str, suscriptores: int, videos: int, vistas: int):
        nuevo_canal = {
            "nombre": nombre,
            "suscriptores": suscriptores,
            "videos": videos,
            "vistas": vistas
        }
        self.canal.insert_one(nuevo_canal)
        # Una vez insertado el canal, se obtiene el id que Mongo le genera, para poder colocarlo como el valor del
        # campo id_canal en la colección vídeo, al momento de ingresar los vídeos pertenecientes al canal
        return self.canal.find_one({"nombre": nombre}, {"_id": 1})

    def insertar_video(self, nombre: str, vistas: int, duracion: float, likes: int, fecha: str, id_canal: str,
                       comentarios: List):
        nuevo_video = {
            "nombre": nombre,
            "vistas": vistas,
            "duracion": duracion,
            "likes": likes,
            "fecha": fecha,
            "canal": id_canal,
            "comentarios": comentarios
        }
        self.video.insert_one(nuevo_video)
        print("Insertado")
