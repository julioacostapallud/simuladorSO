import sys
sys.dont_write_bytecode = True  # Evita la creación de __pycache__

from AlgoritmoSimulador import simulador
from procesos_data import obtener_procesos
from ClaseProceso import Proceso

def main():
    # Cargar procesos desde el archivo de datos
    datos_procesos = obtener_procesos()

    # Convertir los datos de los diccionarios a objetos de la clase Proceso
    procesos = [Proceso(**proceso) for proceso in datos_procesos]

    # Ejecutar el simulador y recibir los procesos finalizados
    finalizados = simulador(procesos)

    # # Mostrar resultados
    # for proceso in finalizados:
    #     print(f"Proceso {proceso.id} ha finalizado.")

if __name__ == "__main__":
    main()
