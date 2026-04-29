import os
from sqlalchemy import text, create_engine
from dotenv import load_dotenv
load_dotenv()

# 1. Configuración de la URL (Asegúrate de que coincida con tus variables)
DATABASE_URL = os.getenv("DATABASE_URL")

def run_sql_file(filename):
    # Creamos el motor de conexión
    engine = create_engine(DATABASE_URL)
    
    if not os.path.exists(filename):
        print(f"❌ Error: El archivo {filename} no existe.")
        return

    print(f"⏳ Leyendo y ejecutando {filename} en Aiven...")
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            # Leemos el archivo y separamos por ';' para ejecutar comando por comando
            sql_content = file.read()
            # Quitamos comentarios de MySQL para evitar errores
            commands = sql_content.split(';')
            
        with engine.connect() as conn:
            with conn.begin(): # Inicia una transacción (si falla uno, no hace nada)
                for command in commands:
                    clean_command = command.strip()
                    if clean_command:
                        conn.execute(text(clean_command))
            print("✅ ¡Estructura de la base de datos creada con éxito!")
            
    except Exception as e:
        print(f"❌ Ocurrió un error: {e}")

if __name__ == "__main__":
    
    nombre_archivo = "backend/database/db.sql" 
    run_sql_file(nombre_archivo)