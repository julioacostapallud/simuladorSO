class Procesador:
    def __init__(self, quantum):
        self.quantum = quantum
        self.quantum_restante = quantum
        self.proceso = None
        self.procesoSaliente = None
        self.libre = True

    def asignar_proceso(self, proceso):
        self.proceso = proceso
        self.quantum_restante = self.quantum
        self.libre = False

    def ejecutar(self):
        if self.proceso:
            tiempo_a_ejecutar = min(1, self.proceso.t_restante, self.quantum_restante)
            self.proceso.t_restante -= tiempo_a_ejecutar
            self.quantum_restante -= tiempo_a_ejecutar

    def liberar(self):
        self.procesoSaliente = self.proceso
        self.proceso = None
        self.libre = True
