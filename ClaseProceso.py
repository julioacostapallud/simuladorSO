class Proceso:
    def __init__(self, id, tamaño, tiempo_arribo, tiempo_irrupcion):
        self.id = id
        self.tamaño = tamaño  # Se usa "tamaño" correctamente
        self.tiempo_arribo = tiempo_arribo
        self.tiempo_irrupcion = tiempo_irrupcion
        self.t_restante = tiempo_irrupcion
        self.tiempo_finalizacion = None
        self.particion_asignada = None
        self.fragmentacion_interna_generada = 0
        self.admitido = False  # Nuevo atributo inicializado en False

    def ha_terminado(self):
        return self.t_restante == 0

    def calcular_tiempo_retorno(self):
        return self.tiempo_finalizacion + 1 - self.tiempo_arribo

    def calcular_tiempo_espera(self):
        return self.calcular_tiempo_retorno() - self.tiempo_irrupcion

    def calcular_tiempo_fragmentacion_interna_generada(self):
        self.fragmentacion_interna_generada = self.particion_asignada.tamaño - self.tamaño

    # Método admitir modificado
    def admitir(self, nuevo_tiempo_arribo):
        self.admitido = True  # Cambia el atributo a True
        if nuevo_tiempo_arribo != self.tiempo_arribo:  # Solo cambia si es distinto
            self.tiempo_arribo = nuevo_tiempo_arribo  # Actualiza tiempo_arribo
