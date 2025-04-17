import pygame
import os

# Clase para el personaje
class Personaje:
    def __init__(self, x, y):
        """
        Inicializa el personaje.
        :param x: Posición inicial en el eje X.
        :param y: Posición inicial en el eje Y.
        """
        # Definir la ruta base para las imágenes
        ASSETS_PATH = "assets/"

        # Cargar las animaciones como listas de imágenes
        self.animations = {
            "down": [
                pygame.image.load(os.path.join(ASSETS_PATH, "frame_down_1.png")),
                pygame.image.load(os.path.join(ASSETS_PATH, "frame_down_2.png")),
                pygame.image.load(os.path.join(ASSETS_PATH, "frame_down_3.png"))
            ],
            "up": [
                pygame.image.load(os.path.join(ASSETS_PATH, "frame_up_1.png")),
                pygame.image.load(os.path.join(ASSETS_PATH, "frame_up_2.png")),
                pygame.image.load(os.path.join(ASSETS_PATH, "frame_up_3.png"))
            ],
            "left": [
                pygame.image.load(os.path.join(ASSETS_PATH, "frame_left_1.png")),
                pygame.image.load(os.path.join(ASSETS_PATH, "frame_left_2.png")),
                pygame.image.load(os.path.join(ASSETS_PATH, "frame_left_3.png"))
            ],
            "right": [
                pygame.image.load(os.path.join(ASSETS_PATH, "frame_right_1.png")),
                pygame.image.load(os.path.join(ASSETS_PATH, "frame_right_2.png")),
                pygame.image.load(os.path.join(ASSETS_PATH, "frame_right_3.png"))
            ]
        }

        # Estado del personaje
        self.direccion = "down"  # Dirección inicial
        self.animacion_index = 0  # Índice para la animación
        self.animation_speed = 0.1  # Velocidad de cambio de sprites
        self.animation_time = 0  # Contador para controlar el tiempo de cambio de frames
        self.is_moving = False  # Indica si el personaje está en movimiento

        # Redimensionar los frames a un tamaño más grande (por ejemplo, 96x96)
        for direction in self.animations:
            self.animations[direction] = [pygame.transform.scale(frame, (96, 96)) for frame in self.animations[direction]]

        # Estado del personaje
        self.sprite_actual = self.animations[self.direccion][0]  # Frame inicial (quieto)
        self.rect = self.sprite_actual.get_rect()
        self.rect.topleft = (x, y)

        # Movimiento
        self.speed = 5  # Velocidad de movimiento

    def mover(self, keys, screen_width, screen_height):
        """
        Maneja el movimiento del personaje.
        :param keys: Estado de las teclas presionadas.
        :param screen_width: Ancho de la pantalla.
        :param screen_height: Alto de la pantalla.
        """
        dx = 0
        dy = 0
        self.is_moving = False

        if keys[pygame.K_LEFT]:
            dx -= self.speed
            self.direccion = "left"
            self.is_moving = True
        if keys[pygame.K_RIGHT]:
            dx += self.speed
            self.direccion = "right"
            self.is_moving = True
        if keys[pygame.K_UP]:
            dy -= self.speed
            self.direccion = "up"
            self.is_moving = True
        if keys[pygame.K_DOWN]:
            dy += self.speed
            self.is_moving = True

        # Actualizar posición
        self.rect.x += dx
        self.rect.y += dy

        # Mantener al personaje dentro de los límites de la pantalla
        self.rect.x = max(0, min(self.rect.x, screen_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, screen_height - self.rect.height))

    def actualizar_animacion(self):
        """
        Actualiza la animación del personaje.
        """
        if self.is_moving:
            self.animation_time += self.animation_speed
            if self.animation_time >= 1:
                self.animation_time = 0

        # Obtener el frame actual
        frames = self.animations[self.direccion]
        self.animacion_index = int(self.animation_time * len(frames))
        if self.animacion_index >= len(frames):
            self.animacion_index = 0
        self.sprite_actual = frames[self.animacion_index]

    def dibujar(self, screen):
        """
        Dibuja al personaje en la pantalla.
        :param screen: Superficie de la pantalla.
        """
        screen.blit(self.sprite_actual, self.rect)