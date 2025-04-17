import pygame
import random
import sys

# Configuración del memorama
TARJETA_WIDTH = 140  # Nuevo tamaño de las tarjetas
TARJETA_HEIGHT = 140
NUM_TARJETAS = 10
CARDS_PER_ROW = 5  # Número de tarjetas por fila

class Memorama:
    def __init__(self, mesa_rect):
        """
        Inicializa el memorama.
        :param mesa_rect: Rectángulo que define la posición y tamaño de la mesa.
        """
        self.mesa_rect = mesa_rect
        self.tarjetas = []
        self.tarjetas_seleccionadas = []  # Almacena las tarjetas seleccionadas temporalmente
        self.tiempo_revertir = 0  # Contador para revertir tarjetas
        self.crear_tarjetas()

    def crear_tarjetas(self):
        """
        Crea las tarjetas del memorama.
        """
        # Cargar imágenes de las tarjetas
        try:
            imagen_trasera = pygame.image.load("assets/tarjeta_trasera.png")
            imagen_trasera = pygame.transform.scale(imagen_trasera, (TARJETA_WIDTH, TARJETA_HEIGHT))  # Redimensionar

            # Cargar imágenes frontales (5 títulos y 5 descripciones)
            imagenes_frente = [
                pygame.transform.scale(pygame.image.load(f"assets/tarjeta_frente_{i}.png"), (TARJETA_WIDTH, TARJETA_HEIGHT))
                for i in range(1, NUM_TARJETAS + 1)
            ]  # Redimensionar cada imagen frontal
        except pygame.error as e:
            print(f"Error al cargar una imagen: {e}")
            pygame.quit()
            sys.exit()

        # Asignar IDs únicos a cada tarjeta
        ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # IDs para títulos y descripciones
        random.shuffle(ids)
        print(f"IDs asignados: {ids}")  # Imprimir los IDs asignados

        # Calcular el espaciado y posición inicial
        spacing = 15  # Espaciado entre tarjetas
        x_start = self.mesa_rect.left + 160  # Margen izquierdo
        y_start = self.mesa_rect.top + 390  # Margen superior

        # Distribuir las tarjetas en la mesa
        for i in range(NUM_TARJETAS):
            row = i // CARDS_PER_ROW
            col = i % CARDS_PER_ROW
            x = x_start + (col * (TARJETA_WIDTH + spacing))
            y = y_start + (row * (TARJETA_HEIGHT + spacing))

            # Crear una tarjeta
            tarjeta = {
                "rect": pygame.Rect(x, y, TARJETA_WIDTH, TARJETA_HEIGHT),
                "frente": imagenes_frente[i],
                "trasera": imagen_trasera,
                "visible": False,  # Estado inicial: trasera visible
                "matched": False,  # Indica si la tarjeta ha sido emparejada
                "id": ids[i]  # ID único para identificar pares
            }
            self.tarjetas.append(tarjeta)

    def dibujar(self, screen):
        """
        Dibuja las tarjetas del memorama en la pantalla.
        :param screen: Superficie de la pantalla.
        """
        for tarjeta in self.tarjetas:
            if tarjeta["visible"]:
                screen.blit(tarjeta["frente"], tarjeta["rect"])
            else:
                screen.blit(tarjeta["trasera"], tarjeta["rect"])

            # Dibujar un rectángulo verde alrededor de las tarjetas emparejadas
            if tarjeta["matched"]:
                pygame.draw.rect(screen, (0, 255, 0), tarjeta["rect"], 2)  # Rectángulo verde transparente

    def verificar_interaccion(self, mouse_pos):
        """
        Verifica si el jugador está interactuando con alguna tarjeta.
        :param mouse_pos: Posición del ratón.
        :return: True si se selecciona una tarjeta, False de lo contrario.
        """
        for tarjeta in self.tarjetas:
            if tarjeta["rect"].collidepoint(mouse_pos) and not tarjeta["visible"] and not tarjeta["matched"]:
                tarjeta["visible"] = True
                self.tarjetas_seleccionadas.append(tarjeta)
                print(f"Tarjeta seleccionada: ID={tarjeta['id']}")  # Imprimir ID de la tarjeta seleccionada
                return True
        return False

    def actualizar(self):
        """
        Actualiza el estado del memorama.
        """
        # Verificar emparejamiento si hay dos tarjetas seleccionadas
        if len(self.tarjetas_seleccionadas) == 2:
            self.verificar_emparejamiento()

        # Revertir tarjetas si no coinciden
        if self.tiempo_revertir > 0:
            self.tiempo_revertir -= 1
            print(f"Tiempo restante para revertir: {self.tiempo_revertir}")  # Depurar el contador
            if self.tiempo_revertir == 0:
                for tarjeta in self.tarjetas_seleccionadas:
                    tarjeta["visible"] = False  # Ocultar tarjetas
                    print(f"Ocultando tarjeta con ID={tarjeta['id']}")  # Depurar la ocultación
                self.tarjetas_seleccionadas.clear()  # Limpiar la lista de tarjetas seleccionadas

    def verificar_emparejamiento(self):
        """
        Verifica si las dos tarjetas seleccionadas coinciden.
        """
        tarjeta1, tarjeta2 = self.tarjetas_seleccionadas

        # Verificar si las tarjetas coinciden usando sus IDs
        if (tarjeta1["id"] <= 5 and tarjeta2["id"] == tarjeta1["id"] + 5) or \
           (tarjeta2["id"] <= 5 and tarjeta1["id"] == tarjeta2["id"] + 5):
            tarjeta1["matched"] = True
            tarjeta2["matched"] = True
            print("¡Emparejamiento exitoso!")  # Imprimir mensaje de éxito
        else:
            # Programar la reversión de las tarjetas
            self.tiempo_revertir = 50  # 50 frames (aproximadamente 1 segundo)
            print("No coinciden. Programando reversión.")  # Imprimir mensaje de fallo

        # Limpiar la lista de tarjetas seleccionadas
        self.tarjetas_seleccionadas.clear()

        print(f"IDs seleccionados: {tarjeta1['id']}, {tarjeta2['id']}")  # Imprimir IDs seleccionados

    def hay_ganador(self):
        """
        Verifica si todas las tarjetas han sido emparejadas.
        :return: True si todas las tarjetas están emparejadas, False de lo contrario.
        """
        return all(tarjeta["matched"] for tarjeta in self.tarjetas)