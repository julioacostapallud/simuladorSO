from tabulate import tabulate

def generar_informe(finalizados, listos, suspendidos, procesador, t, memoria):
    print(f"Tiempo: {t}")
    
    # Procesador
    print(f"Procesador: {'(Libre)' if procesador.libre else f'Ejecutando proceso {procesador.proceso.id}'}")

    # Memoria (tabla con las 4 particiones)
    filas_memoria = [
        [particion.id, particion.tamaño, 
         "SO" if particion.id == 1 else (particion.proceso_asignado.id if particion.proceso_asignado else '---'),
         "N/A" if particion.id == 1 else (particion.proceso_asignado.tamaño if particion.proceso_asignado else '---'),
         particion.calcular_fragmentacion_interna()] 
        for particion in memoria.particiones
    ]
    print("Memoria:")
    print(tabulate(filas_memoria, headers=["Partición ID", "Tamaño Partición", "Proceso Asignado", "Tamaño del Proceso", "Fragmentación Interna"]))

    # Cola de Listos
    print(f"Cola de listos: {[proceso.id for proceso in listos]}")

    # Cola de Suspendidos
    print(f"Cola de suspendidos: {[proceso.id for proceso in suspendidos]}")

    # Informe de procesos finalizados
    if finalizados:
        filas_procesos = [
            [proceso.id, proceso.tamaño, proceso.particion_asignada.id, 
             proceso.particion_asignada.tamaño, proceso.particion_asignada.calcular_fragmentacion_interna(),
             proceso.calcular_tiempo_retorno(), proceso.calcular_tiempo_espera()] 
            for proceso in finalizados
        ]
        print("Informe de procesos:")
        print(tabulate(filas_procesos, headers=["Proceso ID", "Tamaño del Proceso", "Partición ID", "Tamaño Partición", "Fragmentación Interna", "Tiempo de Retorno", "Tiempo de Espera"]))
    else:
        print("Informe de procesos: Ningún proceso ha finalizado todavía.")

    print("==================================================")
