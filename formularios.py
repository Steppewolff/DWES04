from flask_wtf import FlaskForm
from wtforms import StringField, DateField, EmailField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, NoneOf, Regexp, EqualTo, Email
import email_validator
from datetime import date

class FormularioAlta(FlaskForm):
    username = StringField('Usuario: ', validators = [Length(min=6, max=15, message='La longitud debe estar entre 6 y 15 caracteres'), NoneOf(['caca','pedo','culo','pis','java','php'], message='El nombre escogido no es válido, introduzca otro')])    
    name = StringField('Nombre: ', validators = [Length(max=50, message='La longitud debe ser inferior a 50 caracteres')])
    surname = StringField('Apellidos: ', validators = [Length(max=50, message='La longitud debe ser inferior a 50 caracteres')])
    password = PasswordField('Contraseña: ', validators = [Regexp("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,}", message='Formato mal'),Length(min=8, message='Demasiado corta, debe tener al menos 8 caracteres'), EqualTo('passwordRep', message='La contraseña no coincide')])
    passwordRep = PasswordField('Repita su Contraseña: ')
    todayDate = date.today()
    joinDate = DateField('Fecha de alta: ', default=date.today())
    email = EmailField('Correo electrónico: ', validators = [Email(message='Introduzca una cuenta de correo válida')])
    phoneNumber = StringField('Número de teléfono: ', validators = [Regexp("[(][\d]{4}[)][ -]*([\d][ -]*){9}", message='El número de teléfono no es válido, el formato debe ser (00XX)XXXXXXXXX')])    
    submit = SubmitField('Enviar')

