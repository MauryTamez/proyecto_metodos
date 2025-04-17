import pygame

# Clase para representar una casa (nivel)
class Casa:
    def __init__(self, nombre, rect, nivel_requerido=0, interfaz=None):
        """
        Inicializa una casa.
        :param nombre: Nombre de la casa (por ejemplo, "Izquierda", "Centro", "Derecha").
        :param rect: Rectángulo que define la posición y tamaño de la casa.
        :param nivel_requerido: Nivel mínimo requerido para entrar.
        :param interfaz: Ruta de la imagen de la interfaz de la casa.
        """
        self.nombre = nombre
        self.rect = rect
        self.nivel_requerido = nivel_requerido
        self.interfaz = interfaz  # Imagen de la interfaz de la casa
        self.completado = False  # Indica si el nivel ha sido completado
        # Zona de interacción pequeña y centrada en la parte inferior de la casa
        self.zona_interaccion = pygame.Rect(
            rect.centerx - 50, rect.bottom - 300, 100, 100
        )

    def puede_entrar(self, nivel_actual):
        """
        Verifica si el jugador puede entrar a esta casa.
        :param nivel_actual: Nivel actual del jugador.
        :return: True si puede entrar, False de lo contrario.
        """
        return nivel_actual >= self.nivel_requerido

    def entrar(self):
        """
        Acción al entrar a la casa.
        """
        print(f"Entrando a la casa: {self.nombre}")
        self.completado = True  # Marcar como completado al entrar

# Clase para gestionar todas las casas
class GestorCasas:
    def __init__(self):
        """
        Inicializa el gestor de casas.
        """
        self.casas = []
        self.nivel_actual = 0  # Nivel actual del jugador
        self.mensaje_error = ""  # Mensaje de error para mostrar en pantalla

    def agregar_casa(self, nombre, rect, nivel_requerido=0, interfaz=None):
        """
        Agrega una nueva casa al gestor.
        :param nombre: Nombre de la casa.
        :param rect: Rectángulo que define la posición y tamaño de la casa.
        :param nivel_requerido: Nivel mínimo requerido para entrar.
        :param interfaz: Ruta de la imagen de la interfaz de la casa.
        """
        casa = Casa(nombre, rect, nivel_requerido, interfaz)
        self.casas.append(casa)

    def verificar_interaccion(self, jugador_rect, tecla_space):
        """
        Verifica si el jugador está interactuando con alguna casa.
        :param jugador_rect: Rectángulo del jugador.
        :param tecla_space: Booleano indicando si se presionó la tecla SPACE.
        :return: La ruta de la interfaz si el jugador entra en una casa, None si no entra.
        """
        if tecla_space:
            for casa in self.casas:
                if jugador_rect.colliderect(casa.zona_interaccion):  # Si el jugador está cerca
                    if casa.puede_entrar(self.nivel_actual):
                        casa.entrar()
                        self.nivel_actual += 1  # Avanzar al siguiente nivel
                        self.mensaje_error = ""  # Limpiar mensaje de error
                        return casa.interfaz  # Devolver la interfaz de la casa
                    else:
                        self.mensaje_error = f"No puedes entrar a '{casa.nombre}'. Completar niveles previos."
                        return None
        return None

    def dibujar_mensaje_error(self, screen):
        """
        Dibuja el mensaje de error en la esquina superior izquierda.
        :param screen: Superficie de la pantalla.
        """
        if self.mensaje_error:
            fuente = pygame.font.Font(None, 36)
            texto = fuente.render(self.mensaje_error, True, (255, 0, 0))  # Rojo
            screen.blit(texto, (10, 10))  # Esquina superior izquierda