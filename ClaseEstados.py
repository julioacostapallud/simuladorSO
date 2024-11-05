import copy

class ClaseEstados:
    def __init__(self, t, procesador, memoria, listos, suspendidos, finalizados, procesos, eventos):
        self.t = t
        self.procesador = copy.deepcopy(procesador)  # Asumiendo que tienes métodos `copy` o puedes usar deepcopy
        self.memoria = copy.deepcopy(memoria)        # Guardamos una copia de la memoria
        self.listos = copy.deepcopy(listos)          # Hacemos una copia de la cola de listos
        self.suspendidos = copy.deepcopy(suspendidos)# Hacemos una copia de la cola de suspendidos
        self.finalizados = copy.deepcopy(finalizados)# Hacemos una copia de la lista de finalizados
        self.procesos = copy.deepcopy(procesos)# Hacemos una copia de la lista de procesos
        self.eventos = copy.deepcopy(eventos)# Hacemos una copia de la lista de eventos
