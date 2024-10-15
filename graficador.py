import pygame
import sys
import os

# Importamos msvcrt para detectar ENTER en Windows
if os.name == 'nt':  # Para sistemas Windows
    import msvcrt

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla y colores (60% del tamaño original)
ancho, alto = 600, 480
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

# Fuente
fuente = pygame.font.SysFont(None, 24)
fuente_pequena = pygame.font.SysFont(None, 20)

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
        texto_superficie = fuente_pequena.render(letra, True, COLOR_VIOLETA)
        pantalla.blit(texto_superficie, (x, y + i * 20))

# Dibujar el procesador
def dibujar_procesador(pantalla, procesador):
    # Rellenar el fondo del procesador con negro
    pygame.draw.rect(pantalla, COLOR_NEGRO, (50, 50 + DESPLAZAMIENTO_Y, 80, 80))  # Cuadro del procesador relleno

    # Texto del título "Procesador" con color negro
    texto_procesador = fuente.render("Procesador", True, COLOR_NEGRO)
    pantalla.blit(texto_procesador, (50, 30 + DESPLAZAMIENTO_Y))

    if procesador and procesador.proceso:
        # Texto del proceso en color blanco
        texto_proceso = fuente.render(f"{procesador.proceso.id}", True, COLOR_BLANCO)
        pantalla.blit(texto_proceso, (85, 80 + DESPLAZAMIENTO_Y))  # Posición centrada dentro del procesador
    else:
        # Mostrar un cuadro vacío si no hay proceso, en color blanco
        texto_libre = fuente.render("LIBRE", True, COLOR_BLANCO)
        pantalla.blit(texto_libre, (65, 80 + DESPLAZAMIENTO_Y))

# Dibujar particiones de memoria con altura proporcional y borde negro
def dibujar_memoria(pantalla, memoria):
    pygame.draw.rect(pantalla, COLOR_NEGRO, (MEMORIA_X, 50 + DESPLAZAMIENTO_Y, MEMORIA_ANCHO, MEMORIA_ALTO_TOTAL), 2)  # Contorno de la memoria
    texto_memoria = fuente.render("Memoria", True, COLOR_NEGRO)
    pantalla.blit(texto_memoria, (MEMORIA_X + 10, 30 + DESPLAZAMIENTO_Y))

    # Dibujar "Particiones" en vertical a la izquierda
    dibujar_texto_vertical(pantalla, "PARTICIONES", MEMORIA_X - 25, 50 + DESPLAZAMIENTO_Y)

    y = 50 + DESPLAZAMIENTO_Y
    for i, particion in enumerate(memoria.particiones):
        alto_particion = MEMORIA_ALTO_TOTAL * PARTICION_ALTOS[i]  # Alto proporcional de cada partición
        
        # Dibujar partición (fondo)
        pygame.draw.rect(pantalla, COLOR_GRIS if particion.proceso_asignado is None else COLOR_VERDE, (MEMORIA_X, y, MEMORIA_ANCHO, alto_particion))
        
        # Dibujar borde negro alrededor de cada partición
        pygame.draw.rect(pantalla, COLOR_NEGRO, (MEMORIA_X, y, MEMORIA_ANCHO, alto_particion), 2)

        # Mostrar "SO" en la partición 1
        if particion.id == 1:
            texto_so = fuente.render("SO", True, COLOR_NEGRO)
            pantalla.blit(texto_so, (MEMORIA_X + 30, y + 5))
        elif particion.proceso_asignado:
            # Mostrar ID del proceso asignado en otras particiones
            texto_proceso = fuente.render(f"{particion.proceso_asignado.id}", True, COLOR_NEGRO)
            pantalla.blit(texto_proceso, (MEMORIA_X + 35, y + 5))

        # Dibujar número de partición fuera del rectángulo
        texto_numero_particion = fuente.render(f"{particion.id}", True, COLOR_VIOLETA)
        pantalla.blit(texto_numero_particion, (MEMORIA_X - 10, y + alto_particion // 2 - 10))  # A la izquierda, centrado verticalmente
        
        y += alto_particion  # Actualizar posición vertical


# Dibujar cola de listos alineada horizontalmente
def dibujar_cola_listos(pantalla, cola_listos):
    x, y = 280, 50 + DESPLAZAMIENTO_Y
    texto_listos = fuente.render("Cola de Listos", True, COLOR_NEGRO)
    pantalla.blit(texto_listos, (280, 30 + DESPLAZAMIENTO_Y))
    for proceso in cola_listos:
        pygame.draw.rect(pantalla, COLOR_AZUL, (x, y, 30, 30))
        texto_proceso = fuente.render(f"{proceso.id}", True, COLOR_BLANCO)
        pantalla.blit(texto_proceso, (x + 10, y + 5))
        x += 35

# Dibujar cola de suspendidos alineada horizontalmente
def dibujar_cola_suspendidos(pantalla, cola_suspendidos):
    x, y = 280, 120 + DESPLAZAMIENTO_Y
    texto_suspendidos = fuente.render("Cola de Suspendidos", True, COLOR_NEGRO)
    pantalla.blit(texto_suspendidos, (280, 100 + DESPLAZAMIENTO_Y))
    for proceso in cola_suspendidos:
        if (x + 35 > 550):
            x, y = 280, y + 40 
        pygame.draw.rect(pantalla, COLOR_ROJO, (x, y, 30, 30))
        texto_proceso = fuente.render(f"{proceso.id}", True, COLOR_BLANCO)
        pantalla.blit(texto_proceso, (x + 10, y + 5))
        x += 35

# Dibujar procesos finalizados en la parte inferior
def dibujar_procesos_finalizados(pantalla, finalizados):
    x, y = 50, 300 + DESPLAZAMIENTO_Y
    texto_finalizados = fuente.render("Procesos Finalizados", True, COLOR_NEGRO)
    pantalla.blit(texto_finalizados, (50, 280 + DESPLAZAMIENTO_Y))
    for proceso in finalizados:
        if (x + 35 > 550):
            x, y = 50, y + 40
        pygame.draw.rect(pantalla, COLOR_GRIS, (x, y, 30, 30))
        texto_proceso = fuente.render(f"{proceso.id}", True, COLOR_NEGRO)
        pantalla.blit(texto_proceso, (x + 10, y + 5))
        x += 35

# Dibujar botón de avanzar
def dibujar_boton():
    # Botón para avanzar
    boton_rect = pygame.Rect(465, 10, 100, 40)
    pygame.draw.rect(pantalla, COLOR_VERDE, boton_rect)
    texto_boton = fuente.render("Avanzar", True, COLOR_BLANCO)
    pantalla.blit(texto_boton, (480, 20 ))
    return boton_rect

# Función principal para actualizar los gráficos
def actualizar_graficos(procesador, memoria, cola_listos, cola_suspendidos, finalizados, t):
    # Limpiar pantalla
    pantalla.fill(COLOR_BLANCO)

    # Dibujar "Tiempo de Simulación"
    texto_tiempo_unidad = fuente.render(f"Tiempo Simulación {t}", True, COLOR_ROJO)
    pantalla.blit(texto_tiempo_unidad, (200, 10))

    # Dibujar componentes del simulador
    dibujar_procesador(pantalla, procesador)
    dibujar_memoria(pantalla, memoria)
    dibujar_cola_listos(pantalla, cola_listos)
    dibujar_cola_suspendidos(pantalla, cola_suspendidos)
    dibujar_procesos_finalizados(pantalla, finalizados)

    # Dibujar botón de avanzar
    boton_rect = dibujar_boton()

    # Actualizar pantalla
    pygame.display.flip()
    clock.tick(60)  # Limitar la simulación a 60 FPS
    return boton_rect

# Esperar a que el usuario presione el botón en Pygame o ENTER en la terminal
def esperar_evento_o_enter(boton_rect):
    while True:
        # Captura eventos de pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cerrar_graficos()
                exit()  # Salir si se cierra la ventana
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect.collidepoint(event.pos):
                    return  # Salir del bucle si se hace clic en el botón

        # Verificar si se ha presionado ENTER en la terminal
        if os.name == 'nt':  # Para sistemas Windows
            if msvcrt.kbhit() and msvcrt.getch() == b'\r':  # Detectar ENTER en Windows
                return
        else:
            import sys, select
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                input()  # Consumir la entrada
                return  # Salir del bucle si se presionó ENTER en la terminal

        clock.tick(60)

# Función para cerrar Pygame
def cerrar_graficos():
    pygame.quit()
