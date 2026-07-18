#!/usr/bin/env python3

"""
Examen Final DevNet
Alumno: Dany Yanez
Item 3
"""

import sqlite3
import hashlib

from flask import Flask, request

DATABASE = "usuarios.db"

app = Flask(__name__)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def crear_bd():

    conexion = sqlite3.connect(DATABASE)

    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            usuario TEXT UNIQUE,

            password TEXT

        )
    """)

    usuarios = [

        ("Dany Yanez", hash_password("Cisco123")),

        ("Administrador", hash_password("Admin123"))

    ]

    for usuario in usuarios:

        try:

            cursor.execute(

                "INSERT INTO usuarios(usuario,password) VALUES(?,?)",

                usuario

            )

        except sqlite3.IntegrityError:

            pass

    conexion.commit()

    conexion.close()


def validar(usuario, password):

    conexion = sqlite3.connect(DATABASE)

    cursor = conexion.cursor()

    cursor.execute(

        "SELECT password FROM usuarios WHERE usuario=?",

        (usuario,)

    )

    dato = cursor.fetchone()

    conexion.close()

    if dato:

        return dato[0] == hash_password(password)

    return False


@app.route("/", methods=["GET", "POST"])

def login():

    mensaje = ""

    if request.method == "POST":

        usuario = request.form["usuario"]

        password = request.form["password"]

        if validar(usuario, password):

            mensaje = f"<h2>Bienvenido {usuario}</h2>"

        else:

            mensaje = "<h2>Usuario o contraseña incorrectos</h2>"

    return f"""

    <html>

    <head>

        <title>Examen DevNet</title>

    </head>

    <body>

        <h1>Login SQLite</h1>

        <form method="post">

            Usuario:<br>

            <input type="text" name="usuario"><br><br>

            Contraseña:<br>

            <input type="password" name="password"><br><br>

            <input type="submit" value="Ingresar">

        </form>

        {mensaje}

    </body>

    </html>

    """


if __name__ == "__main__":

    crear_bd()

    app.run(

        host="0.0.0.0",

        port=5800,

        debug=True

    )
