#--------------------------------------------------------------------
# Instalar con pip install Flask
from flask import Flask, request, jsonify, render_template
from flask import request

# Instalar con pip install flask-cors
from flask_cors import CORS

# Instalar con pip install mysql-connector-python
import mysql.connector

# Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename

# No es necesario instalar, es parte del sistema standard de Python
import os
import time
#--------------------------------------------------------------------



app = Flask(__name__)
CORS(app)  # Esto habilitará CORS para todas las rutas

#--------------------------------------------------------------------
class Catalogo:
    #----------------------------------------------------------------
    # Constructor de la clase
    def __init__(self, host, user, password, database):
        # Primero, establecemos una conexión sin especificar la base de datos
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()

        # Intentamos seleccionar la base de datos
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            # Si la base de datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err

        # Una vez que la base de datos está establecida, creamos la tabla si no existe
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            edad INT NOT NULL,
            rango DECIMAL(10, 2) NOT NULL,
            imagen_url VARCHAR(255),
            pais INT(4))''')
        self.conn.commit()

        # Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)
        
    #----------------------------------------------------------------
    def agregar_usuario(self, nombre, edad, rango, imagen, pais):
               
        sql = "INSERT INTO usuarios (nombre, edad, rango, imagen_url, pais) VALUES (%s, %s, %s, %s, %s)"
        valores = (nombre, edad, rango, imagen, pais)

        self.cursor.execute(sql, valores)        
        self.conn.commit()
        return self.cursor.lastrowid

    #----------------------------------------------------------------
    def consultar_usuarios(self, id):
        # Consultamos un usuario a partir de su código
        self.cursor.execute(f"SELECT * FROM usuarios WHERE id = {id}")
        return self.cursor.fetchone()

    #----------------------------------------------------------------
    def modificar_usuario(self, id, nueva_nombre, nueva_edad, nuevo_rango, nueva_imagen, nuevo_pais):
        sql = "UPDATE usuarios SET nombre = %s, edad = %s, rango = %s, imagen_url = %s, pais = %s WHERE id = %s"
        valores = (nueva_nombre, nueva_cantidad, nuevo_rango, nueva_imagen, nuevo_pais, id)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0

    #----------------------------------------------------------------
    def listar_usuarios(self):
        self.cursor.execute("SELECT * FROM usuarios")
        usuarios = self.cursor.fetchall()
        return usuarios

    #----------------------------------------------------------------
    def eliminar_usuario(self, id):
        # Eliminamos un usuario de la tabla a partir de su código
        self.cursor.execute(f"DELETE FROM usuarios WHERE id = {id}")
        self.conn.commit()
        return self.cursor.rowcount > 0

    #----------------------------------------------------------------
    def mostrar_usuario(self, id):
        # Mostramos los datos de un usuario a partir de su código
        usuario = self.consultar_usuarios(id)
        if usuario:
            print("-" * 40)
            print(f"id.....: {usuario['id']}")
            print(f"nombre: {usuario['nombre']}")
            print(f"edad...: {usuario['edad']}")
            print(f"rango.....: {usuario['rango']}")
            print(f"Imagen.....: {usuario['imagen_url']}")
            print(f"pais..: {usuario['pais']}")
            print("-" * 40)
        else:
            print("usuario no encontrado.")


#--------------------------------------------------------------------
# Cuerpo del programa
#--------------------------------------------------------------------
# Crear una instancia de la clase Catalogo
catalogo = Catalogo(host='localhost', user='root', password='luisillo', database='hunters')
#catalogo = Catalogo(host='USUARIO.mysql.pythonanywhere-services.com', user='USUARIO', password='CLAVE', database='USUARIO$miapp')


# Carpeta para guardar las imagenes.
RUTA_DESTINO = './static/imagenes/'

#Al subir al servidor, deberá utilizarse la siguiente ruta. USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
#RUTA_DESTINO = '/home/USUARIO/mysite/static/imagenes'


#--------------------------------------------------------------------
# Listar todos los usuarios
#--------------------------------------------------------------------
#La ruta Flask /usuarios con el método HTTP GET está diseñada para proporcionar los detalles de todos los usuarios almacenados en la base de datos.
#El método devuelve una lista con todos los usuarios en formato JSON.
@app.route("/usuarios", methods=["GET"])
def listar_usuarios():
    usuarios = catalogo.listar_usuarios()
    return jsonify(usuarios)


#--------------------------------------------------------------------
# Mostrar un sólo usuario según su código
#--------------------------------------------------------------------
#La ruta Flask /usuarios/<int:codigo> con el método HTTP GET está diseñada para proporcionar los detalles de un usuario específico basado en su código.
#El método busca en la base de datos el usuario con el código especificado y devuelve un JSON con los detalles del usuario si lo encuentra, o None si no lo encuentra.
@app.route("/usuarios/<int:id>", methods=["GET"])
def mostrar_usuario(id):
    usuario = catalogo.consultar_usuarios(id)
    if usuario:
        return jsonify(usuario), 201
    else:
        return "Usuario no encontrado", 404


#--------------------------------------------------------------------
# Agregar un usuario
#--------------------------------------------------------------------
@app.route("/usuarios", methods=["POST"])
#La ruta Flask `/usuarios` con el método HTTP POST está diseñada para permitir la adición de un nuevo usuario a la base de datos.
#La función agregar_usuario se asocia con esta URL y es llamada cuando se hace una solicitud POST a /usuarios.
def agregar_usuario():
    #Recojo los datos del form
    nombre = request.form['nombre']
    edad = request.form['edad']
    rango = request.form['rango']
    imagen = request.files['imagenUsuario']
    pais = request.form['Pais']  
    nombre_imagen=""

    
    # Genero el nombre de la imagen
    nombre_imagen = secure_filename(imagen.filename) #Chequea el nombre del archivo de la imagen, asegurándose de que sea seguro para guardar en el sistema de archivos
    nombre_base, extension = os.path.splitext(nombre_imagen) #Separa el nombre del archivo de su extensión.
    nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}" #Genera un nuevo nombre para la imagen usando un timestamp, para evitar sobreescrituras y conflictos de nombres.

    nuevo_id = catalogo.agregar_usuario(nombre, edad, rango, nombre_imagen, pais)
    if nuevo_id:    
        imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))

        #Si el usuario se agrega con éxito, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 201 (Creado).
        return jsonify({"mensaje": "Usuario agregado correctamente.", "id": nuevo_id, "imagen": nombre_imagen}), 201
    else:
        #Si el usuario no se puede agregar, se devuelve una respuesta JSON con un mensaje de error y un código de estado HTTP 500 (Internal Server Error).
        return jsonify({"mensaje": "Error al agregar al usuario."}), 500
    

#--------------------------------------------------------------------
# Modificar un usuario según su código
#--------------------------------------------------------------------
@app.route("/usuarios/<int:id>", methods=["PUT"])
#La ruta Flask /usuarios/<int:codigo> con el método HTTP PUT está diseñada para actualizar la información de un usuario existente en la base de datos, identificado por su código.
#La función modificar_usuario se asocia con esta URL y es invocada cuando se realiza una solicitud PUT a /usuarios/ seguido de un número (el código del usuario).
def modificar_usuario(id):
    #Se recuperan los nuevos datos del formulario
    nueva_nombre = request.form.get("nombre")
    nueva_edad = request.form.get("edad")
    nuevo_rango = request.form.get("rango")
    nuevo_pais = request.form.get("pais")
    
    
    # Verifica si se proporcionó una nueva imagen
    if 'imagen' in request.files:
        imagen = request.files['imagen']
        # Procesamiento de la imagen
        nombre_imagen = secure_filename(imagen.filename) #Chequea el nombre del archivo de la imagen, asegurándose de que sea seguro para guardar en el sistema de archivos
        nombre_base, extension = os.path.splitext(nombre_imagen) #Separa el nombre del archivo de su extensión.
        nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}" #Genera un nuevo nombre para la imagen usando un timestamp, para evitar sobreescrituras y conflictos de nombres.

        # Guardar la imagen en el servidor
        imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))
        
        # Busco el usuario guardado
        usuario = catalogo.consultar_usuario(id)
        if usuario: # Si existe el usuario...
            imagen_vieja = usuario["imagen_url"]
            # Armo la ruta a la imagen
            ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)

            # Y si existe la borro.
            if os.path.exists(ruta_imagen):
                os.remove(ruta_imagen)
    
    else:
        # Si no se proporciona una nueva imagen, simplemente usa la imagen existente del usuario
        usuario = catalogo.consultar_usuarios(id)
        if usuario:
            nombre_imagen = usuario["imagen_url"]


    # Se llama al método modificar_usuario pasando el codigo del usuario y los nuevos datos.
    if catalogo.modificar_usuario(id, nueva_nombre, nueva_edad, nuevo_rango, nombre_imagen, nuevo_pais):
        
        #Si la actualización es exitosa, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 200 (OK).
        return jsonify({"mensaje": "datos modificados"}), 200
    else:
        #Si el usuario no se encuentra (por ejemplo, si no hay ningún usuario con el código dado), se devuelve un mensaje de error con un código de estado HTTP 404 (No Encontrado).
        return jsonify({"mensaje": "usuario no encontrado"}), 404



#--------------------------------------------------------------------
# Eliminar un usuario según su código
#--------------------------------------------------------------------
@app.route("/usuarios/<int:id>", methods=["DELETE"])
#La ruta Flask /usuarios/<int:codigo> con el método HTTP DELETE está diseñada para eliminar un usuario específico de la base de datos, utilizando su código como identificador.
#La función eliminar_usuario se asocia con esta URL y es llamada cuando se realiza una solicitud DELETE a /usuarios/ seguido de un número (el código del usuario).
def eliminar_usuario(id):
    # Busco el usuario en la base de datos
    usuario = catalogo.consultar_usuarios(id)
    if usuario: # Si el usuario existe, verifica si hay una imagen asociada en el servidor.
        imagen_vieja = usuario["imagen_url"]
        # Armo la ruta a la imagen
        ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)

        # Y si existe, la elimina del sistema de archivos.
        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)

        # Luego, elimina el usuario del catálogo
        if catalogo.eliminar_usuario(id):
            #Si el usuario se elimina correctamente, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 200 (OK).
            return jsonify({"mensaje": "Usuario eliminado"}), 200
        else:
            #Si ocurre un error durante la eliminación (por ejemplo, si el usuario no se puede eliminar de la base de datos por alguna razón), se devuelve un mensaje de error con un código de estado HTTP 500 (Error Interno del Servidor).
            return jsonify({"mensaje": "Error al eliminar al usuario"}), 500
    else:
        #Si el usuario no se encuentra (por ejemplo, si no existe un usuario con el codigo proporcionado), se devuelve un mensaje de error con un código de estado HTTP 404 (No Encontrado). 
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

#--------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)