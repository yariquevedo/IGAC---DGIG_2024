import os
import shutil
import pandas as pd

# Ruta al archivo de Excel
ruta_excel = r"C:\Users\michael.rojas\Documents\RUTAS.xlsx"

# Leer el archivo de Excel
try:
    df = pd.read_excel(ruta_excel)
    print(f"Rutas cargadas desde {ruta_excel}:\n")
    print(df)
except FileNotFoundError:
    print("El archivo no fue encontrado en la ruta especificada.")
except Exception as e:
    print(f"Ocurrió un error al leer el archivo: {e}")


carpeta_destino = r"C:\Users\michael.rojas\Documents\copiar"  # Todas las carpetas se copian aquí

# Función para copiar carpetas
def copiar_carpeta(origen, destino):
    try:
        # Verificar si el directorio de destino existe, si no, créalo
        if not os.path.exists(destino):
            os.makedirs(destino)
        
        # Copiar carpeta
        shutil.copytree(origen, os.path.join(destino, os.path.basename(origen)), dirs_exist_ok=True)
        print(f"Carpeta '{origen}' copiada a '{destino}'.")
    except Exception as e:
        print(f"Error al copiar '{origen}': {e}")

# Migrar carpetas
for index, row in df.iterrows():
    carpeta_origen = row.iloc[0]  # Usar el valor de la primera columna
    copiar_carpeta(carpeta_origen, carpeta_destino)