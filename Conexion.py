import mysql.connector
from mysql.connector import Error


class Conexion:
    def __init__(self):
        self.host = 'b4nquzfgjjuoijifrl0i-mysql.services.clever-cloud.com'
        self.user = 'uiwu07bati059kej'
        self.password = 'n9CBMVNdnB3t05XDpm0k'
        self.database = 'b4nquzfgjjuoijifrl0i'
        self.connection = None
        self.cursor = None

    def conectar(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print('Conexión exitosa!')
                self.cursor = self.connection.cursor()
        except Error as e:
            print('Error al conectarse con MySQL', e)

    def insertar_dato_canal(self, nombre):
        if self.connection.is_connected():
            query = f"""INSERT INTO Canal(`nombre`) 
            VALUES (%s)"""
            datos = (nombre,)
            self.cursor.execute(query, datos)
            self.connection.commit()
            print('Se han insertado los datos del canal!')

    def insertar_dato_historial_canal(self, suscriptores, videos, vistas, fecha_consulta, id_canal):
        if self.connection.is_connected():
            query = f"""INSERT INTO HistorialCanal(`suscriptores`, `videos`, `vistas`, `fechaConsulta`, 
            `Canal_idCanal`) 
            VALUES (%s, %s, %s, %s, %s)"""
            datos = (suscriptores, videos, vistas, fecha_consulta, id_canal)
            self.cursor.execute(query, datos)
            self.connection.commit()
            print('Se han insertado los datos del Historial del canal!')

    def insertar_dato_video(self, nombre, duracion, fecha, id_canal):
        if self.connection.is_connected():
            query = f"""INSERT INTO Video(`nombre`, `duracion`, `fecha`, `Canal_idCanal`) 
            VALUES (%s, %s, %s, %s)"""
            datos = (nombre, duracion, fecha, id_canal)
            self.cursor.execute(query, datos)
            self.connection.commit()
            print('Se han insertado los datos del video!')

    def insertar_dato_historial_video(self, vistas, likes, fecha_consulta, id_video):
        if self.connection.is_connected():
            query = f"""INSERT INTO HistorialVideo(`vistas`, `likes`, `fechaConsulta`, `Video_idVideo`) 
            VALUES (%s, %s, %s, %s)"""
            datos = (vistas, likes, fecha_consulta, id_video)
            self.cursor.execute(query, datos)
            self.connection.commit()
            print('Se han insertado los datos del Historial del video!')

    def insertar_dato_comentario(self, autor, likes, texto, id_video):
        if self.connection.is_connected():
            query = f"""INSERT INTO Comentario(`autor`, `likes`, `texto`, `Video_idVideo`) 
            VALUES (%s, %s, %s, %s)"""
            datos = (autor, likes, texto, id_video)
            self.cursor.execute(query, datos)
            self.connection.commit()
            print('Se han insertado los datos del comentario!')

    def obtener_canal_id(self, nombre: str):
        id_canal = 0
        if self.connection.is_connected():
            query = """SELECT idCanal from Canal 
            where nombre = %s"""
            self.cursor.execute(query, (nombre,))
            row = self.cursor.fetchall()  # Para evitar errores se toman todos los canales con el mismo nombre
            if row is None:
                id_canal = 0
            else:
                id_canal = row[0][0]  # Solo se toma el primero
        return id_canal

    def obtener_video_id(self, nombre: str):
        id_video = -1
        if self.connection.is_connected():
            query = """SELECT idVideo from Video
            where nombre = %s"""
            self.cursor.execute(query, (nombre,))
            row = self.cursor.fetchall()  # Misma idea que el canal
            if row is None:
                id_video = 0
            else:
                id_video = row[0][0]
        return id_video

    def desconectar(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print('\nSesión cerrada')
