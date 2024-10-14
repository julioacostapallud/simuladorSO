class Memoria:
    def __init__(self, particiones):
        self.particiones = particiones

    def buscar_particion_disponible(self, proceso):
        particion_disponible = None
        for particion in self.particiones:
            if particion.libre and particion.tamaño >= proceso.tamaño:
                if particion_disponible is None or particion.tamaño > particion_disponible.tamaño:
                    particion_disponible = particion
        return particion_disponible

    def liberar_particion(self, proceso):
        for particion in self.particiones:
            if particion.proceso_asignado == proceso:
                particion.liberar()
