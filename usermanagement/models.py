from usermanagement import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import pymysql.cursors

class User(UserMixin):
    id = 0

    def __init__(self):
        self.username = "null"

    def fromUsername(self, username):
        self.username = username
        userQuery = self.getID()
        if userQuery:
#            self.id = RQ['id']
            self.id = userQuery
        return self.id

    def fromID(self, userid):
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
        cursor = db.cursor()
        sql = "SELECT idusuari, cuenta, nom, llinatges from dwes04.usuaris where idusuari = '" + userid + "';"
        cursor.execute(sql)
        userQuery = cursor.fetchone()
        if userQuery:
            self.id = userQuery['idusuari']
            self.username = userQuery['cuenta']
            # self.nom = userQuery['nom']
            # self.llinatges = userQuery['llinatges']

    def comprobar(self,pwd):
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
        cursor = db.cursor()
        sql = "SELECT count(*) from dwes04.usuaris where idusuari = '" + str(self.id) + "';"
        cursor.execute(sql)
        userQuery = cursor.fetchone()
        if userQuery['count(*)'] == 1:
            sql = "SELECT pwd from dwes04.usuaris where idusuari = '" + str(self.id) + "';"
            cursor.execute(sql)
            userQuery = cursor.fetchone()
            resultado = check_password_hash(userQuery['pwd'], pwd)
            print('userQuery: ', userQuery['pwd'])
            print('pwd Formulario: ', pwd)            
            self.getID()
        else:
            resultado = False
        db.close()
        return resultado

    def getID(self):
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
        cursor = db.cursor()
        sql = "SELECT idusuari from dwes04.usuaris where cuenta = '" + self.username + "';"
        cursor.execute(sql)
        userQuery = cursor.fetchone()
        if userQuery:
            self.id = userQuery['idusuari']
        return self.id

    def getHash(pwd):
        pwdHash = generate_password_hash(pwd, method='pbkdf2:sha256', salt_length=8)
        return pwdHash