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
            db='dwes03',
            charset='utf8mb4',
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor
        )

        #Creo un objeto cursor para recibir la información de la query
        cursor = db.cursor()

        #Query para MySQL
        sql  = "SELECT * from dwes03.pistes"
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
            db='dwes03',
            charset='utf8mb4',
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        #Creo un objeto cursor para recibir la información de la query
        cursor = db.cursor()

        #Query para MySQL
        sql  = "SELECT tipo from dwes03.pistes WHERE idpista = " + str(idpista) + ";"
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
            db='dwes03',
            charset='utf8mb4',
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        #Creo un objeto cursor para recibir la información de la query
        cursor = db.cursor()

        #Query para MySQL
        sql  = "SELECT * from dwes03.clients"
        cursor.execute(sql)
        resQueryClients = cursor.fetchall()
        db.close()
        return resQueryClients 

    def getUsuario(idclient):
        #Conectarse a la BDD
        db = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='0Castorp0',
            db='dwes03',
            charset='utf8mb4',
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        #Creo un objeto cursor para recibir la información de la query
        cursor = db.cursor()

        #Query para MySQL
        sql  = "SELECT nom, llinatges from dwes03.clients WHERE idclient = " + str(idclient) + ";"
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
            db='dwes03',
            charset='utf8mb4',
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        #Creo un objeto cursor para recibir la información de la query
        cursor = db.cursor()

        #Query para MySQL
        sql  = "SELECT MAX(" + column + ") FROM dwes03." + table + ";"
        cursor.execute(sql)
        resQuery = cursor.fetchall()
        columnValue = resQuery[0]
        db.close()
        return columnValue 

    def addUsuario(newID, newname, newapellidos, newtelefono):
        #Conectarse a la BDD
        db = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='0Castorp0',
            db='dwes03',
            charset='utf8mb4',
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        #Creo un objeto cursor para recibir la información de la query
        cursor = db.cursor()

        #Query para MySQL
        sql  = "INSERT INTO dwes03.clients VALUES (" + str(newID) + ", '" + newname +"', '" + newapellidos + "', '" + newtelefono + "')"
        cursor.execute(sql)
        resQueryClientAdded = cursor.fetchall()
        db.close()
        return cursor.lastrowid 

    def removeUsuario(idclient):
        #Conectarse a la BDD
        db = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='0Castorp0',
            db='dwes03',
            charset='utf8mb4',
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        #Creo un objeto cursor para recibir la información de la query
        cursor = db.cursor()

        #Query para MySQL
        sql  = "DELETE FROM dwes03.clients WHERE idclient = " + str(idclient) + ";"
        cursor.execute(sql)

        db.close()
        return cursor.lastrowid

    def editUsuario(idclient, newname, newapellidos, newtelefono):
        #Conectarse a la BDD
        db = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='0Castorp0',
            db='dwes03',
            charset='utf8mb4',
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        #Creo un objeto cursor para recibir la información de la query
        cursor = db.cursor()

        #Query para MySQL
        sql  = "UPDATE dwes03.clients SET nom = '" + newname + "', llinatges = '" + newapellidos + "', telefon = '" + newtelefono + "' WHERE idclient = " + str(idclient) + ";"
        cursor.execute(sql)

        db.close()
        return cursor.lastrowid

    def cargarReservas(fechaInicio):
        #Conectarse a la BDD
        db = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='0Castorp0',
            db='dwes03',
            charset='utf8mb4',
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        #Creo un objeto cursor para recibir la información de la query
        cursor = db.cursor()

        #Query para MySQL
        fechaFin = fechaInicio + datetime.timedelta(days = 4)
        sql  = "SELECT * from dwes03.reserves WHERE data BETWEEN '" + str(fechaInicio) + "' and '" + str(fechaFin) + "';"
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
            db='dwes03',
            charset='utf8mb4',
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        #Creo un objeto cursor para recibir la información de la query
        cursor = db.cursor()

        #Query para MySQL
        sql  = "SELECT idpista, idclient from dwes03.reserves where data = '" + dia + " " + hora +":00:00' and idpista = " + str(tipopista) + ";"

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
            db='dwes03',
            charset='utf8mb4',
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        #Creo un objeto cursor para recibir la información de la query
        cursor = db.cursor()

        #Query para MySQL
        sql  = "INSERT INTO dwes03.reserves VALUES ('" + dia + " " + hora +":00:00', " + tipopista + ", " + usuario + ")"
        cursor.execute(sql)
        db.commit()
        db.close()
        return cursor.lastrowid