import pymysql.cursors
import datetime

class Reservas(object):
    def cargarTiposPista():
        #Conectarse a la BDD
        db = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='0Castorp0',
            db='dwes04',
            charset='utf8mb4',
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor
        )

        #Creo un objeto cursor para recibir la información de la query
        cursor = db.cursor()

        #Query para MySQL
        sql  = "SELECT * from dwes04.pistes"
        cursor.execute(sql)
        resQueryTipos = cursor.fetchall()
        db.close()
        return resQueryTipos

    def getTipoPista(idpista):
        #Conectarse a la BDD
        db = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='0Castorp0',
            db='dwes04',
            charset='utf8mb4',
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        #Creo un objeto cursor para recibir la información de la query
        cursor = db.cursor()

        #Query para MySQL
        sql  = "SELECT tipo from dwes04.pistes WHERE idpista = " + str(idpista) + ";"
        cursor.execute(sql)
        resQueryPista = cursor.fetchall()
        db.close()
        return resQueryPista 

    def cargarUsuarios():
        #Conectarse a la BDD
        db = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='0Castorp0',
            db='dwes04',
            charset='utf8mb4',
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        #Creo un objeto cursor para recibir la información de la query
        cursor = db.cursor()

        #Query para MySQL
        sql  = "SELECT * from dwes04.usuaris"
        cursor.execute(sql)
        resQueryClients = cursor.fetchall()
        db.close()
        return resQueryClients 

    def getUsuario(idusuari):
        #Conectarse a la BDD
        db = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='0Castorp0',
            db='dwes04',
            charset='utf8mb4',
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        #Creo un objeto cursor para recibir la información de la query
        cursor = db.cursor()

        #Query para MySQL
        sql  = "SELECT nom, llinatges from dwes04.usuaris WHERE idusuari = " + str(idusuari) + ";"
        cursor.execute(sql)
        resQueryClient = cursor.fetchall()
        db.close()
        return resQueryClient 

    def getTableLastValue(table, column):
        #Conectarse a la BDD
        db = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='0Castorp0',
            db='dwes04',
            charset='utf8mb4',
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        #Creo un objeto cursor para recibir la información de la query
        cursor = db.cursor()

        #Query para MySQL
        sql  = "SELECT MAX(" + column + ") FROM dwes04." + table + ";"
        cursor.execute(sql)
        resQuery = cursor.fetchall()
        columnValue = resQuery[0]
        if columnValue['MAX(idusuari)'] == None:
            nextID = 1
        else:
            nextID = columnValue['MAX(idusuari)'] + 1
        db.close()
        return nextID 

    def addUsuario(newID, newusername, newname, newsurname, newpassword, newjoinDate, newemail, newphoneNumber):
        #Conectarse a la BDD
        db = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='0Castorp0',
            db='dwes04',
            charset='utf8mb4',
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        #Creo un objeto cursor para recibir la información de la query
        cursor = db.cursor()

        sql  = "INSERT INTO dwes04.usuaris VALUES (" + str(newID) + ", '" + newusername + "', '" + newname +"', '" + newsurname + "', '" + str(newpassword) + "', '" + str(newjoinDate) + "', '" + str(newemail) + "', '" + newphoneNumber + "');"
        cursor.execute(sql)
        resQueryClientAdded = cursor.fetchall()
        db.close()
        return cursor.lastrowid 

    def cargarReservas(fechaInicio):
        #Conectarse a la BDD
        db = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='0Castorp0',
            db='dwes04',
            charset='utf8mb4',
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        #Creo un objeto cursor para recibir la información de la query
        cursor = db.cursor()

        #Query para MySQL
        fechaFin = fechaInicio + datetime.timedelta(days = 4)
        sql  = "SELECT * from dwes04.reserves WHERE data BETWEEN '" + str(fechaInicio) + "' and '" + str(fechaFin) + "';"
        cursor.execute(sql)
        resQueryReserves = cursor.fetchall()
        db.close()
        return resQueryReserves

    def comprobarReserva(dia, hora, tipopista):
        #Conectarse a la BDD
        db = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='0Castorp0',
            db='dwes04',
            charset='utf8mb4',
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        #Creo un objeto cursor para recibir la información de la query
        cursor = db.cursor()
        print('dia:', dia)
        print('hora:', hora)
        print('pista:', tipopista)
        #Query para MySQL
        sql  = "SELECT idpista, idclient from dwes04.reserves where data = '" + dia + " " + hora +":00:00' and idpista = " + str(tipopista) + ";"

        cursor.execute(sql)
        resQueryReserves = cursor.fetchall()
        db.close()
        return resQueryReserves

    def escribirReserva(dia, hora, usuario, tipopista):
        #Conectarse a la BDD
        db = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='0Castorp0',
            db='dwes04',
            charset='utf8mb4',
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        #Creo un objeto cursor para recibir la información de la query
        cursor = db.cursor()

        #Query para MySQL
        sql  = "INSERT INTO dwes04.reserves VALUES ('" + dia + " " + hora +":00:00', " + tipopista + ", " + usuario + ")"
        cursor.execute(sql)
        db.commit()
        db.close()
        return cursor.lastrowid