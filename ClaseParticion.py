class Particion:
    def __init__(self, id, tamaño, libre=True):
        self.id = id
        self.tamaño = tamaño  # Se usa "tamaño" correctamente
        self.libre = libre
        self.proceso_asignado = None

    def asignar_proceso(self, proceso):
        self.proceso_asignado = proceso
        proceso.particion_asignada = self
        self.libre = False

    def liberar(self):
        self.proceso_asignado = None
        self.libre = True

    def calcular_fragmentacion_interna(self):
        if self.proceso_asignado:
            return self.tamaño - self.proceso_asignado.tamaño
        return 0
