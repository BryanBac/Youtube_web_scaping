from en_videos import get_channel_stats, get_videos_ids, \
    get_videos_details, get_comments, get_user_channel_stats
from googleapiclient.discovery import build
import pprint
from Conexion import Conexion
from cleantext import clean
from mongo import Mongo
from typing import List


dbmongo = Mongo()

data_index = open("api_index.txt", 'r')
data_petición = open("numero_petición.txt", "r")
index = int(data_index.read())
petición = int(data_petición.read())
data_index.close()
data_petición.close()
data_index = open("api_index.txt", 'w')
data_petición = open("numero_petición.txt", "w")

print("------Inicio------")
print(f"{type(index)}---{index}")
print(f"{type(petición)}---{petición}")
petición -= 1
if petición == 0:
    index += 1
    petición = 2
    if index == 20:  # 20
        index = 0
data_index.write(str(index))
data_petición.write(str(petición))

api_key = ["AIzaSyAas7rC594WDvAwKaXpFgaTCv_-mbTJAUo",
           "AIzaSyCtzFyZRlwHUO6uiJlKeYEgH7ZSrJVZcPg",
           "AIzaSyAOdZEHfQCFm_-lNS24IYUK1coXWzfdPsI"]
channel_ids = ["UCWDksMO8R0Mew4B89GhO9dA",
               "UCoSrY_IQQVpmIRZ9Xf-y93g",
               "UC3n5uGu18FoCy23ggWWp8tA",
               "UC5CwaMl1eIgY8h02uZw7u8A",
               "UCI7ktPB6toqucpkkCiolwLg",
               "UCaBTm46K3l59CIty88Q_jog",
               "UC1DCedRgGHBdm81E1llLhOQ",
               "UCgTOIiEgjm58xLjHvDjmgdA",
               "UCmDfpsIMjCw9bMrwa8dIsTw"
               ]
user_channel_ids = ["MissaSinfonia"]


#  aquí deberá ir el index así api_key[index] una vez tengamos todas apis
youtube = build("youtube", "v3", developerKey=api_key[index])


#  main()
all_data = get_channel_stats(youtube, channel_ids)
all_user_data = get_user_channel_stats(youtube, user_channel_ids)

videos = []
videos_details = []
comentarios = []
# Base de Datos Relacional
conexion = Conexion()
nombre_canal = None
suscriptores = None
total_videos = None
vistas_canal = None
id_canal = None
id_video = None
nombre_video = None
vistas_video = None
duracion = None
likes_video = None
fecha = None
autor = None
likes_comentario = None
texto = None
conexion.conectar()

for i in range(len(all_data)):
    pprint.pprint(all_data[i])
    videos = get_videos_ids(youtube, all_data[i]["playlist_id"])
    videos_details = get_videos_details(youtube, videos)
    pprint.pprint(videos_details)

    # ---------↓↓↓Almacenamiento de Datos↓↓↓---------
    # INFO DE CANAL PARA MANDAR A CONSULTA
    nombre_canal = all_data[i].get('Channel_name')
    nombre_canal = clean(nombre_canal, no_emoji=True, lower=False, to_ascii=False)  # Quita emojis
    suscriptores = all_data[i].get('Subscribers')
    total_videos = all_data[i].get('Total_videos')
    vistas_canal = all_data[i].get('Views')
    conexion.insertar_dato_canal(nombre_canal, suscriptores, total_videos, vistas_canal)
    id_canal = conexion.obtener_canal_id(nombre_canal)  # Obtiene el id para llave foranea

    # Insertar canal en MongoAtlas
    object_id_canal = dbmongo.insertar_canal(nombre_canal, int(suscriptores), int(total_videos), int(vistas_canal))

    # ---------↑↑↑Almacenamiento de Datos↑↑↑---------

    for j in range(len(videos)):
        print(f"Video {j}")

        # ---------↓↓↓Almacenamiento de Datos↓↓↓---------
        # INFO DE VIDEOS PARA MANDAR A CONSULTA
        nombre_video = videos_details[j].get('Title')
        nombre_video = clean(nombre_video, no_emoji=True, lower=False, to_ascii=False)  # Quita emojis
        vistas_video = videos_details[j].get('Views')
        duracion = videos_details[j].get('Duracion')
        likes_video = videos_details[j].get('Likes')
        fecha = videos_details[j].get('Published_date')
        fecha = fecha.replace('T', ' ')
        fecha = fecha.replace('Z', '')
        conexion.insertar_dato_video(nombre_video, vistas_video, duracion, likes_video, fecha, id_canal)
        id_video = conexion.obtener_video_id(nombre_video)  # Obtiene el id para llave foranea

        # ---------↑↑↑Almacenamiento de Datos↑↑↑---------

        comentarios.append(get_comments(youtube, videos[j]))
        pprint.pprint(comentarios[j])
        comentarios_data = comentarios[j]
        comentarios_Mongo: List = []
        # ---------↓↓↓Almacenamiento de Datos↓↓↓---------
        for k in range(len(comentarios_data)):
            # INFO DE VIDEOS PARA MANDAR A CONSULTA
            if comentarios_data[k] != 'El video tenía los comentarios deshabilitados':
                # Si se deshabilitaron no se almacenan los datos
                autor = comentarios_data[k].get('autor')
                autor = clean(autor, no_emoji=True, lower=False, to_ascii=False)  # Quita emojis
                likes_comentario = comentarios_data[k].get('likes')
                texto = comentarios_data[k].get('texto')
                if len(texto) > 500:
                    texto = texto[0:500]
                texto = clean(texto, no_emoji=True, lower=False, to_ascii=False)  # Quita emojis
                # conexion.insertar_dato_comentario(autor, likes_comentario, texto, id_video)
                nuevo_comentario = {
                    "autor": autor,
                    "texto": texto,
                    "likes": likes_comentario
                }
                print(f"{autor} {likes_comentario} {texto}")
                comentarios_Mongo.append(nuevo_comentario)
            # ---------↑↑↑Almacenamiento de Datos↑↑↑---------
        print(len(comentarios_Mongo))
        print(comentarios_Mongo)
        dbmongo.insertar_video(nombre_video, vistas_video, duracion, likes_video, fecha, object_id_canal,
                               comentarios_Mongo)
    #  all_data[i], videos_details[i], comentarios[i]
    print("\n\n\n----")
#  para este punto ya debería haberse guardado la info de los de arriba

videos = []
videos_details = []
comentarios = []

for i in range(len(all_user_data)):
    pprint.pprint(all_user_data[i])
    videos = get_videos_ids(youtube, all_user_data[i]["playlist_id"])
    videos_details = get_videos_details(youtube, videos)
    pprint.pprint(videos_details)

    # ---------↓↓↓Almacenamiento de Datos↓↓↓---------
    # INFO DE CANAL PARA MANDAR A CONSULTA
    nombre_canal = all_user_data[i].get('Channel_name')
    nombre_canal = clean(nombre_canal, no_emoji=True, lower=False, to_ascii=False)  # Quita emojis
    suscriptores = all_user_data[i].get('Subscribers')
    total_videos = all_user_data[i].get('Total_videos')
    vistas_canal = all_user_data[i].get('Views')
    conexion.insertar_dato_canal(nombre_canal, suscriptores, total_videos, vistas_canal)
    id_canal = conexion.obtener_canal_id(nombre_canal)  # Obtiene el id para llave foranea

    # Insertar canal en MongoAtlas
    object_id_canal = dbmongo.insertar_canal(nombre_canal, int(suscriptores), int(total_videos), int(vistas_canal))

    # ---------↑↑↑Almacenamiento de Datos↑↑↑---------

    for j in range(len(videos)):
        print(f"Video {j}")

        # ---------↓↓↓Almacenamiento de Datos↓↓↓---------
        # INFO DE VIDEOS PARA MANDAR A CONSULTA
        nombre_video = videos_details[j].get('Title')
        nombre_video = clean(nombre_video, no_emoji=True, lower=False, to_ascii=False)  # Quita emojis
        vistas_video = videos_details[j].get('Views')
        duracion = videos_details[j].get('Duracion')
        likes_video = videos_details[j].get('Likes')
        fecha = videos_details[j].get('Published_date')
        fecha = fecha.replace('T', ' ')
        fecha = fecha.replace('Z', '')
        conexion.insertar_dato_video(nombre_video, vistas_video, duracion, likes_video, fecha, id_canal)
        id_video = conexion.obtener_video_id(nombre_video)  # Obtiene el id para llave foranea

        # ---------↑↑↑Almacenamiento de Datos↑↑↑---------

        comentarios.append(get_comments(youtube, videos[j]))
        pprint.pprint(comentarios[j])
        comentarios_data = comentarios[j]
        comentarios_Mongo: List = []
        # ---------↓↓↓Almacenamiento de Datos↓↓↓---------
        for k in range(len(comentarios_data)):
            # INFO DE VIDEOS PARA MANDAR A CONSULTA
            if comentarios_data[k] != 'El video tenía los comentarios deshabilitados':
                # Si se deshabilitaron no se almacenan los datos
                autor = comentarios_data[k].get('autor')
                autor = clean(autor, no_emoji=True, lower=False, to_ascii=False)  # Quita emojis
                likes_comentario = comentarios_data[k].get('likes')
                texto = comentarios_data[k].get('texto')
                if len(texto) > 500:
                    texto = texto[0:500]
                texto = clean(texto, no_emoji=True, lower=False, to_ascii=False)  # Quita emojis
                # conexion.insertar_dato_comentario(autor, likes_comentario, texto, id_video)
                nuevo_comentario = {
                    "autor": autor,
                    "texto": texto,
                    "likes": likes_comentario
                }
                print(f"{autor} {likes_comentario} {texto}")
                comentarios_Mongo.append(nuevo_comentario)
            # ---------↑↑↑Almacenamiento de Datos↑↑↑---------
        print(len(comentarios_Mongo))
        print(comentarios_Mongo)
        dbmongo.insertar_video(nombre_video, vistas_video, duracion, likes_video, fecha, object_id_canal,
                               comentarios_Mongo)
    #  all_data[i], videos_details[i], comentarios[i]
    print("\n\n\n----")
#  para este punto ya debería haberse guardado la info de los de arriba

#  aquí se reescribiran los archivos
print("------Final------")
print(f"{type(index)}---{index}")
print(f"{type(petición)}---{petición}")
data_index.close()
data_petición.close()

conexion.desconectar()
