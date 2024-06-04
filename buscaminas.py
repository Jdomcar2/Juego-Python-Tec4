import pygame
import sys
import random

# Inicialización de Pygame
pygame.init()

# Constantes
MUSICA = pygame.mixer.Sound("Pou.mp3")
NUM_MINAS = 30
ANCHO, ALTO = 600, 300
COLOR_FONDO = (255, 255, 255)
COLOR_TABLERO = (200, 200, 200)
COLOR_TEXTO = (0, 0, 0)
COLOR_LINEA = (70, 70, 70)
COLOR_CUBIERTA = (220, 220, 220)  # Color de la capa :,C
TAM_CASILLA = 20
MARGEN = 5
FILAS = 15
COLUMNAS = 15
TIEMPO_MAXIMO = 1800
TAM_TEXTO = 24

# Configuración de la ventana
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Buscaminas')

# Cargar imagen de la mina, la bandera y el pou
imagen_mina = pygame.image.load('mina.png')
imagen_mina = pygame.transform.scale(imagen_mina, (TAM_CASILLA - MARGEN, TAM_CASILLA - MARGEN))
imagen_bandera = pygame.image.load('bandera.png')
imagen_bandera = pygame.transform.scale(imagen_bandera, (TAM_CASILLA - MARGEN, TAM_CASILLA - MARGEN))
imagen_Pou = pygame.image.load('Pou.png')
imagen_Pou = pygame.transform.scale(imagen_Pou, (ANCHO, ALTO))

# Tablero del juego
tablero = [[0 for _ in range(COLUMNAS)] for _ in range(FILAS)]
estado_casillas = [['C' for _ in range(COLUMNAS)] for _ in range(FILAS)]
minas_restantes = NUM_MINAS

# Funciones
MUSICA.play()

def colocar_minas():
    minas = []
    while len(minas) < NUM_MINAS:
        fila = random.randint(0, FILAS - 1)
        columna = random.randint(0, COLUMNAS - 1)
        if tablero[fila][columna] == 0:
            tablero[fila][columna] = 'M'
            minas.append((fila, columna))
            for i in range(max(0, fila-1), min(FILAS, fila+2)):
                for j in range(max(0, columna-1), min(COLUMNAS, columna+2)):
                    if isinstance(tablero[i][j], int):
                        tablero[i][j] += 1
    return minas

def dibujar_tablero():
    fondo_tablero = pygame.Rect(0, 0, COLUMNAS * TAM_CASILLA, FILAS * TAM_CASILLA)
    pygame.draw.rect(pantalla, COLOR_TABLERO, fondo_tablero)
    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            rect = pygame.Rect(columna * TAM_CASILLA, fila * TAM_CASILLA, TAM_CASILLA - MARGEN, TAM_CASILLA - MARGEN)
            pygame.draw.rect(pantalla, COLOR_TABLERO, rect)
            valor = tablero[fila][columna]
            estado = estado_casillas[fila][columna]
            if estado == 'R':
                if valor == 'M':
                    pantalla.blit(imagen_mina, rect.topleft)
                elif isinstance(valor, int) and valor > 0:
                    texto_numero = pygame.font.SysFont(None, TAM_TEXTO).render(str(valor), True, COLOR_TEXTO)
                    pantalla.blit(texto_numero, rect.topleft)
            elif estado == 'C' or estado == 'F':
                pygame.draw.rect(pantalla, COLOR_CUBIERTA, rect)
                if estado == 'F':
                    pantalla.blit(imagen_bandera, rect.topleft)

def revelar_casilla(fila, columna):
    if estado_casillas[fila][columna] == 'C':
        estado_casillas[fila][columna] = 'R'
        if tablero[fila][columna] == 'M':
            return False
        elif tablero[fila][columna] == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if 0 <= fila + dy < FILAS and 0 <= columna + dx < COLUMNAS:
                        if tablero[fila + dy][columna + dx] == 0 and estado_casillas[fila + dy][columna + dx] == 'C':
                            revelar_casilla(fila + dy, columna + dx)
                        elif tablero[fila + dy][columna + dx] != 'M':
                            estado_casillas[fila + dy][columna + dx] = 'R'
    return True

def alternar_bandera(fila, columna):
    global minas_restantes
    if estado_casillas[fila][columna] == 'C':
        estado_casillas[fila][columna] = 'F'
        minas_restantes -= 1
    elif estado_casillas[fila][columna] == 'F':
        estado_casillas[fila][columna] = 'C'
        minas_restantes += 1

def comprobar_victoria():
    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            if tablero[fila][columna] == 'M' and estado_casillas[fila][columna] != 'F':
                return False
    return True

# Cositas 
reloj = pygame.time.Clock()
tiempo_inicio = pygame.time.get_ticks()
juego_terminado = False
victoria = False
minas = colocar_minas()

while not juego_terminado:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            fila, columna = pos[1] // TAM_CASILLA, pos[0] // TAM_CASILLA
            if evento.button == 1:  # Click izquierdo para revelar casilla
                juego_terminado = not revelar_casilla(fila, columna)
            elif evento.button == 3:  # Click derecho para alternar bandera
                alternar_bandera(fila, columna)

    pantalla.fill(COLOR_FONDO)
    dibujar_tablero()

    # Dibujar la línea separadora
    posicion_linea = ANCHO // 2
    pygame.draw.line(pantalla, COLOR_LINEA, (posicion_linea, 0), (posicion_linea, ALTO), 2)

    # Actualizar el marcador y el tiempo
    tiempo_actual = (pygame.time.get_ticks() - tiempo_inicio) // 1000
    if tiempo_actual >= TIEMPO_MAXIMO:
        juego_terminado = True
    texto_tiempo = pygame.font.SysFont(None, TAM_TEXTO).render(f'Tiempo: {tiempo_actual}', True, COLOR_TEXTO)
    pantalla.blit(texto_tiempo, (posicion_linea + 10, 10))

    texto_minas = pygame.font.SysFont(None, TAM_TEXTO).render(f'Minas restantes: {minas_restantes}', True, COLOR_TEXTO)
    pantalla.blit(texto_minas, (posicion_linea + 10, 40))

    pygame.display.flip()
    reloj.tick(60)

    if minas_restantes == 0 and comprobar_victoria():
        victoria = True
        juego_terminado = True

# Mostrar mensaje de fin de juego
if victoria:
    texto_victoria = pygame.font.SysFont(None, 72).render('Ganaste, de momento', True, COLOR_TEXTO)
    pantalla.blit(texto_victoria, (ANCHO // 2 - texto_victoria.get_width() // 2, ALTO // 2 - texto_victoria.get_height() // 2))
else:
    pygame.time.wait(1000)
    pantalla.blit(imagen_Pou, (0, 0))

pygame.display.flip()
pygame.time.wait(3000)
pygame.quit()
