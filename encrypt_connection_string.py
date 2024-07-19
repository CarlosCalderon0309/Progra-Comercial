from cryptography.fernet import Fernet
import os

# Función para generar una clave de encriptación y mostrarla
def generar_clave():
    clave = Fernet.generate_key()
    print(f"Clave de encriptación: {clave.decode()}")
    return clave

# Función para encriptar una cadena de conexión
def encriptar_cadena(clave, cadena):
    cifrador = Fernet(clave)
    texto_encriptado = cifrador.encrypt(cadena.encode())
    print(f"Cadena de conexión encriptada: {texto_encriptado.decode()}")
    return texto_encriptado

# Función para guardar la clave y la cadena encriptada en un archivo .env
def guardar_env(clave, texto_encriptado):
    with open('.env', 'w') as archivo:
        archivo.write(f"ENCRYPTION_KEY={clave.decode()}\n")
        archivo.write(f"ENCRYPTED_DATABASE_URL={texto_encriptado.decode()}\n")

if __name__ == "__main__":
    # Cadena de conexión a encriptar
    cadena_conexion = "mysql+mysqlconnector://root:database@localhost:3306/mvc1"
    
    # Generar clave y encriptar cadena
    clave_generada = generar_clave()
    texto_encriptado = encriptar_cadena(clave_generada, cadena_conexion)
    
    # Guardar resultados en el archivo .env
    guardar_env(clave_generada, texto_encriptado)
