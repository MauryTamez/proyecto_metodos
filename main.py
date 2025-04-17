import pygame
import sys
import os
from personaje import Personaje  # Importar la clase Personaje
from casas import GestorCasas  # Importar el gestor de casas
from memorama import Memorama  # Importar la clase Memorama

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego 2D")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Ruta base para las imágenes
ASSETS_PATH = "assets/"

# Cargar imágenes
try:
    fondo_menu = pygame.image.load(os.path.join(ASSETS_PATH, "fondo_menu.png"))
    boton_iniciar = pygame.image.load(os.path.join(ASSETS_PATH, "boton_iniciar.png"))
    boton_instrucciones = pygame.image.load(os.path.join(ASSETS_PATH, "boton_instrucciones.png"))
    boton_salir = pygame.image.load(os.path.join(ASSETS_PATH, "boton_salir.png"))
    fondo_juego = pygame.image.load(os.path.join(ASSETS_PATH, "fondo_juego.png"))

    # Cargar imágenes de las casas
    casa_izquierda = pygame.image.load(os.path.join(ASSETS_PATH, "casa_izquierda.png"))
    casa_derecha = pygame.image.load(os.path.join(ASSETS_PATH, "casa_derecha.png"))
    casa_arriba = pygame.image.load(os.path.join(ASSETS_PATH, "casa_arriba.png"))

    # Cargar imágenes de las interfaces de las casas
    interfaz_izquierda = pygame.image.load(os.path.join(ASSETS_PATH, "interfaz_izquierda.png"))
    interfaz_centro = pygame.image.load(os.path.join(ASSETS_PATH, "interfaz_centro.png"))
    interfaz_derecha = pygame.image.load(os.path.join(ASSETS_PATH, "interfaz_derecha.png"))

    # Cargar imagen de la mesa
    mesa = pygame.image.load(os.path.join(ASSETS_PATH, "mesa.png"))
except pygame.error as e:
    print(f"Error al cargar una imagen: {e}")
    pygame.quit()
    sys.exit()

# Redimensionar las imágenes de los botones (si es necesario)
BOTON_WIDTH, BOTON_HEIGHT = 200, 100
boton_iniciar = pygame.transform.scale(boton_iniciar, (BOTON_WIDTH, BOTON_HEIGHT))
boton_instrucciones = pygame.transform.scale(boton_instrucciones, (BOTON_WIDTH, BOTON_HEIGHT))
boton_salir = pygame.transform.scale(boton_salir, (BOTON_WIDTH, BOTON_HEIGHT))

# Posiciones de los botones
boton_iniciar_rect = boton_iniciar.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
boton_instrucciones_rect = boton_instrucciones.get_rect(center=(WIDTH // 2, HEIGHT // 2))
boton_salir_rect = boton_salir.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

# Redimensionar las casas a un tamaño más pequeño (por ejemplo, 800x800)
CASA_WIDTH, CASA_HEIGHT = 800, 800  # Tamaño deseado para las casas
casa_izquierda = pygame.transform.scale(casa_izquierda, (CASA_WIDTH, CASA_HEIGHT))
casa_derecha = pygame.transform.scale(casa_derecha, (CASA_WIDTH, CASA_HEIGHT))
casa_arriba = pygame.transform.scale(casa_arriba, (CASA_WIDTH, CASA_HEIGHT))

# Posiciones de las casas
casa_izquierda_rect = casa_izquierda.get_rect(center=(WIDTH // 4, HEIGHT // 2))
casa_derecha_rect = casa_derecha.get_rect(center=(3 * WIDTH // 4, HEIGHT // 1.5))
casa_arriba_rect = casa_arriba.get_rect(center=(WIDTH // 2, HEIGHT // 4))

# Posición de la mesa
MESA_X, MESA_Y = -130, HEIGHT // 2 - 540  # Ubicada en la parte izquierda

# Crear el rectángulo de la mesa
mesa_rect = pygame.Rect(MESA_X, MESA_Y, 1080, 1080)  # Área de la mesa

# Función para mostrar el menú principal
def mostrar_menu():
    while True:
        screen.blit(fondo_menu, (0, 0))  # Dibujar el fondo del menú
        screen.blit(boton_iniciar, boton_iniciar_rect)
        screen.blit(boton_instrucciones, boton_instrucciones_rect)
        screen.blit(boton_salir, boton_salir_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if boton_iniciar_rect.collidepoint(mouse_pos):
                    try:
                        iniciar_juego()
                    except Exception as e:
                        print(f"Error al iniciar el juego: {e}")
                        pygame.quit()
                        sys.exit()
                elif boton_instrucciones_rect.collidepoint(mouse_pos):
                    mostrar_instrucciones()
                elif boton_salir_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

# Función para mostrar las instrucciones
def mostrar_instrucciones():
    while True:
        screen.fill(WHITE)
        fuente = pygame.font.Font(None, 36)
        texto = fuente.render("Aquí van las instrucciones del juego.", True, BLACK)
        texto_rect = texto.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(texto, texto_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Volver al menú principal

        pygame.display.flip()

# Función para iniciar el juego
def iniciar_juego():
    try:
        # Crear al personaje en una posición visible
        personaje = Personaje(WIDTH // 2, HEIGHT // 2)

        # Crear el gestor de casas
        gestor_casas = GestorCasas()
        gestor_casas.agregar_casa("Izquierda", casa_izquierda_rect, nivel_requerido=0, interfaz=interfaz_izquierda)
        gestor_casas.agregar_casa("Centro", casa_arriba_rect, nivel_requerido=1, interfaz=interfaz_centro)
        gestor_casas.agregar_casa("Derecha", casa_derecha_rect, nivel_requerido=2, interfaz=interfaz_derecha)

        # Variable para almacenar la interfaz actual
        interfaz_actual = None

        # Crear una instancia del memorama
        tarjeta_memorama = Memorama(mesa_rect)

        while True:
            # Manejar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Verificar si se presiona ESC para volver al menú
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return  # Volver al menú principal
                    elif event.key == pygame.K_SPACE:
                        nueva_interfaz = gestor_casas.verificar_interaccion(personaje.rect, True)
                        if nueva_interfaz:
                            interfaz_actual = nueva_interfaz
                # Verificar interacción con la tarjeta
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    tarjeta_memorama.verificar_interaccion(mouse_pos)

            #Actualizar el estado del memorama
            tarjeta_memorama.actualizar()
            
            # Dibujar el fondo del juego primero
            screen.blit(fondo_juego, (0, 0))

            # Dibujar las casas
            screen.blit(casa_izquierda, casa_izquierda_rect)
            screen.blit(casa_derecha, casa_derecha_rect)
            screen.blit(casa_arriba, casa_arriba_rect)

            # Manejar eventos del personaje
            keys = pygame.key.get_pressed()
            personaje.mover(keys, WIDTH, HEIGHT)

            # Actualizar el personaje
            personaje.actualizar_animacion()

            # Dibujar al personaje encima del fondo y las casas
            personaje.dibujar(screen)

            # Si hay una interfaz activa, dibujarla
            if interfaz_actual:
                screen.blit(interfaz_actual, (0, 0))
                screen.blit(mesa, (MESA_X, MESA_Y))  # Dibujar la mesa
                tarjeta_memorama.dibujar(screen)  # Dibujar las tarjetas del memorama

            pygame.display.flip()
    except Exception as e:
        print(f"Error en el juego: {e}")
        pygame.quit()
        sys.exit()

# Ejecutar el menú principal
if __name__ == "__main__":
    try:
        mostrar_menu()
    except Exception as e:
        print(f"Se produjo un error: {e}")
        pygame.quit()
        sys.exit()