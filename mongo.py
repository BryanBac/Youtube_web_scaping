from pymongo import MongoClient
from typing import List
from datetime import datetime


class Mongo:
    def __init__(self):
        self.client = MongoClient(
            "mongodb+srv://Bryan:traceon@cluster0.m8f238i.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client.get_database('Proyecto')
        self.canal = self.db.Canal
        self.video = self.db.Video

    def insertar_canal(self, nombre: str, suscriptores: int, videos: int, vistas: int):
        if self.canal.count_documents({"nombre": nombre}):
            # Si ya existe el canal, solo se agregan los datos en el historial sobre los cambios en la cantidad de
            # suscriptores, videos y vistas
            Historial_Nuevo = {
                "suscriptores": suscriptores,
                "videos": videos,
                "vistas": vistas,
                "fecha_hora": datetime.today().now()
            }
            self.canal.update_one({"nombre": nombre}, {'$push': {"historial": Historial_Nuevo}})
        else:
            # En caso de que no exista el canal, se agrega a la colección
            nuevo_canal = {
                "nombre": nombre,
                "historial": [
                    {
                        "suscriptores": suscriptores,
                        "videos": videos,
                        "vistas": vistas,
                        "fecha_hora": datetime.today().now()
                    }
                ]
            }
            self.canal.insert_one(nuevo_canal)
        # Una vez insertado el canal, se obtiene el id que Mongo le genera, para poder colocarlo como el valor del
        # campo id_canal en la colección vídeo, al momento de ingresar los vídeos pertenecientes al canal
        return self.canal.find_one({"nombre": nombre}, {"_id": 1})

    def insertar_video(self, nombre: str, vistas: int, duracion: float, likes: int, fecha: str, id_canal: str,
                       comentarios: List):
        if self.video.count_documents({"nombre": nombre}):
            # Si el vídeo ya existe, se agregan los datos de los cambios en likes y vistas
            Historial_Nuevo = {
                "likes": likes,
                "vistas": vistas,
                "fecha_hora": datetime.today().now()
            }
            self.video.update_one({"nombre": nombre}, {'$push': {"historial": Historial_Nuevo}})
        else:
            nuevo_video = {
                "nombre": nombre,
                "duracion": duracion,
                "fecha": datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S'),
                "canal": id_canal,
                "comentarios": comentarios,
                "historial": [
                    {
                        "likes": likes,
                        "vistas": vistas,
                        "fecha_hora": datetime.today().now()
                    }
                ]
            }
            self.video.insert_one(nuevo_video)
