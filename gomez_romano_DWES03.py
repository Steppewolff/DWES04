from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from datetime import date, timedelta, datetime
import datetime as dt
from bdd import Reservas
import os
import sys

app = Flask(__name__)

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
@app.route('/', methods = ['GET', 'POST'])
def crearReserva():
    tiposPista = Reservas.cargarTiposPista()
    usuarios = Reservas.cargarUsuarios()
    return render_template('registropista.html', tiposPista = tiposPista, usuarios = usuarios)

@app.route('/formulario', methods = ['GET', 'POST'])
def formulario():
    tiposPista = Reservas.cargarTiposPista()
    usuarios = Reservas.cargarUsuarios()    
    return render_template('registropista.html', tiposPista = tiposPista, usuarios = usuarios)

'''Esta es la página donde se van a hacer nuevas reservas para las pistas

'''
@app.route('/reservar', methods = ['GET','POST'])
def reservar():
    usuario = request.args.get('usuario')
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
def reservaspista():
    columnas = ["Día", "Hora", "Pista", "Nombre"]
    diaSemana = date.today().weekday()
    fechaInicio = date.today() - dt.timedelta(days = diaSemana)
    fechaFin = fechaInicio + dt.timedelta(days = 4)
    listaReservas = Reservas.cargarReservas(fechaInicio)
    tablaReservas = tabla_reservas(listaReservas)
    return render_template('reservaspista.html', tablaReservas = tablaReservas, columnas = columnas, fechaInicio = fechaInicio, fechaFin= fechaFin)

@app.route('/semanamas', methods = ['GET', 'POST'])
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
def semanamenos():
    columnas = ["Día", "Hora", "Pista", "Nombre"]
    fechaInicioAux = request.args.get('fechaInicioMenos')
    fechaInicioMenos = toDatetime(fechaInicioAux)
    fechaInicio = fechaInicioMenos - dt.timedelta(days = 7)
    fechaFin = fechaInicio + dt.timedelta(days = 4)
    listaReservas = Reservas.cargarReservas(fechaInicio)
    tablaReservas = tabla_reservas(listaReservas)
    return render_template('reservaspista.html', tablaReservas = tablaReservas, columnas = columnas, fechaInicio = fechaInicio, fechaFin= fechaFin)

@app.route('/usuarios', methods = ['GET', 'POST'])
def usuarios():
    usuarios = Reservas.cargarUsuarios()
    add = False
    return render_template('usuarios.html', usuarios = usuarios, add = add)

@app.route('/addusuario', methods = ['GET', 'POST'])
def addUsuarios():
    add = True
    usuarios = Reservas.cargarUsuarios()

    return render_template('usuarios.html', usuarios = usuarios, add = add)

@app.route('/usuarioadded', methods = ['GET', 'POST'])
def usuarioAdded():
    add = False
    usuarios = Reservas.cargarUsuarios()
    nextID = Reservas.getTableLastValue('clients', 'idclient')
    newID = nextID['MAX(idclient)'] + 1
    newname = request.args.get('newname')
    newapellidos = request.args.get('newapellidos')
    newtelefono = request.args.get('newtelefono')
    error = 0
    for usuario in usuarios:
        if usuario['nom'] == newname and usuario['llinatges'] == newapellidos:
            error = 'El usuario ya existe'
            return render_template('usuarios.html', usuarios = usuarios, add = add, error = error)
        elif usuario['telefon'] == newtelefono:
            error = 'El telefono ya está registrado para otro usuario'
            return render_template('usuarios.html', usuarios = usuarios, add = add, error = error)
        else:
            Reservas.addUsuario(newID, newname, newapellidos, newtelefono)
            usuarios = Reservas.cargarUsuarios()
            return render_template('usuarios.html', usuarios = usuarios, add = add)

@app.route('/removeusuario', methods = ['GET', 'POST'])
def removeUsuario():
    add = False
    idclientRemove = request.args.get('id_remove')
    Reservas.removeUsuario(idclientRemove)
    usuarios = Reservas.cargarUsuarios()

    return render_template('usuarios.html', usuarios = usuarios, add = add)

@app.route('/editusuario', methods = ['GET', 'POST'])
def editUsuario():
    add = 'edit'
    idclientEdit = int(request.args.get('id_edit'))
    usuarios = Reservas.cargarUsuarios()

    return render_template('usuarios.html', usuarios = usuarios, add = add, idclientEdit = idclientEdit)

@app.route('/editedusuario', methods = ['GET', 'POST'])
def editedUsuario():
    add = False
    usuarios = Reservas.cargarUsuarios()
    idclientEdit = int(request.args.get('id_edit'))
    newname = request.args.get('newname')
    newapellidos = request.args.get('newapellidos')
    newtelefono = request.args.get('newtelefono')
    error = 0
    for usuario in usuarios:
        if usuario['nom'] == newname and usuario['apellidos'] == newapellidos:
            error = 'El usuario ya existe'
            return render_template('usuarios.html', usuarios = usuarios, add = add, error = error)
        elif usuario['telefon'] == newtelefono:
            error = 'El telefono ya está registrado para otro usuario'
            return render_template('usuarios.html', usuarios = usuarios, add = add, error = error)
        else:
            Reservas.editUsuario(idclientEdit, newname, newapellidos, newtelefono)
            usuarios = Reservas.cargarUsuarios()
            return render_template('usuarios.html', usuarios = usuarios, add = add, idclientEdit = idclientEdit)

#Ejecutar la aplicación
if __name__ == "__main__":
    #app.run('0.0.0.0', 5100, debug=True)

    port = int(os.environ.get("PORT", 5100))
    app.run(host = '0.0.0.0', port = port, debug = True)

#PRINT_DEBUG######################################################################################################
#print('Print PRUEBA Error', file=sys.stderr)
#print('Print PRUEBA Out', file=sys.stdout)