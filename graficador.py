import pygame
import sys
import os

# Importamos msvcrt para detectar ENTER en Windows
if os.name == 'nt':  # Para sistemas Windows
    import msvcrt

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla y colores (60% del tamaño original)
ancho, alto = 1200, 650
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Simulador de Sistema Operativo")
clock = pygame.time.Clock()

# Colores
COLOR_BLANCO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)
COLOR_VERDE = (0, 255, 0)
COLOR_ROJO = (255, 0, 0)
COLOR_AZUL = (0, 0, 255)
COLOR_GRIS = (200, 200, 200)
COLOR_VIOLETA = (128, 0, 128)

COLOR_BLANCO = (255, 255, 255)        # Blanco estándar
COLOR_NEGRO = (0, 0, 0)               # Negro estándar
COLOR_VERDE = (144, 238, 144)  # Verde pastel
COLOR_ROJO = (255, 182, 193)   # Rojo pastel (Rosa claro)
COLOR_AZUL = (173, 216, 230)   # Azul pastel (Azul claro)
COLOR_GRIS = (211, 211, 211)   # Gris pastel (Gris claro)
COLOR_VIOLETA = (216, 191, 216)# Violeta pastel (Lavanda)
COLOR_VIOLETA_OSCURO = (128, 0, 128)
COLOR_AMARILLO = (253, 253, 150) # Amarillo pastel (Limón suave)
COLOR_NARANJA = (255, 204, 153)# Naranja pastel (Durazno)
COLOR_ROSA = (255, 192, 203)   # Rosa pastel
COLOR_TURQUESA = (175, 238, 238)# Turquesa pastel
COLOR_LILA = (221, 160, 221)   # Lila pastel
COLOR_VERDE_MENTA = (152, 251, 152)   # Verde menta pastel
COLOR_VERDE_MENTA_OSCURO = (50, 150, 50)

COLOR_BORDE = (0, 0, 0)
COLOR_TEXTO = (0, 0, 0)


# Fuente
fuente_grande = pygame.font.SysFont(None, 30)
fuente = pygame.font.SysFont(None, 24)
fuente_pequeña = pygame.font.SysFont(None, 20)
fuente__muy_pequeña = pygame.font.SysFont(None, 16)

# Proporciones de la memoria (para las particiones)
MEMORIA_ALTO_TOTAL = 210  # Alto total de la memoria
MEMORIA_ANCHO = 80  # Ancho reducido de las particiones
MEMORIA_X = 180  # Posición X de la memoria

# Altos de las particiones en función de los porcentajes
PARTICION_ALTOS = [0.1818, 0.4545, 0.2727, 0.0909]  # Porcentajes indicados

# Desplazamiento hacia abajo de 20px
DESPLAZAMIENTO_Y = 50

# Dibujar texto en vertical
def dibujar_texto_vertical(pantalla, texto, x, y):
    for i, letra in enumerate(texto):
        texto_superficie = fuente_pequeña.render(letra, True, COLOR_VIOLETA)
        pantalla.blit(texto_superficie, (x, y + i * 20))

# Dibujar el procesador
def dibujar_procesador(pantalla, procesador, listos):
    # Rellenar el fondo del procesador con negro
    pygame.draw.rect(pantalla, COLOR_TURQUESA if procesador.libre else COLOR_AZUL, (50, 50 + DESPLAZAMIENTO_Y, 80, 80))  # Cuadro del procesador relleno

    # Texto del título "Procesador" con color negro
    texto_procesador = fuente_pequeña.render("PROCESADOR", True, COLOR_VIOLETA_OSCURO)
    pantalla.blit(texto_procesador, (45, 30 + DESPLAZAMIENTO_Y))

    

    if (procesador.libre and len(listos) > 0 and procesador.procesoSaliente is not None):
        texto_entrante = fuente.render(f"P{listos[0].id}", True, COLOR_NEGRO)
        pantalla.blit(texto_entrante, (50, 130 + DESPLAZAMIENTO_Y))
        texto_saliente = fuente.render(f"P{procesador.procesoSaliente.id}", True, COLOR_NEGRO)
        pantalla.blit(texto_saliente, (110, 130 + DESPLAZAMIENTO_Y))
        dibujar_flecha_arriba(pantalla, 55, 195)
        dibujar_flecha_abajo(pantalla, 115, 195)

    if procesador and procesador.proceso:
        # Texto del proceso en color blanco
        texto_proceso = fuente.render(f"P{procesador.proceso.id}", True, COLOR_VIOLETA_OSCURO)
        pantalla.blit(texto_proceso, (81, 80 + DESPLAZAMIENTO_Y))  # Posición centrada dentro del procesador
    else:
        if procesador.procesoSaliente is not None and listos:
            # Mostrar un cambio de contexto
            texto_libre = fuente_pequeña.render("CAMBIO DE", True, COLOR_VIOLETA_OSCURO)
            pantalla.blit(texto_libre, (52, 80 + DESPLAZAMIENTO_Y))
            texto_libre = fuente_pequeña.render("CONTEXTO", True, COLOR_VIOLETA_OSCURO)
            pantalla.blit(texto_libre, (52, 95 + DESPLAZAMIENTO_Y))
        else:
            # Mostrar un cambio de contexto
            texto_libre = fuente.render("LIBRE", True, COLOR_VIOLETA_OSCURO)
            pantalla.blit(texto_libre, (65, 80 + DESPLAZAMIENTO_Y))



# Dibujar particiones de memoria con altura proporcional y borde negro
def dibujar_memoria(pantalla, memoria):
    pygame.draw.rect(pantalla, COLOR_NEGRO, (MEMORIA_X, 50 + DESPLAZAMIENTO_Y, MEMORIA_ANCHO, MEMORIA_ALTO_TOTAL), 2)  # Contorno de la memoria
    texto_memoria = fuente_pequeña.render("MEMORIA", True, COLOR_VIOLETA_OSCURO)
    pantalla.blit(texto_memoria, (MEMORIA_X + 10, 30 + DESPLAZAMIENTO_Y))

    # Dibujar "Particiones" en vertical a la izquierda
    dibujar_texto_vertical(pantalla, "PARTICIONES", MEMORIA_X - 25, 50 + DESPLAZAMIENTO_Y)

    y = 50 + DESPLAZAMIENTO_Y
    for i, particion in enumerate(memoria.particiones):
        alto_particion = MEMORIA_ALTO_TOTAL * PARTICION_ALTOS[i]  # Alto proporcional de cada partición
        
        # Si hay un proceso asignado a la partición
        if particion.proceso_asignado:
            proceso = particion.proceso_asignado
            if proceso.tamaño == particion.tamaño:
                # Caso 1: El proceso tiene el mismo tamaño que la partición (pintar verde)
                pygame.draw.rect(pantalla, COLOR_VERDE_MENTA, (MEMORIA_X, y, MEMORIA_ANCHO, alto_particion))
                # Dibujar borde negro alrededor de cada partición
                pygame.draw.rect(pantalla, COLOR_NEGRO, (MEMORIA_X, y, MEMORIA_ANCHO, alto_particion), 2)
            elif proceso.tamaño < particion.tamaño:
                # Caso 2: Fragmentación interna (pintar la parte ocupada en verde y la parte sobrante en verde menta oscuro)
                alto_ocupado = alto_particion * (proceso.tamaño / particion.tamaño)
                alto_fragmentacion = alto_particion - alto_ocupado
                
                # Pintar la parte ocupada en verde
                pygame.draw.rect(pantalla, COLOR_VERDE_MENTA, (MEMORIA_X, y, MEMORIA_ANCHO, alto_ocupado))
                
                # Pintar la fragmentación interna en verde menta oscuro
                pygame.draw.rect(pantalla, COLOR_VERDE_MENTA_OSCURO, (MEMORIA_X, y + alto_ocupado, MEMORIA_ANCHO, alto_fragmentacion))
                
                # Dibujar puntos blancos en la parte fragmentada
                for fila in range(int(y + alto_ocupado), int(y + alto_ocupado + alto_fragmentacion), 2):  # Espaciado vertical de 2 px
                    for columna in range(MEMORIA_X, MEMORIA_X + MEMORIA_ANCHO, 2):  # Espaciado horizontal de 2 px
                        pantalla.set_at((columna, fila), COLOR_BLANCO)  # Dibujar un píxel blanco

                # Dibujar borde negro alrededor de cada partición
                pygame.draw.rect(pantalla, COLOR_NEGRO, (MEMORIA_X, y, MEMORIA_ANCHO, alto_particion), 2)
        
        else:
            # Si no hay proceso asignado, pintar la partición en naranja
            pygame.draw.rect(pantalla, COLOR_NEGRO if particion.id == 1 else COLOR_NARANJA, (MEMORIA_X, y, MEMORIA_ANCHO, alto_particion))
            # Dibujar borde negro alrededor de cada partición
            pygame.draw.rect(pantalla, COLOR_NEGRO, (MEMORIA_X, y, MEMORIA_ANCHO, alto_particion), 2)
        
        # Mostrar "SO" en la partición 1
        if particion.id == 1:
            texto_so = fuente.render("SO", True, COLOR_VIOLETA)
            pantalla.blit(texto_so, (MEMORIA_X + 30, y + 5))
        elif particion.proceso_asignado:
            # Mostrar ID del proceso asignado en otras particiones
            texto_proceso = fuente_pequeña.render(f"P{particion.proceso_asignado.id}", True, COLOR_VIOLETA_OSCURO)
            pantalla.blit(texto_proceso, (MEMORIA_X + 32, y + 5))

        # Dibujar número de partición fuera del rectángulo
        texto_numero_particion = fuente.render(f"{particion.id}", True, COLOR_ROJO)
        pantalla.blit(texto_numero_particion, (MEMORIA_X - 10, y + alto_particion // 2 - 10))  # A la izquierda, centrado verticalmente
        
        y += alto_particion  # Actualizar posición vertical

# Dibujar cola de listos alineada horizontalmente
def dibujar_cola_listos(pantalla, cola_listos):
    x, y = 300, 50 + DESPLAZAMIENTO_Y
    texto_listos = fuente_pequeña.render("COLA DE LISTOS", True, COLOR_VIOLETA_OSCURO)
    pantalla.blit(texto_listos, (280, 30 + DESPLAZAMIENTO_Y))
    # pygame.draw.line(pantalla, COLOR_NEGRO, (x - 3, y - 2), (x - 3, y + 30), 1)
    # pygame.draw.line(pantalla, COLOR_NEGRO, (x + 32, y - 2), (x + 32, y + 30), 1)
    # pygame.draw.line(pantalla, COLOR_NEGRO, (x - 3, y - 2), (x + 32, y - 2), 1)
    # pygame.draw.line(pantalla, COLOR_NEGRO, (x - 3, y + 30), (x + 32, y + 30), 1)

    for proceso in cola_listos:
        pygame.draw.rect(pantalla, COLOR_NEGRO, (x - 3, y - 3, 36, 35), 1)
        pygame.draw.rect(pantalla, COLOR_VERDE, (x, y, 30, 30))
        texto_proceso = fuente.render(f"P{proceso.id}", True, COLOR_VIOLETA_OSCURO)
        pantalla.blit(texto_proceso, (x + (5 if proceso.id < 10 else 1), y + 5))
        x += 35
    

# Dibujar cola de suspendidos alineada horizontalmente
def dibujar_cola_suspendidos(pantalla, cola_suspendidos):
    x, y = 300, 120 + DESPLAZAMIENTO_Y
    texto_suspendidos = fuente_pequeña.render("COLA DE SUSPENDIDOS", True, COLOR_VIOLETA_OSCURO)
    pantalla.blit(texto_suspendidos, (280, 100 + DESPLAZAMIENTO_Y))
    for proceso in cola_suspendidos:
        pygame.draw.rect(pantalla, COLOR_NEGRO, (x - 3, y - 3, 36, 35), 1)
        if (x + 35 > 550):
            x, y = 300, y + 40 
        pygame.draw.rect(pantalla, COLOR_GRIS, (x, y, 30, 30))
        texto_proceso = fuente_pequeña.render(f"P{proceso.id}", True, COLOR_VIOLETA_OSCURO)
        pantalla.blit(texto_proceso, (x + (5 if proceso.id < 10 else 1), y + 5))
        x += 35

# Dibujar procesos admitidos
def dibujar_procesos_no_admitidos(pantalla, procesos):
    x, y = 300, 190 + DESPLAZAMIENTO_Y
    texto_finalizados = fuente_pequeña.render("NUEVOS", True, COLOR_VIOLETA_OSCURO)
    pantalla.blit(texto_finalizados, (x - 20, 170 + DESPLAZAMIENTO_Y))
    for proceso in procesos:        
        if (x + 35 > 500):
            x, y = 300, y + 40
        pygame.draw.rect(pantalla, COLOR_NEGRO, (x - 3, y - 3, 36, 35), 1)
        pygame.draw.rect(pantalla, COLOR_AMARILLO, (x, y, 30, 30))
        texto_proceso = fuente.render(f"P{proceso.id}", True, COLOR_VIOLETA_OSCURO)
        pantalla.blit(texto_proceso, (x + (5 if proceso.id < 10 else 1), y + 5))
        x += 35

# Dibujar procesos finalizados en la parte inferior
def dibujar_procesos_finalizados(pantalla, finalizados):
    x, y = 20, 300 + DESPLAZAMIENTO_Y
    texto_finalizados = fuente_pequeña.render("PROCESOS FINALIZADOS", True, COLOR_VIOLETA_OSCURO)
    pantalla.blit(texto_finalizados, (x, y - 75 + DESPLAZAMIENTO_Y))
    for proceso in finalizados:
        if (x + 35 > 550):
            x, y = 50, y + 40
        pygame.draw.rect(pantalla, COLOR_NEGRO, (x, y, 30, 30))
        texto_proceso = fuente.render(f"P{proceso.id}", True, COLOR_BLANCO)
        pantalla.blit(texto_proceso, (x + (5 if proceso.id < 10 else 1), y + 5))
        x += 35

def dibujar_botones(t, procesos, indice_estado, historial_estados, cambios_contexto_indices):
    boton_rect_avanzar, boton_rect_retroceder = None, None
    boton_rect_avanzar_cc, boton_rect_retroceder_cc = None, None

    # Botón para avanzar: solo se muestra si queda algún proceso sin finalizar
    if any(proceso.tiempo_finalizacion is None for proceso in procesos) and indice_estado < len(historial_estados) - 1:
        boton_rect_avanzar = pygame.Rect(ancho - 190, 35, 85, 20)
        pygame.draw.rect(pantalla, COLOR_AZUL if t > -1 else COLOR_VERDE, boton_rect_avanzar)
        texto_boton_avanzar = fuente_pequeña.render(f"{'Avanzar' if t > -1 else 'Iniciar'}", True, COLOR_NEGRO)
        pantalla.blit(texto_boton_avanzar, (ancho - 172, 38))

    # Botón para retroceder: solo se muestra si no estamos en el primer estado
    if indice_estado > 0:
        boton_rect_retroceder = pygame.Rect(ancho - 285, 35, 85, 20)
        pygame.draw.rect(pantalla, COLOR_AZUL, boton_rect_retroceder)
        texto_boton_retroceder = fuente_pequeña.render("Retroceder", True, COLOR_NEGRO)
        pantalla.blit(texto_boton_retroceder, (ancho - 275, 38))

    # Botón para avanzar a cambio de contexto: solo si existe un cambio de contexto después del estado actual
    if any(i > indice_estado for i in cambios_contexto_indices):
        boton_rect_avanzar_cc = pygame.Rect(ancho - 95, 35, 90, 20)
        pygame.draw.rect(pantalla, COLOR_ROJO, boton_rect_avanzar_cc)
        texto_boton_avanzar_cc = fuente_pequeña.render("Avanzar CC", True, COLOR_NEGRO)
        pantalla.blit(texto_boton_avanzar_cc, (ancho - 87, 38))

    # Botón para retroceder a cambio de contexto: solo si existe un cambio de contexto antes del estado actual
    if any(i < indice_estado for i in cambios_contexto_indices):
        boton_rect_retroceder_cc = pygame.Rect(ancho - 405, 35, 110, 20)
        pygame.draw.rect(pantalla, COLOR_ROJO, boton_rect_retroceder_cc)
        texto_boton_retroceder_cc = fuente_pequeña.render("Retroceder CC", True, COLOR_NEGRO)
        pantalla.blit(texto_boton_retroceder_cc, (ancho - 395, 38))

    return boton_rect_avanzar, boton_rect_retroceder, boton_rect_avanzar_cc, boton_rect_retroceder_cc



def edge(pantalla, x, y):
    pygame.draw.line(pantalla, COLOR_NEGRO, (x - 5, y), (x, y), 1)
    pygame.draw.line(pantalla, COLOR_NEGRO, (x - 5, y), (x - 5, y - 45), 1)
    pygame.draw.line(pantalla, COLOR_NEGRO, (x - 5, y - 45), (x + 170, y - 45), 1)
    pygame.draw.line(pantalla, COLOR_NEGRO, (x + 170, y - 45), (x + 170, y - 70), 1)
    pygame.draw.line(pantalla, COLOR_NEGRO, (x + 160, y - 70), (x + 170, y - 70), 1)
    dibujar_flecha_izquierda(pantalla, x + 145, y - 75)


def dibujar_flecha_izquierda(pantalla, x, y):
    # Definir los puntos de la flecha hacia la izquierda (triángulo)
    puntos_flecha = [(x + 20, y), (x, y + 5), (x + 20, y + 10)]  # Alto 10px, Ancho 20px
    
    # Dibujar la flecha en la pantalla
    pygame.draw.polygon(pantalla, COLOR_NEGRO, puntos_flecha)

def dibujar_flecha_arriba(pantalla, x, y):
    # Definir los puntos de la flecha hacia arriba (triángulo)
    puntos_flecha = [(x, y + 20), (x + 5, y), (x + 10, y + 20)]  # Alto 20px, Ancho 10px
    
    # Dibujar la flecha en la pantalla
    pygame.draw.polygon(pantalla, COLOR_VERDE, puntos_flecha)

def dibujar_flecha_abajo(pantalla, x, y):
    # Definir los puntos de la flecha hacia abajo (triángulo)
    puntos_flecha = [(x, y), (x + 5, y + 20), (x + 10, y)]  # Alto 20px, Ancho 10px
    
    # Dibujar la flecha en la pantalla
    pygame.draw.polygon(pantalla, COLOR_ROJO, puntos_flecha)

def centrar_texto_en_casilla(texto, fuente, x, ancho_celda):
    # Obtener el ancho del texto
    texto_ancho, _ = fuente.size(texto)
    # Calcular la posición x donde debe comenzar el texto para estar centrado
    x_centrado = x + (ancho_celda - texto_ancho) // 2
    return x_centrado

def dibujar_tabla_memoria(pantalla, filas, headers):
    x = 500
    y = 100
    ancho_total = 450  # Ajustamos el ancho total para acomodar las nuevas columnas
    alto_fila = 25  # Altura fija para las filas
    particion_inicio = 0  # Para llevar la cuenta del inicio de cada partición
    
    # Definir los anchos de cada columna según lo solicitado
    anchos_columnas = {
        "ID": 0.08,        # 8%
        "INI": 0.15,       # 16%
        "FIN": 0.15,       # 16%
        "PAR TAM": 0.18,   # 16%
        "PID": 0.08,       # 8%
        "PTAM": 0.16,      # 16%
        "FRAG INT": 0.20   # 20%
    }
    
    # Calcular el ancho de cada columna basado en el ancho total y los porcentajes definidos
    anchos = [int(ancho_total * anchos_columnas[col]) for col in headers]

    # Dibujar encabezados
    header_y = y
    for i, header in enumerate(headers):
        x_centrado = centrar_texto_en_casilla(header, fuente, x + sum(anchos[:i]), anchos[i])
        texto = fuente.render(header, True, COLOR_TEXTO)
        pantalla.blit(texto, (x_centrado, header_y + 5))
        pygame.draw.rect(pantalla, COLOR_BORDE, (x + sum(anchos[:i]), header_y, anchos[i], alto_fila), 1)

    # Dibujar filas con los cálculos de INICIO y FIN
    for fila_idx, fila in enumerate(filas):
        fila_y = y + alto_fila * (fila_idx + 1)  # Cada fila debajo del encabezado
        
        # Extraer el tamaño de la partición de la fila
        particion_tamaño = int(fila[1].replace("KB", ""))  # Columna de tamaño de partición
        
        # Calcular el valor de INICIO y FIN
        particion_fin = particion_inicio + particion_tamaño - 1
        
        # Insertar INICIO y FIN en las posiciones correctas
        fila.insert(1, f"{particion_inicio}KB")  # INICIO
        fila.insert(2, f"{particion_fin}KB")     # FIN
        
        # Dibujar los valores de la fila
        for col_idx, valor in enumerate(fila):
            x_centrado = centrar_texto_en_casilla(str(valor), fuente, x + sum(anchos[:col_idx]), anchos[col_idx])
            texto = fuente.render(str(valor), True, COLOR_TEXTO)
            pantalla.blit(texto, (x_centrado, fila_y + 5))
            pygame.draw.rect(pantalla, COLOR_BORDE, (x + sum(anchos[:col_idx]), fila_y, anchos[col_idx], alto_fila), 1)

        # Actualizar el inicio de la siguiente partición
        particion_inicio = particion_fin + 1

def dibujar_tabla_procesos(pantalla, filas, headers):
    x = 500
    y = 270  # Colocamos la tabla de procesos más abajo
    alto_fila = 30  # Altura de cada fila
    margen = 3  # Margen de 3 píxeles a cada lado del texto

    # Calcular el ancho de cada columna basado en el texto del encabezado más 3 píxeles de cada lado
    anchos_columnas = []
    for header in headers:
        ancho_texto = fuente.size(header)[0]  # Obtener el ancho del texto del encabezado
        anchos_columnas.append(ancho_texto + 2 * margen)  # Sumar margen a cada lado

    # Dibujar encabezados
    header_y = y
    x_pos = x
    for i, header in enumerate(headers):
        ancho_columna = anchos_columnas[i]
        x_centrado = centrar_texto_en_casilla(header, fuente, x_pos, ancho_columna)
        texto = fuente.render(header, True, COLOR_TEXTO)
        pantalla.blit(texto, (x_centrado, header_y + 5))
        pygame.draw.rect(pantalla, COLOR_BORDE, (x_pos, header_y, ancho_columna, alto_fila), 1)
        x_pos += ancho_columna  # Moverse a la siguiente posición en x

    # Dibujar filas
    for fila_idx, fila in enumerate(filas):
        fila_y = y + alto_fila * (fila_idx + 1)  # Cada fila debajo del encabezado
        x_pos = x  # Reiniciar x_pos para cada fila
        for col_idx, valor in enumerate(fila):
            ancho_columna = anchos_columnas[col_idx]
            x_centrado = centrar_texto_en_casilla(str(valor), fuente, x_pos, ancho_columna)
            texto = fuente.render(str(valor), True, COLOR_TEXTO)
            pantalla.blit(texto, (x_centrado, fila_y + 5))
            pygame.draw.rect(pantalla, COLOR_BORDE, (x_pos, fila_y, ancho_columna, alto_fila), 1)
            x_pos += ancho_columna  # Moverse a la siguiente posición en x para la siguiente columna

def dibujar_eventos(pantalla, eventos, comienzo_x, comienzo_y, ancho, cortar_texto=True, t=None):
    # Configuración de la altura de cada línea de texto
    alto_linea = 25  # Altura de cada línea de texto
    margen_x = 10  # Margen a la izquierda de los eventos
    margen_y = 5   # Margen arriba de cada línea
    y_actual = comienzo_y  # Iniciar en la posición vertical indicada

    # Dibujar encabezado "Eventos"
    texto_encabezado = fuente_pequeña.render(f"EVENTOS DE {t} A {t+1}", True, COLOR_VIOLETA_OSCURO)  # Corregido el f-string
    pantalla.blit(texto_encabezado, (comienzo_x + margen_x, y_actual))  # Colocar el encabezado
    y_actual += alto_linea  # Pasar a la siguiente línea después del encabezado

    # Dibujar los eventos
    for evento in eventos:
        if cortar_texto:
            # Dividir el texto si es más largo que el ancho disponible
            palabras = evento.split(" ")
            linea_actual = ""
            for palabra in palabras:
                # Verificar si la palabra cabe en la línea actual
                if fuente__muy_pequeña.size(linea_actual + palabra)[0] < (ancho - 2 * margen_x):
                    linea_actual += palabra + " "  # Añadir la palabra a la línea actual
                else:
                    # Si no cabe, dibujar la línea actual y empezar una nueva
                    texto_evento = fuente__muy_pequeña.render(linea_actual, True, COLOR_TEXTO)
                    pantalla.blit(texto_evento, (comienzo_x + margen_x, y_actual))
                    y_actual += alto_linea
                    linea_actual = palabra + " "  # Iniciar nueva línea con la palabra actual
            
            # Dibujar la última línea de texto
            if linea_actual:
                texto_evento = fuente__muy_pequeña.render(linea_actual, True, COLOR_TEXTO)
                pantalla.blit(texto_evento, (comienzo_x + margen_x, y_actual))
                y_actual += alto_linea
        else:
            # Si no cortamos el texto, dibujarlo tal como está
            texto_evento = fuente__muy_pequeña.render(evento, True, COLOR_TEXTO)
            pantalla.blit(texto_evento, (comienzo_x + margen_x, y_actual))
            y_actual += alto_linea

        pygame.draw.line(pantalla, COLOR_NEGRO, (comienzo_x + 10, y_actual - 8), (1190, y_actual - 8), 1)  # Línea horizontal    
    

def dibujar_tabla_rendimiento(pantalla, filas, headers):
    x = 960  # Ajustar la posición horizontal al final de la tabla de memoria
    y = 100  # Ajustar la posición vertical según sea necesario
    ancho_total = 220  # Ancho total de la tabla de rendimiento
    alto_fila = 30  # Altura de cada fila

    # Definir el ancho de cada columna según los porcentajes deseados
    ancho_columna_1 = int(ancho_total * 0.15)  # 15% para PF
    ancho_columna_2 = int(ancho_total * 0.20)  # 20% para TRP
    ancho_columna_3 = int(ancho_total * 0.20)  # 20% para TEP
    ancho_columna_4 = int(ancho_total * 0.45)  # 45% para Rendimiento

    # Dibujar encabezados
    header_y = y
    for i, header in enumerate(headers):
        # Ajustar el ancho según la columna
        if i == 0:
            ancho_columna = ancho_columna_1
        elif i == 1:
            ancho_columna = ancho_columna_2
        elif i == 2:
            ancho_columna = ancho_columna_3
        else:
            ancho_columna = ancho_columna_4

        x_centrado = centrar_texto_en_casilla(header, fuente, x, ancho_columna)
        texto = fuente.render(header, True, COLOR_TEXTO)
        pantalla.blit(texto, (x_centrado, header_y + 5))
        pygame.draw.rect(pantalla, COLOR_BORDE, (x, header_y, ancho_columna, alto_fila), 1)

        # Actualizar la posición x para la siguiente columna
        x += ancho_columna

    # Dibujar filas
    for fila_idx, fila in enumerate(filas):
        fila_y = y + alto_fila * (fila_idx + 1)  # Cada fila debajo del encabezado
        x = 960  # Restablecer x para la primera columna de la fila
        for col_idx, valor in enumerate(fila):
            # Ajustar el ancho según la columna
            if col_idx == 0:
                ancho_columna = ancho_columna_1
            elif col_idx == 1:
                ancho_columna = ancho_columna_2
            elif col_idx == 2:
                ancho_columna = ancho_columna_3
            else:
                ancho_columna = ancho_columna_4

            x_centrado = centrar_texto_en_casilla(str(valor), fuente, x, ancho_columna)
            texto = fuente.render(str(valor), True, COLOR_TEXTO)
            pantalla.blit(texto, (x_centrado, fila_y + 5))
            pygame.draw.rect(pantalla, COLOR_BORDE, (x, fila_y, ancho_columna, alto_fila), 1)

            # Actualizar la posición x para la siguiente columna
            x += ancho_columna

def generar_array_memoria(memoria):
    filas_memoria = [
        [particion.id, 
         f"{particion.tamaño}KB", 
         "SO" if particion.id == 1 else (particion.proceso_asignado.id if particion.proceso_asignado else '---'),
         "N/A" if particion.id == 1 else (f"{particion.proceso_asignado.tamaño}KB" if particion.proceso_asignado else '---'),
         f"{particion.calcular_fragmentacion_interna()}KB" if particion.proceso_asignado else "N/A"]
        for particion in memoria.particiones
    ]
    return filas_memoria

def generar_array_procesos(finalizados):
    filas_procesos = [
        [
            proceso.id, 
            f"{proceso.tamaño}KB", 
            proceso.particion_asignada.id if proceso.particion_asignada else '---', 
            f"{proceso.particion_asignada.tamaño}KB" if proceso.particion_asignada else '---', 
            f"{proceso.fragmentacion_interna_generada}KB" if proceso.fragmentacion_interna_generada else '---', 
            f"{proceso.calcular_tiempo_retorno()}",
            f"{proceso.calcular_tiempo_espera()}"
        ] 
        for proceso in finalizados
    ]
    return filas_procesos

def generar_array_rendimiento(finalizados):
    # Cálculo de tiempos promedio
    tiempo_retorno_promedio = sum(proceso.calcular_tiempo_retorno() for proceso in finalizados) / len(finalizados)
    tiempo_espera_promedio = sum(proceso.calcular_tiempo_espera() for proceso in finalizados) / len(finalizados)

    # Obtener el tiempo de finalización máximo entre los procesos finalizados
    ultimo_t_finalizacion = max(proceso.tiempo_finalizacion for proceso in finalizados)

    # Calcular rendimiento usando solo el último tiempo de finalización
    rendimiento_sistema = len(finalizados) / ultimo_t_finalizacion if ultimo_t_finalizacion > 0 else 0

    # Formato tabla con columnas solicitadas
    filas_rendimiento = [
        [len(finalizados), f"{tiempo_retorno_promedio:.2f}", f"{tiempo_espera_promedio:.2f}", f"{rendimiento_sistema:.2f} P/UT"]
    ]
    return filas_rendimiento


# Función para dibujar los procesos en filas de 5
def dibujar_procesos(pantalla, procesos, t, x, y, l):
    separacion = 5  # Separación de 5px entre los cuadrados
    for i, proceso in enumerate(procesos):
        fila = i // 5  # Determinar en qué fila va el proceso
        columna = i % 5  # Determinar en qué columna va el proceso
        pos_x = x + columna * (l + separacion)
        pos_y = y + fila * (l + separacion)
        
        # Dibujar fondo gris del cuadrado
        pygame.draw.rect(pantalla, COLOR_GRIS if proceso.tiempo_arribo > t else COLOR_NEGRO if proceso.tiempo_finalizacion != None else COLOR_VERDE if proceso.admitido else COLOR_AMARILLO, (pos_x, pos_y, l, l))
        # Dibujar borde negro del cuadrado
        pygame.draw.rect(pantalla, COLOR_NEGRO, (pos_x, pos_y, l, l), 2)

        # Dibujar la información dentro del cuadrado
        fuente = pygame.font.SysFont(None, 20)

        # Dibujar ID del proceso en el centro
        texto_id = fuente_grande.render(str(proceso.id), True, COLOR_NEGRO if proceso.tiempo_finalizacion == None else COLOR_BLANCO)
        pantalla.blit(texto_id, (pos_x + l//2 - texto_id.get_width()//2, pos_y + 25))

        # Dibujar el estado del proceso (Admitido o No Admitido)
        estado = "No arribado" if proceso.tiempo_arribo > t else "Terminado" if proceso.tiempo_finalizacion != None else "Admitido" if proceso.admitido else "Espera"
        

        texto_estado = fuente.render(estado, True, COLOR_NEGRO if proceso.tiempo_finalizacion == None else COLOR_BLANCO)
        pantalla.blit(texto_estado, (pos_x + l//2 - texto_estado.get_width()//2, pos_y + 45))

        # Dibujar el tamaño del proceso
        texto_tamano = fuente.render(f"{proceso.tamaño}KB", True, COLOR_NEGRO if proceso.tiempo_finalizacion == None else COLOR_BLANCO)
        pantalla.blit(texto_tamano, (pos_x + l//2 - texto_tamano.get_width()//2, pos_y + 65))

        # Dibujar tiempos de arribo y de irrupción en las esquinas
        texto_arribo = fuente.render(f"A:{proceso.tiempo_arribo}", True, COLOR_NEGRO if proceso.tiempo_finalizacion == None else COLOR_BLANCO)
        pantalla.blit(texto_arribo, (pos_x + 5, pos_y + 5))

        texto_irrupcion = fuente.render(f"I:{proceso.tiempo_irrupcion}", True, COLOR_NEGRO if proceso.tiempo_finalizacion == None else COLOR_BLANCO)
        pantalla.blit(texto_irrupcion, (pos_x + l - texto_irrupcion.get_width() - 5, pos_y + 5))

# Función principal para actualizar los gráficos
def actualizar_graficos(procesador, memoria, cola_listos, cola_suspendidos, finalizados, t, procesos, eventos, indice_estado, historial_estados, cambios_contexto_indices):
    # Limpiar pantalla
    pantalla.fill(COLOR_BLANCO)

    texto_titulo = fuente_grande.render(f"SIMULADOR", True, COLOR_NEGRO)
    pantalla.blit(texto_titulo, (550, 10))

    texto_subtitulo1 = fuente_pequeña.render(f"Planificación de CPU: ", True, COLOR_NEGRO)
    pantalla.blit(texto_subtitulo1, (10, 10))
    texto_subtitulo1 = fuente_pequeña.render(f"ROUND-ROBIN Q=3", True, COLOR_VIOLETA_OSCURO)
    pantalla.blit(texto_subtitulo1, (155, 10))
    texto_subtitulo2 = fuente_pequeña.render(f"Política de asignación de memoria: ", True, COLOR_NEGRO)
    pantalla.blit(texto_subtitulo2, (10, 25))
    texto_subtitulo2 = fuente_pequeña.render(f"WORST-FIT", True, COLOR_VIOLETA_OSCURO)
    pantalla.blit(texto_subtitulo2, (240, 25))
    texto_subtitulo3 = fuente_pequeña.render(f"Grado de Multiprogramación: ", True, COLOR_NEGRO)
    pantalla.blit(texto_subtitulo3, (10, 40))
    texto_subtitulo3 = fuente_pequeña.render(f"5 PROCESOS", True, COLOR_VIOLETA_OSCURO)
    pantalla.blit(texto_subtitulo3, (205, 40))

    texto_antes = fuente_grande.render("Rango de Tiempo:", True, COLOR_NEGRO)
    pantalla.blit(texto_antes, (ancho - 320, 10))
    # texto_t = fuente_grande.render(f"{t if t > -1 else '-'}", True, COLOR_VIOLETA_OSCURO)
    texto_t = fuente_grande.render(f"{t if t > -1 else '-'}...{t + 1 if t > -1 else '-'}", True, COLOR_VIOLETA_OSCURO)
    pantalla.blit(texto_t, (ancho - 130, 10))

    # Dibujar componentes del simulador
    dibujar_procesador(pantalla, procesador, cola_listos)
    dibujar_memoria(pantalla, memoria)
    dibujar_cola_listos(pantalla, cola_listos)
    dibujar_cola_suspendidos(pantalla, cola_suspendidos)
    dibujar_procesos_no_admitidos(pantalla, [p for p in procesos if p.tiempo_arribo <= t and not p.admitido])
    dibujar_procesos_finalizados(pantalla, finalizados)
    dibujar_flecha_izquierda(pantalla, 275, 110)
    dibujar_flecha_izquierda(pantalla, 275, 180)
    edge(pantalla, 275, 185)
    dibujar_flecha_izquierda(pantalla, 275, 250)
    edge(pantalla, 275, 255)

    filas_memoria = generar_array_memoria(memoria)
    headers_memoria = ["ID","INI", "FIN", "PAR TAM", "PID", "PTAM", "FRAG INT"]
    texto_memoria = fuente_pequeña.render("TABLA DE MEMORIA", True, COLOR_VIOLETA_OSCURO)
    pantalla.blit(texto_memoria, (500, 80))
    dibujar_tabla_memoria(pantalla, filas_memoria, headers_memoria)

    filas_procesos = generar_array_procesos(finalizados)
    headers_procesos = ["PID", "TAM PRO", "PAR ID", "PAR TAM", "FRAG INT", "TR", "TE"]
    texto_procesos = fuente_pequeña.render("INFORMACIÓN DE PROCESOS", True, COLOR_VIOLETA_OSCURO)
    pantalla.blit(texto_procesos, (500, 245))
    dibujar_tabla_procesos(pantalla, filas_procesos, headers_procesos)

    texto_rendimiento = fuente_pequeña.render("ESTADISTICAS", True, COLOR_VIOLETA_OSCURO)
    pantalla.blit(texto_rendimiento, (960, 80))
    if len(finalizados) > 0:
        filas_rendimiento = generar_array_rendimiento(finalizados)
        headers_rendimiento = ["PF", "TRP", "TEP", "RENDIM."]
        dibujar_tabla_rendimiento(pantalla, filas_rendimiento, headers_rendimiento)

    dibujar_eventos(pantalla, eventos, comienzo_x=900, comienzo_y=245, ancho=285, cortar_texto=True, t=t)

    pygame.draw.line(pantalla, COLOR_NEGRO, (490, 80), (490, 620), 2)
    pygame.draw.line(pantalla, COLOR_NEGRO, (955, 80), (955, 230), 2)
    pygame.draw.line(pantalla, COLOR_NEGRO, (900, 240), (900, 620), 2)
    pygame.draw.line(pantalla, COLOR_NEGRO, (20, 65), (1180, 65), 2)
    pygame.draw.line(pantalla, COLOR_NEGRO, (20, 320), (480, 320), 2)
    pygame.draw.line(pantalla, COLOR_NEGRO, (20, 390), (480, 390), 2)
    pygame.draw.line(pantalla, COLOR_NEGRO, (500, 235), (1180, 235), 2)
    pygame.draw.line(pantalla, COLOR_NEGRO, (20, 630), (1180, 630), 2)

    pygame.draw.line(pantalla, COLOR_NEGRO, (791, 60), (1197, 60), 2)
    pygame.draw.line(pantalla, COLOR_NEGRO, (791, 5), (1197, 5), 2)
    pygame.draw.line(pantalla, COLOR_NEGRO, (791, 5), (791, 60), 2)
    pygame.draw.line(pantalla, COLOR_NEGRO, (1197, 5), (1197, 60), 2)

    texto_finalizados = fuente_pequeña.render("DATOS DE PROCESOS", True, COLOR_VIOLETA_OSCURO)
    pantalla.blit(texto_finalizados, (20, 405))
    dibujar_procesos(pantalla, procesos, t, 20, 435, 85)

    # Dibujar los botones con las condiciones actualizadas
    boton_rect_avanzar, boton_rect_retroceder, boton_rect_avanzar_cc, boton_rect_retroceder_cc = dibujar_botones(
        t, procesos, indice_estado, historial_estados, cambios_contexto_indices
    )

    # Actualizar pantalla
    pygame.display.flip()
    clock.tick(60)

    return boton_rect_avanzar, boton_rect_retroceder, boton_rect_avanzar_cc, boton_rect_retroceder_cc

# Esperar a que el usuario presione el botón en Pygame o ENTER en la terminal
def esperar_evento_o_enter(boton_rect_avanzar, boton_rect_retroceder, boton_rect_avanzar_cc, boton_rect_retroceder_cc, indice_estado, historial_estados, cambios_contexto_indices):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cerrar_graficos()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect_avanzar and boton_rect_avanzar.collidepoint(event.pos):
                    return 'avanzar'
                
                elif boton_rect_retroceder and boton_rect_retroceder.collidepoint(event.pos):
                    if indice_estado > 0:
                        return 'retroceder'
                
                elif boton_rect_avanzar_cc and boton_rect_avanzar_cc.collidepoint(event.pos):
                    return 'avanzar_cc'
                
                elif boton_rect_retroceder_cc and boton_rect_retroceder_cc.collidepoint(event.pos):
                    return 'retroceder_cc'

        pygame.time.Clock().tick(60)

# Función para cerrar Pygame
def cerrar_graficos():
    pygame.quit()