
class S:
    def __init__(self, nivel_maximo_sin_capturas):
        self.nivel_maximo_sin_capturas = nivel_maximo_sin_capturas


class Partidas:
    def __init__(self, nivel_maximo_sin_capturas):
        self.nivel_maximo_sin_capturas = nivel_maximo_sin_capturas


class Partida:
    def __init__(self, nivel_maximo_sin_capturas):
        self.nivel_maximo_sin_capturas = nivel_maximo_sin_capturas


class Turnos:
    def __init__(self, color_primer_turno, numero_jugada_primer_turno, nivel_maximo_sin_capturas):
        self.color_primer_turno = color_primer_turno
        self.numero_jugada_primer_turno = numero_jugada_primer_turno
        self.nivel_maximo_sin_capturas = nivel_maximo_sin_capturas


class Jugada:
    def __init__(self, color, numero_jugada, nivel_maximo_sin_capturas):
        self.color = color
        self.numero_jugada = numero_jugada
        self.nivel_maximo_sin_capturas = nivel_maximo_sin_capturas


class InfoJugada:
    def __init__(self, nivel_maximo_sin_capturas):
        self.nivel_maximo_sin_capturas = nivel_maximo_sin_capturas


class ComentarioContenidos:
    def __init__(self, nivel_maximo_sin_capturas, hay_capturas):
        self.nivel_maximo_sin_capturas = nivel_maximo_sin_capturas
        self.hay_capturas = hay_capturas


class Comentario:
    def __init__(self, nivel_maximo_sin_capturas):
        self.nivel_maximo_sin_capturas = nivel_maximo_sin_capturas


class Movimiento:
    def __init__(self, es_captura):
        self.es_captura = es_captura
