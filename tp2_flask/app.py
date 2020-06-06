import os
import redis
from flask import Flask, request
from flask import render_template

app = Flask(__name__)

def connect_db():
    conexion = redis.StrictRedis(os.environ['DB_PORT_6379_TCP_ADDR'], port=6379, db=0)
    if(conexion.ping()):
        print("conectado al servidor de redis")
    else:
        print("error..")
    return conexion
    
@app.route('/almacenarDatos')
def almacenarDatos():
    conexion = connect_db()
    conexion.set("Clave1","Valor1")
    return "Almacenado"


@app.route('/recuperarDatos')
def recuperarDatos():
    conexion = connect_db()
    return conexion.get("Clave1")

@app.route('/cargarLista')
def cargarLista():
    conexion = connect_db()
    conexion.lpush("1 temporada", 
    "Chapter 1: The Mandalorian", 
    "Chapter 2: The Child", 
    "Chapter 3: The Sin",
    "Chapter 4: Sanctuary", 
    "Chapter 5: The Gunslinger", 
    "Chapter 6: The Prisoner", 
    "Chapter 7: The Reckoning", 
    "Chapter 8: Redemption")
    return render_template('/')



@app.route('/')
def todo():
    conexion = connect_db()
    resultado = conexion.lrange('1 temporada', 0, -1)
    aux = []
    aux2 = []
    for valor in resultado:
        aux.append(str(valor))
        v = str(valor)
        v = v.strip('b')
        v=v.replace("'", '')
        if (conexion.exists(v)):
            a=conexion.get(v)
            print(a)
            a=str(a)
            a=a.strip('b')
            a=a.replace("'", '')       
            aux2.append(a)
        else:
            aux2.append(v)
    return render_template('/todo.html',datos=aux, datos2=aux2)

@app.route('/reservar', methods=["POST"])
def reservar():
    if request.method == 'POST':
        nombre = request.form['nombre']
    conexion =  connect_db()
    conexion.setex(nombre, 240, "Reservado")
    return render_template('/confirmarAlquiler.html', nombre=nombre)

@app.route('/alquilar', methods=["POST"])
def alquilar():
    if request.method == 'POST':
        nombre = request.form['nombre']
    conexion =  connect_db()
    conexion.setex(nombre, 86400, "Alquilado")
    return render_template('/alquilado.html', nombre=nombre)

""" @app.route('/verSiReservado/<nombre>')
def verSiReservado(nombre=""):
    conexion = connect_db()
    if (conexion.exists(nombre)):
        return "reservado"
    else:
        return "disponible" """

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)