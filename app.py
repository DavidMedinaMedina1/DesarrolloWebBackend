from email import message_from_string
from http import client
from flask import Flask, redirect, render_template, request, session, url_for
import datetime
import pymongo
from sqlalchemy import false
from decouple import config

# FlASK
#############################################################
app = Flask(__name__)
app.permanent_session_lifetime = datetime.timedelta(days=1)
app.secret_key = "super secret key"
#############################################################

# MONGODB
#############################################################
mongodb_key = config("mongodb_key")
client = pymongo.MongoClient(
    mongodb_key, tls=True, tlsAllowInvalidCertificates=True)
db = client.Tizanyaki
####cuentas = db.usuario
cuentas = db.usuario
##############################################################

##############################################################
#Configuración profesor
#mongodb_key = "mongodb+srv://desarrollowebuser:desarrollowebpassword@cluster0.dfh7g.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
#client = pymongo.MongoClient(
#    mongodb_key, tls=True, tlsAllowInvalidCertificates=True)
#db = client.Escuela
#cuentas = db.alumno
#############################################################

@app.route('/')
def home():
    email = None
    if "email" == session:
        email = session["email"]
        return render_template('index.html', error = email)
    else:
        return render_template('login.html', error = email)



@app.route('/login', methods=['POST'])
def login2Index():
    nombre = ""
    email = request.form['email']
    password = request.form['password']
    session['email'] = email
    session['password'] = password
    try:
        cursor = cuentas.find({"Correo":email, "Contrasena":password})
        users = []
        for doc in cursor:
            users.append(doc)
        
        if len(users) == 0:
            return  "<p>El correo %s no existe o la contraseña es incorrecta, regrese a la página anterior e intentelo nuevamente</p>" % (email)
        else:
            
            return render_template('index.html', error = users)
            
    except Exception as e:
        return "%s" % e
    
@app.route('/signup', methods=['POST'])
def signup():
    email = ""
    if 'email' in session:
        return render_template('index.html', error=email)
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        session['email'] = email
        session['password'] = password
        session['name'] = name
    return render_template('index.html', error=email)

@app.route('/logout')
def logout():
    if 'email' in session:
        email = session['email']
    session.clear()
    return redirect(url_for('home'))

@app.route("/usuarios")
def usuarios():
    cursor = cuentas.find({})
    users = []
    for doc in cursor:
        users.append(doc)
    return render_template("/Usuarios.html", data=users)

@app.route("/insert", methods=["POST"])
def insertUsers():
    user = {
        "Nombre": request.form["nombre"],
        "Edad": request.form["edad"],
        "Correo": request.form["correo"],
        "Contrasena": request.form["contrasena"],
    }
    try:
        cuentas.insert_one(user)
        return redirect(url_for("usuarios"))
    except Exception as e:
         return "<p>El servicio no esta disponible =>: %s %s" % type(e), e

@app.route("/find_one/<correo>")
def find_one(Correo):
    try:
        user = cuentas.find_one({"correo": (Correo)})
        if user == None:
            #return True
            return "<p>El correo %s nó existe</p>" % (Correo)
        else:
            return "<p>Encontramos: %s </p>" % (user)
         #  return False
    except Exception as e:
        return "%s" % e

@app.route("/delete/<correo>")
def delete_one(correo):
    try:
        user = cuentas.delete_one({"Correo": (correo)})
        if user.deleted_count == None:
            return "<p>El correo %s nó existe</p>" % (correo)
        else:
            return redirect(url_for("usuarios"))
    except Exception as e:
        return "%s" % e

@app.route("/update", methods=["POST"])
def update():
    try:
        filter = {"Correo": request.form["correo"]}
        user = {"$set": {
            "Nombre": request.form["nombre"],
        }}
        cuentas.update_one(filter, user)
        return redirect(url_for("usuarios"))
    except Exception as e:
        return "error %s" % (e)

@app.route('/create')
def create():
    return render_template('Create.html')

@app.route('/sss')
def sss():
    return render_template('sss.html')

