from flask import Flask, render_template, redirect, url_for
from flask import session, send_from_directory
from flask import request, make_response #make_response se usa la información de la solicitud HTTP
from flaskext.mysql import MySQL
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash #Para hashear y comprobar las contraseñas
import os

app = Flask(__name__)

app.secret_key = "chatpy"

mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'pychat'
mysql.init_app(app)#se inicializa el valor 
    

@app.route('/home')
def home ():
    if not 'login' in session:
        return  redirect('/')
    
    #make_response para crear una respuesta HTTP, se crea una respuesta que renderiza la plantilla de la página login.html usando render_template.
    response = make_response(render_template('paginas/index.html'))
    #Establece encabezados HTTP para controlar el almacenamiento en caché,La configuración 'no-store, no-cache, must-revalidate, max-age=0' indica al navegador que no debe almacenar en caché la página y que siempre debe solicitar la versión más reciente al servidor.
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
       
    return response


@app.route('/')
def homepage():
    if 'login' in session:
        return  redirect('/home')
    
    response = make_response(render_template('paginas/homepage.html'))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response


@app.route('/login')
def login():
    if 'login' in session:
        return  redirect('/home')
    
    response = make_response(render_template('paginas/login.html'))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'

    return response


#Aquí se verifica el logeo
@app.route('/login', methods = ['POST'])
def login_comprobar():
    _correo = request.form['login-correo']
    _password = request.form['login-password']


    if _correo and _password != '': 

        conexion = mysql.connect()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM `usuarios` WHERE correo = %s",(_correo)) 
        usuario = cursor.fetchone()
        conexion.commit()

        if usuario and check_password_hash(usuario[3], _password): #check nos devuelve valor True o False, verifica el hash con el que se guardo la contraseña, no la contraseña, si el hash coincide regresa True
            #Variables de session que vamos a utilizar
            session['login'] = True
            session['id'] = usuario[0]
            session['nombre'] = usuario[1]
            session['correo'] = usuario[2]
            session['imagen'] = usuario[4]
            print('Se inicia sesión con: ',session['login'],session['nombre'],session['correo'],session['imagen'])    
            return redirect('/home')
            
        else:
            return render_template('paginas/login.html', mensaje = 'Correo no encontrado')
    else:
        return render_template('paginas/login.html', mensaje = 'Insertar Todos los Datos*')


#Página de registro
@app.route('/registro')
def registro():
    if 'login' in session:
        return  redirect('/home')
    
    response = make_response(render_template('paginas/registro.html'))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'

    return response


#Ruta con función donde se hace el guardado de datos en la base de datos
@app.route('/registro', methods = ['POST'])
def registro_guardar():
    _nombre = request.form['registro-nombre']
    _correo = request.form['registro-correo']
    if request.form['registro-password'] != '':
        _password = generate_password_hash(request.form['registro-password'], method = 'scrypt')#Se hashea la contraseña recibida por el form
    else:
        _password = ''
    #Datos para guardar imagenes de registro
    _imagen = request.files['imagenUsuario']
    tiempo = datetime.now()
    hora_actual = tiempo.strftime('%Y%H%M%S')#formato year, hours, minutes, seconds

    _edad = request.form['registro-edad'] 
    edad = int(_edad)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `usuarios`") 
    usuarios_registrados = cursor.fetchall()
    conexion.commit()

    existe = False
    for usuario in usuarios_registrados:
        if _correo in usuario:
            existe = True


    if _nombre and _correo and _password and _imagen and _edad != '' and edad >= 18 and existe!= True :
    #Se crea la conexion para verificar si ya existe el correo de usuario dentro de la bd
        conexion1 = mysql.connect()
        cursor1 = conexion1.cursor()
        cursor1.execute("SELECT * FROM `usuarios`;")
        usuarios = cursor1.fetchall()
        conexion1.commit()
        for usuario in usuarios:
            if _correo in usuario[2]:
                return render_template('paginas/registro.html', mensaje = 'Correo de Usuario Registrado Anteriormente')
        #Codigo para guardar imagen con nuevo nombre 
        if _imagen.filename != '':
            nuevo_nombre_imagen = hora_actual + "_" + _imagen.filename
            _imagen.save('templates/paginas/img/' + nuevo_nombre_imagen)# se guarda el archivo en la carpeta de imagenes con el nuevo nombre
        #Creación de sql para guardar los datos en la bd
        sql = "INSERT INTO `usuarios` (`usuario_id`, `nombre`,`correo`,`password`, `imagen`, `edad`) VALUES (NULL, %s, %s, %s, %s, %s );"
        datos = (_nombre, _correo, _password, nuevo_nombre_imagen, edad ) #variables que tomaran el valor que irá a la BD

        conexion = mysql.connect()
        cursor = conexion.cursor()
        cursor.execute(sql, datos) #se ejecuta el cursor y se envia la consulta/insercion que deseamos hacer, con los datos dados
        conexion.commit()
        return redirect('/login')

    elif edad < 18 :
        return render_template('paginas/registro.html', mensaje = 'Debes ser mayor de edad para ingresar' )
    
    elif existe == True:
        return render_template('paginas/registro.html', mensaje = 'Correo Registrado anteriormente')
    
    else:
        return render_template('paginas/registro.html', mensaje = 'Completar todos los datos' )


@app.route('/salir')
def salir():
    if not 'login' in session:
        return  redirect('/')
    session.clear()
    return redirect('/')


#Ruta y funciones para tomar y presentar la información del usuario
@app.route('/perfil')
def perfil():
    if not 'login' in session:
        return  redirect('/home')
    
    conexion = mysql.connect()
    cursor = conexion.cursor() 
    cursor.execute("SELECT * FROM `contactos` WHERE `id_usuario` = %s", (session['id'])) 
    contactos_usuario = cursor.fetchall()
    conexion.commit()


    response = make_response(render_template('paginas/perfil.html',id = session['id'], nombre = session['nombre'], correo = session['correo'], imagen = session['imagen'], contactos = contactos_usuario))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'

    return response

@app.route('/img/<imagen>')#se crea una ruta que muestra imagenes 
def imagenes(imagen):#se toma como parametro la misma img que estará en el path
    print(imagen)
    return send_from_directory(os.path.join('templates/paginas/img/'), imagen)#se envia directamente de la carpeta que está en la ruta y se concatena con la imagen


@app.route('/perfil/borrar', methods = ["POST"])
def borrar_perfil():
    _id_borrar = request.form['perfil-borrar']

    conexion = mysql.connect()
    cursor = conexion.cursor() 
    cursor.execute("SELECT imagen FROM `usuarios` WHERE `usuario_id` = %s", (_id_borrar)) 
    _imagen_borrar = cursor.fetchall()
    conexion.commit()


    if os.path.exists("templates/paginas/img/" + str(_imagen_borrar[0][0])):#[0][0] está representando el valor de la primera columna de la primera fila en el resultado de la consulta SQL
        os.unlink("templates/paginas/img/" + str(_imagen_borrar[0][0]))

    conexion = mysql.connect()
    cursor = conexion.cursor() 
    cursor.execute("DELETE FROM usuarios WHERE `usuarios`.`usuario_id` = %s", (_id_borrar))
    cursor.execute("DELETE FROM contactos WHERE `contactos`.`id_usuario` = %s", (_id_borrar))
    conexion.commit()

    session.clear()

    return redirect('/')


#Bscar y agregar pyamigos
@app.route('/pyamigo')
def pyamigo():
    conexion = mysql.connect()
    cursor = conexion.cursor() 
    cursor.execute("SELECT * FROM `usuarios`") 
    usuarios = cursor.fetchall()
    conexion.commit()

    contactos = []
    for usuario in usuarios:
        if session['id'] not in usuario:
            contactos.append(usuario)  

    response  = make_response(render_template('paginas/pyamigo.html', contactos = contactos))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'

    return response

@app.route('/pyamigo/agregar', methods = ['POST'])
def agregar_pyamigo():
    contacto_id = request.form['contacto-agregar']
    contacto = request.form['contacto-correo']
    nombre = request.form['contacto-nombre']
    imagen = request.form['contacto-imagen']

    conexion = mysql.connect()
    cursor = conexion.cursor() 
    cursor.execute("INSERT INTO `contactos` (`contacto_id`, `contacto`, `nombre`, `imagen`, `id_usuario`) VALUES (%s,%s,%s,%s,%s)",(contacto_id, contacto,nombre,imagen,session['id'])) 
    conexion.commit()

    return redirect('/pyamigo')


@app.route('/pyamigo/buscar', methods = ['POST'])
def buscar_pyamigo():
    correo = request.form['buscar-pyamigo']

    conexion = mysql.connect()
    cursor = conexion.cursor() 
    cursor.execute("SELECT * FROM usuarios") 
    usuarios = cursor.fetchall()
    conexion.commit()

    usuarios_buscar = []
    for usuario in usuarios:
        if correo in usuario:
            usuarios_buscar.append(usuario)

    return render_template('paginas/pyamigo.html', contactos = usuarios_buscar)


#ENVIAR MENSAJE AL AMIGO QUE QUEREMOS
@app.route('/chats')
def chats():
    if not 'login' in session:
        return  redirect('/')
    
    #Se busca si existe alguna conversación
    conexion = mysql.connect()
    cursor = conexion.cursor() 
    cursor.execute("SELECT * FROM conversacion WHERE id_usuario = %s", (session['id'])) 
    conversaciones = cursor.fetchall()
    cursor.execute("SELECT * FROM `contactos` WHERE `id_usuario` = %s", (session['id'])) 
    contactos_usuario = cursor.fetchall()
    conexion.commit()
    
    contactos = []
    for contacto in contactos_usuario:
        for chat in conversaciones:
            if session['id'] in chat:
                contactos.append(contacto)

    #Empieza Parte de Mensajes
    conexion = mysql.connect()
    cursor = conexion.cursor() 
    cursor.execute("SELECT * FROM conversacion WHERE id_usuario = %s", (session['id'])) 
    conversaciones = cursor.fetchall()
    cursor.execute("SELECT * FROM `contactos` WHERE `id_usuario` = %s", (session['id'])) 
    contactos_usuario = cursor.fetchall()
    conexion.commit()
    
    
    response = make_response(render_template('paginas/chats.html',chats = conversaciones, contactos = contactos))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

#Para los mensajes del chat
@app.route('/chats/mensajes', methods = ['POST'])
def mensajes():


    return redirect('/chats')



#Para generar una nueva conversación
@app.route('/perfil/mensaje/contacto', methods = ['POST'])
def mensaje_contacto():
    _id_contacto = request.form['contacto-mensaje']

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `contactos` where contacto_id = %s AND id_usuario = %s",(_id_contacto,session['id'])) 
    contactos_ = cursor.fetchall()
    conexion.commit()

    for contacto in contactos_:
        if _id_contacto and session['id'] in contacto:

            conexion = mysql.connect()
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO `conversacion` (`conversacion_id`, `id_usuario`, `id_contacto`) VALUES (NULL, %s, %s)",(session['id'],_id_contacto )) 
            conexion.commit()


    response  = make_response(redirect('/chats'))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'

    return response



@app.route('/perfil/borrar/contacto', methods = ['POST'])
def borrar_contacto():
    id_borrar = request.form['contacto-borrar']

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM `contactos` WHERE contacto_id = %s AND id_usuario = %s",(id_borrar,session['id'])) 
    conexion.commit()

    response = make_response(redirect('/perfil'))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response


#Aquí
if __name__ == '__main__':
    app.run(debug = True)