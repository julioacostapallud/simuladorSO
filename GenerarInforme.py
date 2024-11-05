from tabulate import tabulate
from colorama import Fore, Style, init

init(autoreset=True)

def generar_informe(finalizados, listos, suspendidos, procesador, t, memoria, procesos):
    
    print(Fore.YELLOW + "==================================================")
    print(Fore.YELLOW + f" Estado general al finalizar el Tiempo: {t}")
    print(Fore.YELLOW + "==================================================")
    
        
   # Procesador
    if not procesador.procesoSaliente and not procesador.proceso:
        print("- PROCESADOR: Libre")
    else:
        print(f"- PROCESADOR: {f'Liberado del proceso {procesador.procesoSaliente.id} (quantum agotado)' if not procesador.proceso else f'Ejecutando proceso {procesador.proceso.id} | quantum restante {procesador.quantum_restante}'}")


    # Memoria (tabla con las 4 particiones)
    filas_memoria = [
        [particion.id, particion.tamaño, 
         "SO" if particion.id == 1 else (particion.proceso_asignado.id if particion.proceso_asignado else '---'),
         "N/A" if particion.id == 1 else (particion.proceso_asignado.tamaño if particion.proceso_asignado else '---'),
         particion.calcular_fragmentacion_interna()] 
        for particion in memoria.particiones
    ]
    print("- MEMORIA:")
    print(tabulate(filas_memoria, headers=["PAR OD", "PAR TAM", "PID", "P TAM", "FRAG INT"]))

    # Cola de Listos
    print(f"- POCESOS SOLICITANDO ADMISIÔN: {[proceso.id for proceso in procesos if proceso.tiempo_arribo <= t and not proceso.admitido]}")

    # Cola de Listos
    print(f"- COLA DE LISTOS: {[proceso.id for proceso in listos]}")

    # Cola de Suspendidos
    print(f"- COLA DE SUSPENDIDOS: {[proceso.id for proceso in suspendidos]}")

    # Informe de procesos finalizados
    if finalizados:
        filas_procesos = [
            [proceso.id, proceso.tamaño, proceso.particion_asignada.id, 
             proceso.particion_asignada.tamaño, proceso.fragmentacion_interna_generada,
             proceso.calcular_tiempo_retorno(), proceso.calcular_tiempo_espera()] 
            for proceso in finalizados
        ]
        print("- INFORME DE PROCESOS:")
        print(tabulate(filas_procesos, headers=["P ID", "TAM PRO", "PAR ID", "PAR TAM", "FRAG INT", "TR", "TE"]))
        # Acá va en formato tabla el tiempo retorno promedio, tiempo espera promedio y rendimiento del sistema
    else:
        print("- INFORME DE PROCESOS: Ningún proceso ha finalizado todavía.")

   
    print(Fore.YELLOW + "==================================================")
    print(Fore.CYAN + "==================================================")
    print(Fore.CYAN + f"Estadísticas de rendimiento del sistema en tiempo: {t}")
    print(Fore.CYAN + "==================================================")

    if finalizados:  # Verifica si hay elementos en la lista 'finalizados'
        # Cálculo de tiempos promedio
        tiempo_retorno_promedio = sum(proceso.calcular_tiempo_retorno() for proceso in finalizados) / len(finalizados)
        tiempo_espera_promedio = sum(proceso.calcular_tiempo_espera() for proceso in finalizados) / len(finalizados)
        rendimiento_sistema = len(finalizados) / t

        # Formato tabla con columnas solicitadas
        filas_estadisticas = [
            [f"{tiempo_retorno_promedio:.2f}", f"{tiempo_espera_promedio:.2f}", f"{rendimiento_sistema:.2f}"]
        ]

        # Mostrar tabla con tiempos promedio y rendimiento        
        print(tabulate(filas_estadisticas, headers=["TRP", "TEP", "Rendimiento del Sistema"]))
        
    else:
        print("No hay procesos finalizados para calcular las estadísticas.")
    
    print(Fore.CYAN + "==================================================")

    
