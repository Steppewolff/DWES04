from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
#from usermanagement import app
from usermanagement.models import User
#from usermanagement import login_manager
from flask_login import login_required, login_user, logout_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, timedelta, datetime
import datetime as dt
from bdd import Reservas
from formularios import FormularioAlta
import os
import sys

app = Flask(__name__)

app.config['SECRET_KEY'] = 'gomez_romano'
app.config['TESTING'] = False

user = User()

def init_login():
    app.config['SECRET_KEY'] = 'gomez romano'
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        if user_id:
#            user = User()
            user.fromID(user_id)
            return user

def validar_formulario(formulario):
    devolver=0
    if formulario['usuario']=="":
        devolver="No se ha introducido el nombre para la reserva"
    if formulario['tipopista']=="":
        devolver="Indica el tipo de pista a reservar"
    if devolver==0:
        resQueryReserves = Reservas.comprobarReserva(formulario['dia'], formulario['hora'], formulario['tipopista'])
        if resQueryReserves:
            devolver="Pista ya reservada"
    return devolver

def tabla_reservas (lista):
    tabla=[]
    for fila in range(0,5):
        fila_aux=[]
        for columna in range(0,6):
            match_reserva=""
            for reserva in lista:
                if reserva['data'].weekday()==fila+1 and reserva['data'].hour==columna+15:
                    nombreStr = Reservas.getUsuario(reserva['idclient'])
                    pistaStr = Reservas.getTipoPista(reserva['idpista'])     
                    match_reserva = match_reserva + nombreStr[0]['nom'] + " " + nombreStr[0]['llinatges'] + " (" + pistaStr[0]['tipo'] + ") "
            fila_aux.append(match_reserva)
        tabla.append(fila_aux)
    return tabla

def toDatetime(fechaStr):
    fechaDate = datetime.date(datetime.strptime(fechaStr, "%Y-%m-%d"))
    return fechaDate

#Pantallas de la aplicación con sus rutas, cada @ define una pantalla o sección
'''Esta es la página inicial, que coincide con la página de reservas

'''
init_login()

@app.route('/', methods = ['GET', 'POST'])
def login():

    return render_template('login.html')

@app.route('/loginVal', methods = ['GET', 'POST'])
def loginVal():
    usuarioVal = request.args.get('usuario')
    pwdVal = request.args.get('pwd')
    user = User()
    user.fromUsername(usuarioVal)
    if user.comprobar(pwdVal):
        user.getID()
        login_user(user)
        print('Ok loginVal')
        return redirect('formulario')
    else:
        return render_template('login.html', message="Login incorrecto")
    return render_template('login.html', message="Login incorrecto")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login.html')

@app.route('/signForm', methods = ['GET', 'POST'])
def signForm():
    #Instancianmos el formulario de alta
    formularioAlta = FormularioAlta()
        
    #Comprobamos que todas las restricciones de la entrada de datos al formulario se cumplen 
    if formularioAlta.validate_on_submit():
        newusername = formularioAlta.username.data
        newname = formularioAlta.name.data
        newsurname = formularioAlta.surname.data
        password = formularioAlta.password.data
        newpassword = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        newjoinDate = formularioAlta.joinDate.data
        newemail = formularioAlta.email.data
        phoneNumber = formularioAlta.phoneNumber.data
        newphoneNumber = phoneNumber.replace(' ','')

        #Recupero la tabla de usuarios de la BDD y compruebo que el nuevo usuario no existe
        usuarios = Reservas.cargarUsuarios()
        print('usuarios: ', usuarios)
        newID = Reservas.getTableLastValue('usuaris', 'idusuari')
        error = 0
        if usuarios:
            for usuario in usuarios:
                if usuario['nom'] == newname and usuario['llinatges'] == newsurname:
                    error = 'El usuario ya tiene una cuenta'
                    return render_template('login.html', error = error)
                elif usuario['cuenta'] == newusername:
                    error = 'El nombre de usuario ya existe'
                    return render_template('login.html', error = error)
                else:
                    Reservas.addUsuario(newID, newusername, newname, newsurname, newpassword, newjoinDate, newemail, newphoneNumber)
                    # return redirect(url_for("login", newusername = newusername))
                    return render_template('login.html', newusername = newusername)
        else:
            Reservas.addUsuario(newID, newusername, newname, newsurname, newpassword, newjoinDate, newemail, newphoneNumber)
            return render_template('login.html', newusername = newusername) 

    return render_template('signForm.html', formularioAlta = formularioAlta)                

@app.route('/formulario', methods = ['GET', 'POST'])
def formulario():
    tiposPista = Reservas.cargarTiposPista()
    usuarios = Reservas.cargarUsuarios()    
    return render_template('registropista.html', tiposPista = tiposPista, usuarios = usuarios)

'''Esta es la página donde se van a hacer nuevas reservas para las pistas

'''
@app.route('/reservar', methods = ['GET','POST'])
@login_required
def reservar():
    usuario = user.username
    tipopista = request.args.get('tipopista')
    dia = request.args.get('dia')
    hora = request.args.get('hora')
    nuevaReserva = {'usuario':usuario, 'tipopista':tipopista, 'dia':dia, 'hora':hora}
    comprobacionReserva = validar_formulario(nuevaReserva)
    if comprobacionReserva == 0:
        verificar = Reservas.escribirReserva(dia, hora, usuario, tipopista)
        columnas = ["Día", "Hora", "Pista", "Nombre"]
        diaSemana = date.today().weekday()
        fechaInicio = date.today() - dt.timedelta(days = diaSemana)
        fechaFin = fechaInicio + dt.timedelta(days = 4)
        listaReservas = Reservas.cargarReservas(fechaInicio)
        tablaReservas = tabla_reservas(listaReservas)
        return render_template('reservaspista.html', tablaReservas = tablaReservas, columnas = columnas, verificar = verificar, fechaInicio = fechaInicio, fechaFin= fechaFin)
    else:
        tiposPista = Reservas.cargarTiposPista()
        usuarios = Reservas.cargarUsuarios()    
        return render_template('registropista.html', error = comprobacionReserva, tiposPista = tiposPista, usuarios = usuarios)

'''Esta es la página donde se van a visualizar las reservas ya realizadas

'''
@app.route('/reservaspista', methods = ['GET', 'POST'])
@login_required
def reservaspista():
    columnas = ["Día", "Hora", "Pista", "Nombre"]
    diaSemana = date.today().weekday()
    fechaInicio = date.today() - dt.timedelta(days = diaSemana)
    fechaFin = fechaInicio + dt.timedelta(days = 4)
    listaReservas = Reservas.cargarReservas(fechaInicio)
    tablaReservas = tabla_reservas(listaReservas)
    return render_template('reservaspista.html', tablaReservas = tablaReservas, columnas = columnas, fechaInicio = fechaInicio, fechaFin= fechaFin)

@app.route('/semanamas', methods = ['GET', 'POST'])
@login_required
def semanamas():
    columnas = ["Día", "Hora", "Pista", "Nombre"]
    fechaInicioAux = request.args.get('fechaInicioMas')    
    fechaInicioMas = toDatetime(fechaInicioAux)
    fechaInicio = fechaInicioMas + dt.timedelta(days = 7)
    fechaFin = fechaInicio + dt.timedelta(days = 4)
    listaReservas = Reservas.cargarReservas(fechaInicio)
    tablaReservas = tabla_reservas(listaReservas)
    return render_template('reservaspista.html', tablaReservas = tablaReservas, columnas = columnas, fechaInicio = fechaInicio, fechaFin= fechaFin)

@app.route('/semanamenos', methods = ['GET', 'POST'])
@login_required
def semanamenos():
    columnas = ["Día", "Hora", "Pista", "Nombre"]
    fechaInicioAux = request.args.get('fechaInicioMenos')
    fechaInicioMenos = toDatetime(fechaInicioAux)
    fechaInicio = fechaInicioMenos - dt.timedelta(days = 7)
    fechaFin = fechaInicio + dt.timedelta(days = 4)
    listaReservas = Reservas.cargarReservas(fechaInicio)
    tablaReservas = tabla_reservas(listaReservas)
    return render_template('reservaspista.html', tablaReservas = tablaReservas, columnas = columnas, fechaInicio = fechaInicio, fechaFin= fechaFin)

#Ejecutar la aplicación
if __name__ == "__main__":
    #app.run('0.0.0.0', 5100, debug=True)

    port = int(os.environ.get("PORT", 5100))
    app.run(host = '0.0.0.0', port = port, debug = True)