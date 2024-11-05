import time
from colorama import Fore, Back, Style, init
import os
import copy  # Necesitamos copy para hacer deepcopy de los objetos
from ClaseMemoria import Memoria
from ClaseParticion import Particion
from ClaseProcesador import Procesador
from GenerarInforme import generar_informe
from ClaseEstados import ClaseEstados  # Importamos ClaseEstados para guardar el estado del sistema
import graficador  # Importamos el graficador

init(autoreset=True)
os.system('cls')

multiprogramacion = 5

def simulador(procesos):

    multiprogramacion = 5

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
    t = -1

    # Lista para almacenar los estados
    historial_estados = []
    eventos = []
    indice_estado = 0  # Índice para manejar el estado actual

    # Bucle principal de simulación
    while True:
        print(f"Antes de presionar botones: t={t}, indice_estado={indice_estado}, len(historial_estados)={len(historial_estados)}")
        print(f"t: {t}")
        print(f"indice: {indice_estado}")
        print(f"cantidad de estados: {len(historial_estados)}")
        if indice_estado == len(historial_estados):  # Si estamos en un nuevo estado, actualizar
            line = 0
            eventos.clear()
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
                    evento = (f"{line}) {f'Proceso {proceso.id} paso de SUSPENDIDOS A LISTOS con Partición de MEMORIA {particion_disponible.id}'}")
                    eventos.append(evento)  # Agregar el evento a la lista
                    print(evento)

            # Luego, verificar si hay procesos actuales que deben llegar en t
            actuales = [proceso for proceso in procesos if ((proceso.tiempo_arribo <= t) and not (proceso.admitido))]
            for proceso in actuales:
                particion_disponible = memoria.buscar_particion_disponible(proceso)
                if ((len(Listos) + (0 if procesador.libre else 1) + len(Suspendidos)) < multiprogramacion):
                    if particion_disponible:
                        if (proceso.tiempo_arribo < t):
                            line += 1
                            evento = (f"{line}) {f'Proceso {proceso.id} cambió su tiempo de arribo de {proceso.tiempo_arribo} a {t} por grado de multiprogramación'}")
                            eventos.append(evento)  # Agregar el evento a la lista
                            print(evento)
                        proceso.admitir(t)
                        particion_disponible.asignar_proceso(proceso)
                        Listos.append(proceso)
                        line += 1
                        evento = (f"{line}) {f'Proceso {proceso.id} arribó y se ubicó en cola de LISTOS con Partición de MEMORIA {particion_disponible.id}'}")
                        eventos.append(evento)  # Agregar el evento a la lista
                        print(evento)
                    else:
                        if (proceso.tiempo_arribo < t):
                            line += 1
                            evento = (f"{line}) {f'Proceso {proceso.id} cambió su tiempo de arribo de {proceso.tiempo_arribo} a {t} por grado de multiprogramación'}")
                            eventos.append(evento)  # Agregar el evento a la lista
                            print(evento)
                        proceso.admitir(t)
                        Suspendidos.append(proceso)
                        line += 1
                        evento = (f"{line}) {f'Proceso {proceso.id} arribó y se ubicó en cola de SUSPENDIDOS'}")
                        eventos.append(evento)  # Agregar el evento a la lista
                        print(evento)

            # Ejecutar proceso si el procesador está libre y hay procesos en la cola de listos
            if procesador.libre and len(Listos) > 0:
                proceso_actual = Listos.pop(0)
                procesador.asignar_proceso(proceso_actual)
                proceso_actual.calcular_tiempo_fragmentacion_interna_generada()
                line += 1
                evento = (f"{line}) {f'Proceso {proceso_actual.id} sale de cola de LISTOS para ejecutarse'}")
                eventos.append(evento)  # Agregar el evento a la lista
                print(evento)
                line += 1
                evento = (f"{line}) {f'Procesador comienza a ejecutar Proceso {proceso_actual.id}'}")
                eventos.append(evento)  # Agregar el evento a la lista
                print(evento)

            # Ejecutar el proceso en el procesador
            if not procesador.libre:
                procesador.ejecutar()

                # Si el proceso ha terminado
                if procesador.proceso.ha_terminado():
                    procesador.proceso.tiempo_finalizacion = t
                    Finalizados.append(procesador.proceso)
                    line += 1
                    evento = (f"{line}) {f'Proceso {procesador.proceso.id} finaliza en esta unidad de tiempo'}")
                    eventos.append(evento)  # Agregar el evento a la lista
                    print(evento)
                    memoria.liberar_particion(procesador.proceso)
                    procesador.liberar()

                # Si el quantum ha terminado pero el proceso no ha finalizado
                elif procesador.quantum_restante == 0 and not procesador.proceso.ha_terminado():
                    Listos.append(procesador.proceso)
                    line += 1
                    evento = (f"{line}) {f'Proceso {procesador.proceso.id} agota el quantum en esta unidad de tiempo y pasa a cola de LISTOS'}")
                    eventos.append(evento)  # Agregar el evento a la lista
                    print(evento)
                    procesador.liberar()

            # Generar informe antes de incrementar el tiempo
            print(Fore.GREEN + "==================================================")
            # generar_informe(Finalizados, Listos, Suspendidos, procesador, t, memoria, procesos)

            # **Guardar el estado actual haciendo deepcopy**
            estado_actual = ClaseEstados(t, copy.deepcopy(procesador), copy.deepcopy(memoria), copy.deepcopy(Listos), copy.deepcopy(Suspendidos), copy.deepcopy(Finalizados), copy.deepcopy(procesos), copy.deepcopy(eventos))
            historial_estados.append(estado_actual)

            # Incrementar el tiempo solo si estamos avanzando
            t += 1

        # Mostrar gráficos del estado actual
        estado = historial_estados[indice_estado]
        graficador.actualizar_graficos(estado.procesador, estado.memoria, estado.listos, estado.suspendidos, estado.finalizados, estado.t, estado.procesos, estado.eventos)

        # Esperar interacción para avanzar o retroceder
        
        boton_rect_avanzar, boton_rect_retroceder = graficador.dibujar_botones(estado.t, estado.procesos)
        accion = graficador.esperar_evento_o_enter(boton_rect_avanzar, boton_rect_retroceder, indice_estado, historial_estados, procesos)

        # Modificar el índice del estado basado en la acción
        if accion == 'avanzar':
            # Permitir avanzar si no estamos en el último estado ya registrado
            if indice_estado < len(historial_estados) - 1:
                indice_estado += 1  # Avanzar a un estado ya creado
            elif indice_estado == len(historial_estados) - 1:
                indice_estado += 1  # Avanza al siguiente estado solo si estamos en el último
        elif accion == 'retroceder' and indice_estado > 0:
            indice_estado -= 1  # Retrocede al estado anterior

        # Limpiar la terminal y actualizar gráficos solo si se ha realizado un cambio en el índice
        if accion == 'avanzar' or accion == 'retroceder':
            os.system('cls')  # Limpiar la terminal para un nuevo estado

        print(f"Después de interacción: t={t}, indice_estado={indice_estado}, len(historial_estados)={len(historial_estados)}")

        # Verificar si hemos llegado al final de la simulación
        if len(Finalizados) == len(procesos):
            # Mostrar informe final
            print(Fore.YELLOW + "==================================================")
            print(Fore.YELLOW + "                SIMULACIÓN FINALIZADA               ")
            print(Fore.YELLOW + "==================================================")
            # generar_informe(Finalizados, Listos, Suspendidos, procesador, t, memoria, procesos)

            # Actualizar gráficos finales
            graficador.actualizar_graficos(procesador, memoria, Listos, Suspendidos, Finalizados, t, procesos, eventos)
            
            # Esperar que el usuario presione ENTER para finalizar
            input(Fore.RED + "\nPresiona ENTER para finalizar la simulación...")
            break

    # Cerrar los gráficos al finalizar la simulación
    graficador.cerrar_graficos()

    return Finalizados
