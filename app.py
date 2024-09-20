from flask import Flask, render_template,Blueprint
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import (
    login_required,
    login_manager,
    UserMixin,
    login_user,
    logout_user,
    current_user,
)
from sqlalchemy.exc import IntegrityError
from app import create_app,db
from app.models import Equipo
from app.routes import equipo_routes
from app.models import Usuario
from app.config import SERVER_HOST, SERVER_PORT
import os
import socket
import threading
import json
import psutil
import ctypes
import signal

app = create_app()  

@app.route("/")
def index():
    contraseña ="scrypt:32768:8:1$FIYhHFrUEmO0kpti$7ec6e191d345f9d1e973e5b04fcfb4a06727a291421c96653d80b4398e5afe352cf597bc82504a8f8911843d6849a877bfdacf899bc3847f8d96d0a963db0b3e"
    #registrar administrador
    administrador_existente = Usuario.query.filter_by(idUsuario=1).first()

    if not administrador_existente:
        administrador = Usuario(
            idUsuario=1,
            usuario="administrador",
            contraseña=contraseña,
            nombreUsuario="administrador",
            identificacionUsuario="1",
            Facultad_idFacultad="Administracion"
        )
        try:
            db.session.add(administrador)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            print("Error registrando administrador", e)
    
    #registrar equipos de las salas automaticamente
    for i in range(1, 69):
        # Verifica si el equipo ya existe en la base de datos
        equipo_existente = Equipo.query.filter_by(idEquipo=i, sala="D507").first()

        if not equipo_existente:
            # Si no existe, lo creamos
            nuevo_equipo = Equipo(
                idEquipo=i,
                estadoEquipo="libre",
                sala="D507"
            )
            try:
                db.session.add(nuevo_equipo)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                print(f"Error registrando el equipo {i} en sala D507")

            
    for i in range(101,135):
        # Verifica si el equipo ya existe en la base de datos
        equipo_existente = Equipo.query.filter_by(idEquipo=i, sala="H405").first()

        if not equipo_existente:
            # Si no existe, lo creamos
            nuevo_equipo = Equipo(
                idEquipo=i,
                estadoEquipo="libre",
                sala="H405"
            )
            try:
                db.session.add(nuevo_equipo)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                print(f"Error registrando el equipo {i} en sala H405")

            
    for i in range(201,225):
        # Verifica si el equipo ya existe en la base de datos
        equipo_existente = Equipo.query.filter_by(idEquipo=i, sala="I408").first()

        if not equipo_existente:
            # Si no existe, lo creamos
            nuevo_equipo = Equipo(
                idEquipo=i,
                estadoEquipo="libre",
                sala="I408"
            )
            try:
                db.session.add(nuevo_equipo)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                print(f"Error registrando el equipo {i} en sala I408")

    return render_template('index.html')


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    

        
def start_server():
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((SERVER_HOST, SERVER_PORT))
        server.listen()
        print(f"Servidor escuchando en {SERVER_HOST}:{SERVER_PORT}")
    except Exception as e:
            print(f"Error al iniciar el servidor: {e}")
    finally:
        server.close()



with app.app_context():
    Base = declarative_base()
    target_metadata = db.metadata
    db.create_all()

import signal

def signal_handler(sig, frame):
    print('Cerrando el servidor de sockets...')
    server.close()  # Asegúrate de cerrar el socket

# Registrar la señal
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == '__main__':
    socket_thread = threading.Thread(target=start_server)
    socket_thread.start()
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

