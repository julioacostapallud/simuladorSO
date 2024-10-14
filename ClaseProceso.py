class Proceso:
    def __init__(self, id, tamaño, tiempo_arribo, tiempo_irrupcion):
        self.id = id
        self.tamaño = tamaño  # Se usa "tamaño" correctamente
        self.tiempo_arribo = tiempo_arribo
        self.tiempo_irrupcion = tiempo_irrupcion
        self.t_restante = tiempo_irrupcion
        self.tiempo_finalizacion = None
        self.particion_asignada = None

    def ha_terminado(self):
        return self.t_restante == 0

    def calcular_tiempo_retorno(self):
        return self.tiempo_finalizacion - self.tiempo_arribo

    def calcular_tiempo_espera(self):
        return self.calcular_tiempo_retorno() - self.tiempo_irrupcion
