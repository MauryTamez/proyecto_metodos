import os, pygame
import random
import sys
from datetime import datetime, timedelta

# Configuración
TARJETA_WIDTH = 140
TARJETA_HEIGHT = 140
NUM_TARJETAS = 10
CARDS_PER_ROW = 5
TIEMPO_LIMITE = 300  # 5 minutos en segundos

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Juego de Memorama")
font = pygame.font.SysFont("Arial", 28)
small_font = pygame.font.SysFont("Arial", 20)

class BotonExplicacion:
    def __init__(self, ruta_imagen, x, y, explicacion):
        self.imagen = pygame.image.load(ruta_imagen)
        self.rect = self.imagen.get_rect(topleft=(x, y))
        self.explicacion = explicacion
        self.mostrar_explicacion = False

    def dibujar(self, screen):
        screen.blit(self.imagen, self.rect)
        if self.mostrar_explicacion:
            self.mostrar_texto(screen)

    def verificar_click(self, pos):
        if self.rect.collidepoint(pos):
            self.mostrar_explicacion = not self.mostrar_explicacion

    def mostrar_texto(self, screen):
        lineas = self.explicacion.split("\n")
        for i, linea in enumerate(lineas):
            texto = small_font.render(linea, True, (255, 255, 255))
            screen.blit(texto, (self.rect.x, self.rect.bottom + 10 + i * 20))
# Nombres y descripciones de temas de interpolación
TEMAS_INTERPOLACION = {
    1: {
        "nombre": "",
        "descripcion": "La interpolación de Lagrange encuentra un polinomio único que pasa exactamente por un conjunto dado de puntos.",
        "imagen": "Lagrange.png"
    },
    3: {
        "nombre": "",
        "descripcion": "Los splines lineales conectan cada par de puntos con una línea recta, creando una función continua por partes.",
        "imagen": "Interpolacion_Lineal.png"
    },
    4: {
        "nombre": "",
        "descripcion": "Los splines cúbicos usan polinomios de tercer grado para crear una curva suave que pasa por todos los puntos.",
        "imagen": "Newton_Hacia_Atras.png"
    },
    5: {
        "nombre": "",
        "descripcion": "La interpolación de Hermite considera tanto los valores de la función como sus derivadas en los puntos dados.",
        "imagen": "Newton_DDivididas.png"
    },
    2:{
        "nombre": "",
        "descripcion": "Los splines cúbicos usan polinomios de tercer grado para crear una curva suave que pasa por todos los puntos.",
        "imagen": "Newton_Hacia_Adelante.png" 
    }
}

class Memorama:
    def __init__(self, mesa_rect):
        self.mesa_rect = mesa_rect
        self.tarjetas = []
        self.tarjetas_seleccionadas = []
        self.tiempo_revertir = 0
        self.match_ids = []
        self.crear_tarjetas()
        self.inicio_tiempo = datetime.now()
        self.fin_tiempo = self.inicio_tiempo + timedelta(seconds=TIEMPO_LIMITE)
        self.juego_terminado = False

    def crear_tarjetas(self):
        try:
            imagen_trasera = pygame.transform.scale(
                pygame.image.load("assets/tarjeta_trasera.png"),
                (TARJETA_WIDTH, TARJETA_HEIGHT)
            )
            imagenes_frente = [
                pygame.transform.scale(pygame.image.load(f"assets/tarjeta_frente_{i}.png"),
                (TARJETA_WIDTH, TARJETA_HEIGHT)) for i in range(1, NUM_TARJETAS + 1)
            ]
        except pygame.error as e:
            print(f"Error al cargar imagen: {e}")
            pygame.quit()
            sys.exit()

        ids = list(range(1, NUM_TARJETAS + 1))
        random.shuffle(ids)

        spacing = 15
        x_start = self.mesa_rect.left + 160
        y_start = self.mesa_rect.top + 390

        for i in range(NUM_TARJETAS):
            row = i // CARDS_PER_ROW
            col = i % CARDS_PER_ROW
            x = x_start + (col * (TARJETA_WIDTH + spacing))
            y = y_start + (row * (TARJETA_HEIGHT + spacing))

            tarjeta = {
                "rect": pygame.Rect(x, y, TARJETA_WIDTH, TARJETA_HEIGHT),
                "frente": imagenes_frente[i],
                "trasera": imagen_trasera,
                "visible": False,
                "matched": False,
                "id": ids[i]
            }
            self.tarjetas.append(tarjeta)

    def dibujar(self, screen):
        for tarjeta in self.tarjetas:
            if tarjeta["visible"]:
                screen.blit(tarjeta["frente"], tarjeta["rect"])
            else:
                screen.blit(tarjeta["trasera"], tarjeta["rect"])
            if tarjeta["matched"]:
                pygame.draw.rect(screen, (0, 255, 0), tarjeta["rect"], 2)
     
        # Temporizador
        tiempo_restante = max(0, int((self.fin_tiempo - datetime.now()).total_seconds()))
        temporizador_texto = font.render(f"Tiempo: {tiempo_restante // 60}:{tiempo_restante % 60:02}", True, (255, 255, 255))
        screen.blit(temporizador_texto, (20, 20))

        # Título
        titulo = font.render("Interpolación", True, (255, 255, 255))
        screen.blit(titulo, (700, 20))

        # Calcular posición para los botones debajo del panel de temas descubiertos
        y_inicio_botones = 100 + len(self.match_ids) * 70 + 20  # 20 píxeles de margen

        # Botones reiniciar y siguiente nivel si se gana o termina el juego
        if (self.hay_ganador() or self.juego_terminado):
            # Botón reiniciar
            pygame.draw.rect(screen, (200, 100, 100), (800, y_inicio_botones, 220, 50))
            reiniciar_texto = font.render("Reiniciar Nivel", True, (255, 255, 255))
            reiniciar_rect = reiniciar_texto.get_rect(center=(800 + 110, y_inicio_botones + 25))
            screen.blit(reiniciar_texto, reiniciar_rect)

            # Botón siguiente nivel
            pygame.draw.rect(screen, (100, 200, 100), (800, y_inicio_botones + 60, 220, 50))
            siguiente_texto = font.render("Siguiente Nivel", True, (0, 0, 0))
            siguiente_rect = siguiente_texto.get_rect(center=(800 + 110, y_inicio_botones + 60 + 25))
            screen.blit(siguiente_texto, siguiente_rect)

            # Guardar rects para detección de clic
            self.reiniciar_rect = pygame.Rect(800, y_inicio_botones, 220, 50)
            self.siguiente_rect = pygame.Rect(800, y_inicio_botones + 60, 220, 50)

    def verificar_interaccion(self, mouse_pos):
        if len(self.tarjetas_seleccionadas) >= 2 or self.tiempo_revertir > 0:
            return False
        for tarjeta in self.tarjetas:
            if tarjeta["rect"].collidepoint(mouse_pos) and not tarjeta["visible"] and not tarjeta["matched"]:
                tarjeta["visible"] = True
                self.tarjetas_seleccionadas.append(tarjeta)
                print(f"Tarjeta seleccionada: ID={tarjeta['id']}")
                return True
        return False

    def actualizar(self):
        if len(self.tarjetas_seleccionadas) == 2 and self.tiempo_revertir == 0:
            self.verificar_emparejamiento()

        if self.tiempo_revertir > 0:
            self.tiempo_revertir -= 1
            if self.tiempo_revertir == 0:
                for tarjeta in self.tarjetas_seleccionadas:
                    tarjeta["visible"] = False
                self.tarjetas_seleccionadas.clear()

        # Verificar fin de tiempo
        if datetime.now() >= self.fin_tiempo:
            print("Tiempo agotado.")
            self.juego_terminado = True

    def verificar_emparejamiento(self):
        tarjeta1, tarjeta2 = self.tarjetas_seleccionadas
        if (tarjeta1["id"] <= 5 and tarjeta2["id"] == tarjeta1["id"] + 5) or \
           (tarjeta2["id"] <= 5 and tarjeta1["id"] == tarjeta2["id"] + 5):
            tarjeta1["matched"] = True
            tarjeta2["matched"] = True
            self.match_ids.append(tarjeta1["id"])
            print("¡Emparejamiento exitoso!")
            print(f"IDs emparejadas: {self.match_ids}")
            self.tarjetas_seleccionadas.clear()
        else:
            self.tiempo_revertir = 15  # Reducido para voltear más rápido
            print("No coinciden. Programando reversión.")

    def hay_ganador(self):
        return all(tarjeta["matched"] for tarjeta in self.tarjetas)

# NUEVO - Clase para mostrar explicaciones en pantalla completa
class PantallaExplicacion:
    def __init__(self, nombre, descripcion, imagen):
        self.nombre = nombre
        self.descripcion = descripcion
        self.imagen = pygame.image.load(imagen)
        self.imagen = pygame.transform.scale(self.imagen, (300, 300))

    def mostrar(self):
        mostrando = True
        while mostrando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        mostrando = False

            screen.fill((10, 10, 40))
            titulo = font.render(self.nombre, True, (255, 255, 255))
            screen.blit(titulo, (400, 30))
            screen.blit(self.imagen, (350, 100))

            y = 420
            for linea in self.descripcion.split("\n"):
                txt = small_font.render(linea, True, (255, 255, 255))
                screen.blit(txt, (100, y))
                y += 30

            instrucciones = small_font.render("Presiona ESC para volver", True, (180, 180, 180))
            screen.blit(instrucciones, (350, 750))

            pygame.display.flip()

# NUEVO - Panel lateral con temas descubiertos

class PanelTemasDescubiertos:
    def __init__(self, juego):
        self.juego = juego
        self.botones = []

    def actualizar_botones(self):
        self.botones.clear()
        for i, id in enumerate(self.juego.match_ids):
            tema_id = id if id <= 5 else id - 5
            tema = TEMAS_INTERPOLACION[tema_id]
            # Cargar miniatura
            ruta = os.path.join("assets", tema["imagen"])
            mini = pygame.transform.scale(pygame.image.load(ruta), (160, 160))
            boton_rect = pygame.Rect(800, 100 + i * 70, 220, 70)
            self.botones.append((boton_rect, tema, mini))

    def dibujar(self, screen):
        titulo = small_font.render("Temas Descubiertos:", True, (255, 255, 255))
        screen.blit(titulo, (800, 60))
        for boton_rect, tema, mini in self.botones:
            # pygame.draw.rect(screen, (50, 120, 200), boton_rect)  # Fondo azul eliminado
            texto = small_font.render(tema["nombre"], True, (255, 255, 255))
            texto_rect = texto.get_rect()
            # Centrar imagen y texto juntos horizontalmente en el rectángulo del botón
            total_width = mini.get_width() + 10 + texto_rect.width
            x_start = boton_rect.x + (boton_rect.width - total_width) // 2 + 20  # Mover 20 píxeles a la derecha
            y_center = boton_rect.y + boton_rect.height // 2

            # Dibujar imagen centrada verticalmente
            screen.blit(mini, (x_start, y_center - mini.get_height() // 2))
            # Dibujar texto centrado verticalmente y con un margen de 10 píxeles a la derecha de la imagen
            screen.blit(texto, (x_start + mini.get_width() + 10, y_center - texto_rect.height // 2))

    def verificar_click(self, pos):
        for boton_rect, tema, _ in self.botones:
            if boton_rect.collidepoint(pos):
                pantalla = PantallaExplicacion(
                    tema["nombre"], tema["descripcion"],
                    os.path.join("assets", tema["imagen"])
                )
                pantalla.mostrar()


# Código de ejecución principal
    def main():
        reloj = pygame.time.Clock()
        mesa = pygame.Rect(0, 0, 1000, 800)
        juego = Memorama(mesa)
        panel_temas = PanelTemasDescubiertos(juego)  # NUEVO


        # Botones educativos
        botones = [
            BotonExplicacion("Newton_DDivididas.png", -140, -390, "Newton con Diferencias Divididas:\nUtiliza nodos no equidistantes\ny una tabla de diferencias divididas."),
            BotonExplicacion("Newton_Hacia_Adelante.png", 140, 390, "Newton Hacia Adelante:\nSe usa cuando los datos están\nordenados hacia adelante y equidistantes."),
            BotonExplicacion("Newton_Hacia_Atras.png", 140, 390, "Newton Hacia Atrás:\nIdeal para interpolar hacia el final\nde una tabla con nodos equidistantes."),
            BotonExplicacion("Lagrange.png", 140, 390, "Lagrang:\nSe usa cuando los datos están\nordenados hacia adelante y equidistantes."),
            BotonExplicacion("Interpolacion_Lineal.png", 140, 390, "Interpolacion_Lineal:\nIdeal para interpolar hacia el final\nde una tabla con nodos equidistantes."),
        ]   

        corriendo = True
        siguiente_nivel = False
        reiniciar_nivel = False
        while corriendo:
            screen.fill((30, 30, 60))

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    print("Evento QUIT detectado, terminando juego.")
                    corriendo = False
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if juego.hay_ganador() and hasattr(juego, 'siguiente_rect') and juego.siguiente_rect.collidepoint(evento.pos):
                        print("Siguiente nivel... clic en botón detectado, terminando juego.")
                        siguiente_nivel = True
                        corriendo = False
                    elif hasattr(juego, 'reiniciar_rect') and juego.reiniciar_rect.collidepoint(evento.pos):
                        print("Reiniciar nivel... clic en botón detectado, reiniciando juego.")
                        reiniciar_nivel = True
                        corriendo = False
                    else:
                        if not juego.verificar_interaccion(evento.pos):
                            for boton in botones:
                                boton.verificar_click(evento.pos)

            juego.actualizar()
            panel_temas.actualizar_botones()  
            panel_temas.dibujar(screen)       
            juego.dibujar(screen)
        if not juego.verificar_interaccion(evento.pos):
            for boton in botones:
                boton.verificar_click(evento.pos)
        panel_temas.verificar_click(evento.pos)  # NUEVO

        if reiniciar_nivel:
            return False  # No volver al menú, reiniciar nivel
        return siguiente_nivel

if __name__ == "__main__":
    main()
