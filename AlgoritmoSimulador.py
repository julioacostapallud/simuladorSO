import time
from ClaseMemoria import Memoria
from ClaseParticion import Particion
from ClaseProcesador import Procesador
from GenerarInforme import generar_informe

def simulador(procesos):
    # Crear particiones con tamaños definidos
    particiones = [
        Particion(id=1, tamaño=100, libre=False),  # Partición reservada para SO (no se usa)
        Particion(id=2, tamaño=250, libre=True),   # Grandes
        Particion(id=3, tamaño=150, libre=True),   # Medianos
        Particion(id=4, tamaño=50, libre=True)     # Pequeños
    ]

    memoria = Memoria(particiones=particiones)
    procesador = Procesador(quantum=3)
    Listos = []
    Suspendidos = []
    Finalizados = []
    t = 0

    while True:
        # Primero, asignar procesos suspendidos si hay espacio
        for proceso in Suspendidos[:]:
            particion_disponible = memoria.buscar_particion_disponible(proceso)
            if particion_disponible:
                particion_disponible.asignar_proceso(proceso)
                Listos.append(proceso)
                Suspendidos.remove(proceso)

        # Luego, verificar si hay procesos actuales que deben llegar en t
        actuales = [proceso for proceso in procesos if proceso.tiempo_arribo == t]
        for proceso in actuales:
            particion_disponible = memoria.buscar_particion_disponible(proceso)
            if particion_disponible:
                particion_disponible.asignar_proceso(proceso)
                Listos.append(proceso)
            else:
                Suspendidos.append(proceso)

        # Ejecutar proceso si el procesador está libre y hay procesos en la cola de listos
        if procesador.libre and len(Listos) > 0:
            proceso_actual = Listos.pop(0)
            procesador.asignar_proceso(proceso_actual)

        # Ejecutar el proceso en el procesador
        if not procesador.libre:
            procesador.ejecutar()

            # Si el proceso ha terminado
            if procesador.proceso.ha_terminado():
                procesador.proceso.tiempo_finalizacion = t
                Finalizados.append(procesador.proceso)
                memoria.liberar_particion(procesador.proceso)
                procesador.liberar()

            # Si el quantum ha terminado pero el proceso no ha finalizado
            elif procesador.quantum_restante == 0 and not procesador.proceso.ha_terminado():
                Listos.append(procesador.proceso)
                procesador.liberar()

        # Generar informe antes de incrementar el tiempo
        generar_informe(Finalizados, Listos, Suspendidos, procesador, t, memoria)

        time.sleep(2)

        # Incrementar el tiempo
        t += 1

        # Terminar si todos los procesos han finalizado
        if len(Finalizados) == len(procesos):
            break

    return Finalizados
