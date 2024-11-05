import os
import sys

def obtener_procesos():
    # Obtener el directorio del ejecutable o script
    directorio_base = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
    ruta_archivo = os.path.join(directorio_base, "procesos.txt")
    
    procesos = []
    
    with open(ruta_archivo, "r") as archivo:
        next(archivo)  # Saltar la primera línea de títulos
        for linea in archivo:
            partes = linea.strip().split(";")
            proceso = {
                "id": int(partes[0]),
                "tamaño": int(partes[1]),
                "tiempo_arribo": int(partes[2]),
                "tiempo_irrupcion": int(partes[3])
            }
            procesos.append(proceso)
    
    return procesos
