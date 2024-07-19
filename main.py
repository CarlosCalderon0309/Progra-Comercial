# main.py
import os
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from dotenv import load_dotenv
from cryptography.fernet import Fernet
import uvicorn

# Configuración de entorno y desencriptación
load_dotenv()

KEY = os.getenv("ENCRYPTION_KEY")
ENCRYPTED_DB_URL = os.getenv("ENCRYPTED_DATABASE_URL")

cipher = Fernet(KEY.encode())
DECRYPTED_DB_URL = cipher.decrypt(ENCRYPTED_DB_URL.encode()).decode()

print(f"Cadena encriptada: {ENCRYPTED_DB_URL}")
print(f"Cadena desencriptada: {DECRYPTED_DB_URL}")

# Configuración de la base de datos
db_engine = create_engine(DECRYPTED_DB_URL)
Base = declarative_base()

class Perro(Base):
    __tablename__ = "perros"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    raza = Column(String, index=True)
    edad = Column(Integer, index=True)

Base.metadata.create_all(bind=db_engine)

SessionLocal = sessionmaker(bind=db_engine, autocommit=False, autoflush=False)
db_session = SessionLocal()

# Configuración de la API
app = FastAPI()

class PerroSchema(BaseModel):
    nombre: str
    raza: str
    edad: int

# Endpoints CRUD
@app.get("/perros/")
def obtener_perros():
    return db_session.query(Perro).all()

@app.get("/perros/{perro_id}")
def obtener_perro(perro_id: int):
    perro = db_session.query(Perro).filter(Perro.id == perro_id).first()
    if not perro:
        raise HTTPException(status_code=404, detail="Perro no encontrado")
    return perro

@app.post("/perros/")
def crear_perro(perro: PerroSchema):
    nuevo_perro = Perro(**perro.dict())
    db_session.add(nuevo_perro)
    db_session.commit()
    db_session.refresh(nuevo_perro)
    return nuevo_perro

@app.put("/perros/{perro_id}")
def actualizar_perro(perro_id: int, perro: PerroSchema):
    db_perro = db_session.query(Perro).filter(Perro.id == perro_id).first()
    if not db_perro:
        raise HTTPException(status_code=404, detail="Perro no encontrado")
    for key, value in perro.dict().items():
        setattr(db_perro, key, value)
    db_session.commit()
    db_session.refresh(db_perro)
    return db_perro

@app.delete("/perros/{perro_id}")
def eliminar_perro(perro_id: int):
    db_perro = db_session.query(Perro).filter(Perro.id == perro_id).first()
    if not db_perro:
        raise HTTPException(status_code=404, detail="Perro no encontrado")
    db_session.delete(db_perro)
    db_session.commit()
    return {"message": "Perro eliminado exitosamente"}

# Código para encriptar cadena de conexión
def generar_clave():
    clave = Fernet.generate_key()
    print(f"Clave de encriptación: {clave.decode()}")
    return clave

def encriptar_cadena(clave, cadena):
    cifrador = Fernet(clave)
    texto_encriptado = cifrador.encrypt(cadena.encode())
    print(f"Cadena de conexión encriptada: {texto_encriptado.decode()}")
    return texto_encriptado

def guardar_env(clave, texto_encriptado):
    with open('.env', 'w') as archivo:
        archivo.write(f"ENCRYPTION_KEY={clave.decode()}\n")
        archivo.write(f"ENCRYPTED_DATABASE_URL={texto_encriptado.decode()}\n")

# Interfaz gráfica con tkinter
import tkinter as tk
from tkinter import messagebox

def encrypt_and_save():
    cadena_conexion = entry_conexion.get()
    clave_generada = generar_clave()
    texto_encriptado = encriptar_cadena(clave_generada, cadena_conexion)
    guardar_env(clave_generada, texto_encriptado)
    messagebox.showinfo("Éxito", "Cadena encriptada y guardada en .env")

def start_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Encriptar Cadena de Conexión")

tk.Label(root, text="Cadena de Conexión:").grid(row=0, column=0, padx=10, pady=10)
entry_conexion = tk.Entry(root, width=50)
entry_conexion.grid(row=0, column=1, padx=10, pady=10)

btn_encrypt = tk.Button(root, text="Encriptar y Guardar", command=encrypt_and_save)
btn_encrypt.grid(row=1, column=0, columnspan=2, pady=10)

btn_start_server = tk.Button(root, text="Iniciar Servidor", command=start_server)
btn_start_server.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
