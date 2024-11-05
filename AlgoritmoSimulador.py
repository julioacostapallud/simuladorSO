import time
import os
import copy
from colorama import Fore, Back, Style, init
from ClaseMemoria import Memoria
from ClaseParticion import Particion
from ClaseProcesador import Procesador
from GenerarInforme import generar_informe
from ClaseEstados import ClaseEstados
import graficador as graficador

init(autoreset=True)
os.system('cls')

multiprogramacion = 5

def simulador(procesos):
    particiones = [
        Particion(id=1, tamaño=100, libre=False),
        Particion(id=2, tamaño=250, libre=True),
        Particion(id=3, tamaño=150, libre=True),
        Particion(id=4, tamaño=50, libre=True)
    ]

    memoria = Memoria(particiones=particiones)
    procesador = Procesador(quantum=3)
    Listos = []
    Suspendidos = []
    Finalizados = []
    historial_estados = []
    eventos = []
    cambios_contexto_indices = []
    t = 0

    while len(Finalizados) < len(procesos):
        eventos.clear()
        line = 0

        # Asignar procesos suspendidos si hay espacio
        for proceso in Suspendidos[:]:
            particion_disponible = memoria.buscar_particion_disponible(proceso)
            if particion_disponible:
                particion_disponible.asignar_proceso(proceso)
                proceso.fragmentacion_interna_generada = particion_disponible.calcular_fragmentacion_interna()
                Listos.append(proceso)
                Suspendidos.remove(proceso)
                eventos.append(f"{line + 1}) Proceso {proceso.id} pasó de SUSPENDIDOS a LISTOS con Partición de MEMORIA {particion_disponible.id}")
                line += 1

        # Verificar procesos que deben llegar en t
        actuales = [proceso for proceso in procesos if proceso.tiempo_arribo <= t and not proceso.admitido]
        for proceso in actuales:
            particion_disponible = memoria.buscar_particion_disponible(proceso)
            if len(Listos) + int(not procesador.libre) + len(Suspendidos) < multiprogramacion:
                if particion_disponible:
                    proceso.admitir(t)
                    particion_disponible.asignar_proceso(proceso)
                    Listos.append(proceso)
                    eventos.append(f"{line + 1}) Proceso {proceso.id} llegó y está en LISTOS con Partición {particion_disponible.id}")
                    line += 1
                else:
                    proceso.admitir(t)
                    Suspendidos.append(proceso)
                    eventos.append(f"{line + 1}) Proceso {proceso.id} llegó y está en SUSPENDIDOS")
                    line += 1

        # Ejecutar si el procesador está libre y hay procesos en LISTOS
        if procesador.libre and Listos:
            proceso_actual = Listos.pop(0)
            procesador.asignar_proceso(proceso_actual)
            proceso_actual.calcular_tiempo_fragmentacion_interna_generada()
            eventos.append(f"{line + 1}) Proceso {proceso_actual.id} sale de LISTOS para ejecutarse")
            line += 1

        # Ejecutar el proceso en el procesador
        if not procesador.libre:
            procesador.ejecutar()
            if procesador.proceso.ha_terminado():
                procesador.proceso.tiempo_finalizacion = t
                Finalizados.append(procesador.proceso)
                eventos.append(f"{line + 1}) Proceso {procesador.proceso.id} finaliza")
                memoria.liberar_particion(procesador.proceso)
                procesador.liberar()
                cambios_contexto_indices.append(len(historial_estados))  # Marcamos cambio de contexto cuando se libera
            elif procesador.quantum_restante == 0 and not procesador.proceso.ha_terminado():
                Listos.append(procesador.proceso)
                eventos.append(f"{line + 1}) Proceso {procesador.proceso.id} agota el quantum y regresa a LISTOS")
                procesador.liberar()
                cambios_contexto_indices.append(len(historial_estados))  # Marcamos cambio de contexto cuando se libera

        # Guardar el estado actual en el historial
        estado_actual = ClaseEstados(
            t, copy.deepcopy(procesador), copy.deepcopy(memoria),
            copy.deepcopy(Listos), copy.deepcopy(Suspendidos),
            copy.deepcopy(Finalizados), copy.deepcopy(procesos), copy.deepcopy(eventos)
        )
        historial_estados.append(estado_actual)
        t += 1

    # Agregar un estado final extra después de la finalización de todos los procesos
    estado_final = ClaseEstados(
        t, copy.deepcopy(procesador), copy.deepcopy(memoria),
        copy.deepcopy(Listos), copy.deepcopy(Suspendidos),
        copy.deepcopy(Finalizados), copy.deepcopy(procesos), ["Simulación completada"]
    )
    historial_estados.append(estado_final)

    # Navegación entre estados
    indice_estado = 0
    while True:
        estado = historial_estados[indice_estado]
        # Pasamos ahora los nuevos parámetros a `actualizar_graficos`
        boton_rect_avanzar, boton_rect_retroceder, boton_rect_avanzar_cc, boton_rect_retroceder_cc = graficador.actualizar_graficos(
            estado.procesador, estado.memoria, estado.listos, estado.suspendidos, estado.finalizados,
            estado.t, estado.procesos, estado.eventos, indice_estado, historial_estados, cambios_contexto_indices
        )
        
        # Usar `esperar_evento_o_enter` para la acción del usuario
        accion = graficador.esperar_evento_o_enter(
            boton_rect_avanzar, boton_rect_retroceder, boton_rect_avanzar_cc,
            boton_rect_retroceder_cc, indice_estado, historial_estados, cambios_contexto_indices
        )

        if accion == 'avanzar' and indice_estado < len(historial_estados) - 1:
            indice_estado += 1
        elif accion == 'retroceder' and indice_estado > 0:
            indice_estado -= 1
        elif accion == 'avanzar_cc':
            indice_estado = next((i for i in cambios_contexto_indices if i > indice_estado), indice_estado)
        elif accion == 'retroceder_cc':
            indice_estado = next((i for i in reversed(cambios_contexto_indices) if i < indice_estado), indice_estado)

        # Condición para terminar la simulación en el último estado extra agregado
        if indice_estado == len(historial_estados) - 1:
            input("Simulación finalizada. Presiona ENTER para salir.")
            break

    graficador.cerrar_graficos()
    return Finalizados
