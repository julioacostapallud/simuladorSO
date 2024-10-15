import time
from colorama import Fore, Back, Style, init
import os
from ClaseMemoria import Memoria
from ClaseParticion import Particion
from ClaseProcesador import Procesador
from GenerarInforme import generar_informe
import graficador  # Importamos el graficador

init(autoreset=True)
os.system('cls')

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

    # Bucle principal de simulación
    while True:
        line = 0
        print(f"                UNIDAD DE TIEMPO: {Back.RED}{Fore.YELLOW}{t}{Style.RESET_ALL}                ")
        print(Fore.GREEN + "==================================================")
        print(Fore.GREEN + f"Listado de eventos en tiempo: {t}")
        print(Fore.GREEN + "==================================================")
        
        # Primero, asignar procesos suspendidos si hay espacio
        for proceso in Suspendidos[:]:
            particion_disponible = memoria.buscar_particion_disponible(proceso)
            if particion_disponible:
                particion_disponible.asignar_proceso(proceso)
                proceso.fragmentacion_interna_generada = particion_disponible.calcular_fragmentacion_interna()
                Listos.append(proceso)
                Suspendidos.remove(proceso)
                line += 1
                print(f"{line}> {f'Proceso {proceso.id} paso de SUSPENDIDOS A LISTOS con Partición de MEMORIA {particion_disponible.id}'}")
                
        # Luego, verificar si hay procesos actuales que deben llegar en t
        actuales = [proceso for proceso in procesos if proceso.tiempo_arribo == t]
        for proceso in actuales:
            particion_disponible = memoria.buscar_particion_disponible(proceso)
            if particion_disponible:
                particion_disponible.asignar_proceso(proceso)
                Listos.append(proceso)
                line += 1
                print(f"{line}> {f'Proceso {proceso.id} arribó y se ubicó en cola de LISTOS con Partición de MEMORIA {particion_disponible.id}'}")
            else:
                Suspendidos.append(proceso)
                line += 1
                print(f"{line}> {f'Proceso {proceso.id} arribó y se ubicó en cola de SUSPENDIDOS'}")

        # Ejecutar proceso si el procesador está libre y hay procesos en la cola de listos
        if procesador.libre and len(Listos) > 0:
            proceso_actual = Listos.pop(0)
            procesador.asignar_proceso(proceso_actual)
            proceso_actual.calcular_tiempo_fragmentacion_interna_generada()
            line += 1
            print(f"{line}> {f'Proceso {proceso_actual.id} sale de cola de LISTOS para ejecutarse'}")
            line += 1
            print(f"{line}> {f'Procesador comienza a ejecutar Proceso {proceso_actual.id}'}")

        # Ejecutar el proceso en el procesador
        if not procesador.libre:
            procesador.ejecutar()

            # Si el proceso ha terminado
            if procesador.proceso.ha_terminado():
                procesador.proceso.tiempo_finalizacion = t
                Finalizados.append(procesador.proceso)
                line += 1
                print(f"{line}> {f'Proceso {procesador.proceso.id} finaliza en esta unidad de tiempo'}")
                memoria.liberar_particion(procesador.proceso)
                procesador.liberar()

            # Si el quantum ha terminado pero el proceso no ha finalizado
            elif procesador.quantum_restante == 0 and not procesador.proceso.ha_terminado():
                Listos.append(procesador.proceso)
                line += 1
                print(f"{line}> {f'Proceso {procesador.proceso.id} agota el quantum en esta unidad de tiempo y pasa a cola de LISTOS'}")
                procesador.liberar()

        # Generar informe antes de incrementar el tiempo
        print(Fore.GREEN + "==================================================")
        generar_informe(Finalizados, Listos, Suspendidos, procesador, t, memoria)

        # Actualizar gráficos después del informe y obtener el botón
        boton_rect = graficador.actualizar_graficos(procesador, memoria, Listos, Suspendidos, Finalizados, t)

        # Esperar evento de clic en el botón o ENTER en la terminal
        graficador.esperar_evento_o_enter(boton_rect)

        # Limpiar la terminal antes de avanzar
        os.system('cls')

        # Incrementar el tiempo
        t += 1

        # Terminar si todos los procesos han finalizado
        if len(Finalizados) == len(procesos):
            break

    # Cerrar los gráficos al finalizar la simulación
    graficador.cerrar_graficos()

    return Finalizados
