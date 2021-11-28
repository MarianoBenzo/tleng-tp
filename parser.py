import lexer
import ply.yacc as yacc

from atributos import Partidas, Partida, Turnos, Jugada, InfoJugada, Comentario, Movimiento, ComentarioContenidos

tokens = lexer.tokens


def p_s(t):
    's : partidas'
    print('\nMáximo nivel sin capturas: %d.' % int(t[1].nivel_maximo_sin_capturas))


def p_partidas(t):
    '''partidas : partida partidas
                | partida '''
    nivel_maximo_sin_capturas = max(t[1].nivel_maximo_sin_capturas, t[2].nivel_maximo_sin_capturas) if len(t) == 3 \
        else t[1].nivel_maximo_sin_capturas
    t[0] = Partidas(nivel_maximo_sin_capturas)


def p_partida(t):
    'partida : descriptores turnos'
    t[0] = Partida(t[2].nivel_maximo_sin_capturas)
    if t[2].numero_jugada_primer_turno != 1:
        print('El número de jugada debe comenzar en 1.')


def p_descriptores(t):
    '''descriptores : DESCRIPTOR descriptores
                    | DESCRIPTOR'''


def p_turnos(t):
    '''turnos   : jugada_blancas turnos_aux
                | resultado'''

    if len(t) == 3:
        nivel_maximo_sin_capturas = max(t[1].nivel_maximo_sin_capturas, t[2].nivel_maximo_sin_capturas)
        t[0] = Turnos('Blancas', t[1].numero_jugada, nivel_maximo_sin_capturas)

        if t[2].numero_jugada_primer_turno is not None:
            if t[2].color_primer_turno == 'Negras' and t[2].numero_jugada_primer_turno != t[1].numero_jugada:
                print('Los números de jugada %d y %d deben ser el mismo' % (
                    t[1].numero_jugada, t[2].numero_jugada_primer_turno))

            if t[2].color_primer_turno == 'Blancas' and t[2].numero_jugada_primer_turno != t[1].numero_jugada + 1:
                if t[2].numero_jugada_primer_turno > t[1].numero_jugada + 1:
                    print('Faltan jugadas entre %d y %d.' % (t[1].numero_jugada, t[2].numero_jugada_primer_turno))
                else:
                    print('Las jugadas %d y %d no son crecientes.' % (
                        t[1].numero_jugada, t[2].numero_jugada_primer_turno))
    else:
        t[0] = Turnos(None, None, 0)


def p_turnos_aux(t):
    '''turnos_aux   : jugada_negras turnos
                    | resultado'''
    if len(t) == 3:
        nivel_maximo_sin_capturas = max(t[1].nivel_maximo_sin_capturas, t[2].nivel_maximo_sin_capturas)
        color_primer_turno = 'Negras' if t[1].numero_jugada is not None else t[2].color_primer_turno
        numero_jugada_primer_turno = t[1].numero_jugada if t[1].numero_jugada is not None else t[
            2].numero_jugada_primer_turno

        t[0] = Turnos(color_primer_turno, numero_jugada_primer_turno, nivel_maximo_sin_capturas)

        if t[1].numero_jugada is not None and t[1].numero_jugada + 1 != t[2].numero_jugada_primer_turno:
            print('Las jugadas %d y %d no son consecutivas.' % (t[1].numero_jugada, t[2].numero_jugada_primer_turno))
    else:
        t[0] = Turnos(None, None, 0)


def p_resultado(t):
    '''resultado    : GANA_BLANCAS
                    | GANA_NEGRAS
                    | TABLAS'''


def p_jugada_blancas(t):
    'jugada_blancas : NUM_JUGADAS_BLANCAS ESPACIO info_jugada'
    t[0] = Jugada("Blancas", t[1], t[3].nivel_maximo_sin_capturas)


def p_jugada_negras(t):
    '''jugada_negras    : NUM_JUGADAS_NEGRAS ESPACIO info_jugada
                        | info_jugada'''
    if len(t) == 4:
        t[0] = Jugada("Negras", t[1], t[3].nivel_maximo_sin_capturas)
    else:
        t[0] = Jugada("Negras", None, t[1].nivel_maximo_sin_capturas)


def p_info_jugada(t):
    'info_jugada : MOVIMIENTO ESPACIO info_jugada_aux'
    t[0] = t[3]


def p_info_jugada_aux(t):
    '''info_jugada_aux  : comentario ESPACIO
                        | empty'''
    t[0] = InfoJugada(t[1].nivel_maximo_sin_capturas) if len(t) == 3 else InfoJugada(0)


def p_comentario(t):
    '''comentario   : LLAVE_IZQ comentario_contenidos LLAVE_DER
                    | PARENTESIS_IZQ comentario_contenidos PARENTESIS_DER'''
    nivel_maximo_sin_capturas = 0 if t[2].nivel_maximo_sin_capturas == 0 and t[2].hay_capturas\
        else t[2].nivel_maximo_sin_capturas + 1
    t[0] = Comentario(nivel_maximo_sin_capturas)


def p_comentario_contenidos(t):
    '''comentario_contenidos    : comentario_contenido ESPACIO comentario_contenidos
                                | comentario_contenido'''
    if len(t) == 4:
        if type(t[1]) is Movimiento:
            t[0] = ComentarioContenidos(t[3].nivel_maximo_sin_capturas, t[1].es_captura or t[3].hay_capturas)
        elif type(t[1]) is Comentario:
            nivel_maximo_sin_capturas = max(t[1].nivel_maximo_sin_capturas, t[3].nivel_maximo_sin_capturas)
            t[0] = ComentarioContenidos(nivel_maximo_sin_capturas, t[3].hay_capturas)
        else:
            t[0] = ComentarioContenidos(t[3].nivel_maximo_sin_capturas, t[3].hay_capturas)
    else:
        if type(t[1]) is Movimiento:
            t[0] = ComentarioContenidos(0, t[1].es_captura)
        elif type(t[1]) is Comentario:
            t[0] = ComentarioContenidos(t[1].nivel_maximo_sin_capturas, False)
        else:
            t[0] = ComentarioContenidos(0, False)


def p_comentario_contenido(t):
    '''comentario_contenido : comentario
                            | MOVIMIENTO
                            | TEXTO
                            | NUM_JUGADAS_NEGRAS
                            | NUM_JUGADAS_BLANCAS
                            | GANA_BLANCAS
                            | GANA_NEGRAS
                            | TABLAS'''
    t[0] = t[1]


def p_empty(p):
    'empty :'
    pass


def p_error(t):
    print(f"Error sintáctico en '{t.value}', linea {t.lineno}")


parser = yacc.yacc()
