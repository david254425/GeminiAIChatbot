import os

secret_key = os.urandom(24).hex()
print("Clave secreta generada:")
print(secret_key)

# Guardar solo la clave en .env, pero sin borrar otras variables existentes
env_path = ".env"

# Leer contenido previo, si existe
existing_env = ""
if os.path.exists(env_path):
    with open(env_path, "r") as f:
        existing_env = f.read()

# Escribir la clave al final, solo si no está ya definida
if "FLASK_SECRET_KEY" not in existing_env:
    with open(env_path, "a") as f:
        f.write(f"\nFLASK_SECRET_KEY={secret_key}\n")
    print(".env actualizado con la clave secreta.")
else:
    print("FLASK_SECRET_KEY ya existe en .env, no se modificó.")
