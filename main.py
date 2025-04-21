import pygame
import sys
import os
import webbrowser
from personaje import Personaje  # Importar la clase Personaje
from casas import GestorCasas  # Importar el gestor de casas
from memorama import Memorama, PanelTemasDescubiertos  # Importar PanelTemasDescubiertos para botones dinámicos
 

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

    # Carga de imagen de los temas (ya no se usan directamente aquí, ahora en memorama.py)
    # Se manejan en PanelOpciones
except pygame.error as e:
    print(f"Error al cargar una imagen: {e}")
    pygame.quit()
    sys.exit()

# Redimensionar las imágenes de los botones
BOTON_WIDTH, BOTON_HEIGHT = 200, 100
boton_iniciar = pygame.transform.scale(boton_iniciar, (BOTON_WIDTH, BOTON_HEIGHT))
boton_instrucciones = pygame.transform.scale(boton_instrucciones, (BOTON_WIDTH, BOTON_HEIGHT))
boton_salir = pygame.transform.scale(boton_salir, (BOTON_WIDTH, BOTON_HEIGHT))

# Posiciones de los botones
boton_iniciar_rect = boton_iniciar.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
boton_instrucciones_rect = boton_instrucciones.get_rect(center=(WIDTH // 2, HEIGHT // 2))
boton_salir_rect = boton_salir.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

# Redimensionar las casas
CASA_WIDTH, CASA_HEIGHT = 800, 800
casa_izquierda = pygame.transform.scale(casa_izquierda, (CASA_WIDTH, CASA_HEIGHT))
casa_derecha = pygame.transform.scale(casa_derecha, (CASA_WIDTH, CASA_HEIGHT))
casa_arriba = pygame.transform.scale(casa_arriba, (CASA_WIDTH, CASA_HEIGHT))

# Posiciones de las casas
casa_izquierda_rect = casa_izquierda.get_rect(center=(WIDTH // 4, HEIGHT // 2))
casa_derecha_rect = casa_derecha.get_rect(center=(3 * WIDTH // 4, HEIGHT // 1.5))
casa_arriba_rect = casa_arriba.get_rect(center=(WIDTH // 2, HEIGHT // 4))

# Posición de la mesa
MESA_X, MESA_Y = -130, HEIGHT // 2 - 540
mesa_rect = pygame.Rect(MESA_X, MESA_Y, 1080, 1080)

# Función para mostrar el menú principal
def mostrar_menu():
    while True:
        screen.blit(fondo_menu, (0, 0))
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
                        while True:
                            volver_menu = iniciar_juego()
                            if volver_menu:
                                break
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
                    return

        pygame.display.flip()

# Función para iniciar el juego
def iniciar_juego():
    try:
        personaje = Personaje(WIDTH // 2, HEIGHT // 2)
        gestor_casas = GestorCasas()
        gestor_casas.agregar_casa("Izquierda", casa_izquierda_rect, nivel_requerido=0, interfaz=interfaz_izquierda)
        gestor_casas.agregar_casa("Centro", casa_arriba_rect, nivel_requerido=1, interfaz=interfaz_centro)
        gestor_casas.agregar_casa("Derecha", casa_derecha_rect, nivel_requerido=2, interfaz=interfaz_derecha)

        interfaz_actual = None
        tarjeta_memorama = Memorama(mesa_rect)
        panel_temas = PanelTemasDescubiertos(tarjeta_memorama)  # Instanciar panel de temas descubiertos

        #  Crear el panel lateral de opciones
        panel_opciones = PanelOpciones(1050, 100)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if interfaz_actual:
                            interfaz_actual = None  # Cerrar interfaz actual
                        else:
                            return True  # Retroceder al menú principal
                    elif event.key == pygame.K_SPACE:
                        nueva_interfaz = gestor_casas.verificar_interaccion(personaje.rect, True)
                        if nueva_interfaz:
                            interfaz_actual = nueva_interfaz
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # Manejar clics en botones de Memorama
                    if hasattr(tarjeta_memorama, 'reiniciar_rect') and tarjeta_memorama.reiniciar_rect.collidepoint(mouse_pos):
                        # Reiniciar juego y nivel
                        gestor_casas.nivel_actual = 0
                        tarjeta_memorama = Memorama(mesa_rect)
                        panel_temas = PanelTemasDescubiertos(tarjeta_memorama)
                        interfaz_actual = None
                        continue
                    elif hasattr(tarjeta_memorama, 'siguiente_rect') and tarjeta_memorama.siguiente_rect.collidepoint(mouse_pos):
                        # Desbloquear siguiente nivel y reiniciar memorama y panel temas
                        if gestor_casas.nivel_actual < len(gestor_casas.casas) - 1:
                            gestor_casas.nivel_actual += 1
                        tarjeta_memorama = Memorama(mesa_rect)
                        panel_temas = PanelTemasDescubiertos(tarjeta_memorama)
                        interfaz_actual = None
                        continue
                    # Solo permitir interacción si no hay tiempo de reversión
                    if tarjeta_memorama.tiempo_revertir == 0:
                        tarjeta_memorama.verificar_interaccion(mouse_pos)
                    panel_temas.verificar_click(mouse_pos)  # Verificar clicks en botones dinámicos
                
                # ✅ Eventos del panel lateral
                panel_opciones.manejar_evento(event)

            tarjeta_memorama.actualizar()
            if len(tarjeta_memorama.match_ids) > 0:
                panel_temas.actualizar_botones()  # Actualizar botones dinámicos
            screen.blit(fondo_juego, (0, 0))
            screen.blit(casa_izquierda, casa_izquierda_rect)
            screen.blit(casa_derecha, casa_derecha_rect)
            screen.blit(casa_arriba, casa_arriba_rect)

            keys = pygame.key.get_pressed()
            personaje.mover(keys, WIDTH, HEIGHT)
            personaje.actualizar_animacion()
            personaje.dibujar(screen)

            if interfaz_actual:
                screen.blit(interfaz_actual, (0, 0))
                screen.blit(mesa, (MESA_X, MESA_Y))
                tarjeta_memorama.dibujar(screen)

                # ✅ Dibujar panel lateral
                panel_opciones.dibujar(screen)
                if len(tarjeta_memorama.match_ids) > 0:
                    panel_temas.dibujar(screen)  # Dibujar botones dinámicos

            pygame.display.flip()
    except Exception as e:
        print(f"Error en el juego: {e}")
        # Evitar cierre abrupto para depuración
        # pygame.quit()
        # sys.exit()
class PanelOpciones:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.botones = []
        self.temas = {
           # "Interpolación Newton DD": ("Newton_DDivididas.png", "https://example.com/Newton_DDivididas"),
           # "Interpolación Newton Adelante": ("Newton_Hacia_Adelante.png", "https://example.com/Newton_Hacia_Adelante"),
            #"Interpolación Newton Atrás": ("Newton_Hacia_Atras.png", "https://example.com/Newton_Hacia_Atras"),
            # "Interpolación Newton Adelante": ("Lagrange.png", "https://example.com/Lagrange"),
            #"Interpolación Newton Atrás": ("Interpolacion_Lineal.png", "https://example.com/Interpolacion_Lineal"),
        }
        self.cargar_botones()

    def cargar_botones(self):
        for idx, (nombre, (archivo, url)) in enumerate(self.temas.items()):
            ruta = os.path.join("assets", archivo)
            try:
                imagen = pygame.image.load(ruta)
                imagen = pygame.transform.scale(imagen, (200, 100))
                rect = imagen.get_rect(topleft=(self.x, self.y + idx * 100))
                self.botones.append((nombre, imagen, rect, url))
            except pygame.error as e:
                print(f"No se pudo cargar {ruta}: {e}")

    def dibujar(self, screen):
        for nombre, imagen, rect, url in self.botones:
            screen.blit(imagen, rect)

    def manejar_evento(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for nombre, imagen, rect, url in self.botones:
                if rect.collidepoint(mouse_pos):
                    print(f"Abrir explicación: {nombre}")
                    webbrowser.open(url)
# Ejecutar el menú principal
if __name__ == "__main__":
    try:
        mostrar_menu()
    except Exception as e:
        print(f"Se produjo un error: {e}")
        pygame.quit()
        sys.exit()
