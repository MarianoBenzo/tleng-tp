
tokens  = (
    'PARENTESIS_IZQ',
    'PARENTESIS_DER',
    'LLAVE_IZQ',
    'LLAVE_DER',
    'DESCRIPTOR',
    'ESPACIO',
    'MOVIMIENTO',
    'NUM_JUGADAS_NEGRAS',
    'NUM_JUGADAS_BLANCAS',
    'GANA_BLANCAS',
    'GANA_NEGRAS',
    'TABLAS',
    'TEXTO'
)

# Tokens

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_DESCRIPTOR(t):
    r'\[(.+)\s"(.+)"\]'
    return t

def t_PARENTESIS_IZQ(t):
    r'\('
    return t

def t_PARENTESIS_DER(t):
    r'\)'
    return t

def t_LLAVE_IZQ(t):
    r'\{'
    return t

def t_LLAVE_DER(t):
    r'\}'
    return t

def t_NUM_JUGADAS_NEGRAS(t):
    r'\d+\.\.\.'
    try:
        t.value = int(t.value.replace(".", ""))
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_NUM_JUGADAS_BLANCAS(t):
    r'\d+\.'
    try:
        t.value = int(t.value.replace(".", ""))
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_MOVIMIENTO(t):
    r'([PNBRQK]?[a-h]?[1-8]?x?[a-h][1-8](\+\+|\+)?|O-O-O|O-O)(\!|\?)?'
    t.value = Movimiento('x' in t.value)
    return t

def t_GANA_BLANCAS(t):
    r'1-0'
    return t

def t_GANA_NEGRAS(t):
    r'0-1'
    return t

def t_TABLAS(t):
    r'1/2-1/2'
    return t

def t_ESPACIO(t):
    r'\s+'
    return t

def t_TEXTO(t):
    r'[^\s{}()]+'
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Construyendo el analizador léxico
import ply.lex as lex
lexer = lex.lex()


# Atributos
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


# Definición de la gramática
def p_s(t):
    's : partidas'
    print('\nMáximo nivel sin capturas: %d.' % int(t[1].nivel_maximo_sin_capturas))

def p_partidas(t):
    '''partidas : partida partidas
                | partida '''
    nivel_maximo_sin_capturas = max(t[1].nivel_maximo_sin_capturas, t[2].nivel_maximo_sin_capturas) if len(t) == 3 else t[1].nivel_maximo_sin_capturas
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

        if t[2].numero_jugada_primer_turno != None:
            if t[2].color_primer_turno == 'Negras' and t[2].numero_jugada_primer_turno != t[1].numero_jugada:
                print('Los números de jugada %d y %d deben ser el mismo' % (t[1].numero_jugada, t[2].numero_jugada_primer_turno))
            
            if t[2].color_primer_turno == 'Blancas' and t[2].numero_jugada_primer_turno != t[1].numero_jugada + 1:
                if t[2].numero_jugada_primer_turno > t[1].numero_jugada + 1:
                    print('Faltan jugadas entre %d y %d.' % (t[1].numero_jugada, t[2].numero_jugada_primer_turno))
                else:
                    print('Las jugadas %d y %d no son crecientes.' % (t[1].numero_jugada, t[2].numero_jugada_primer_turno))
    else:
        t[0] = Turnos(None, None, 0)

def p_turnos_aux(t):
    '''turnos_aux   : jugada_negras turnos
                    | resultado'''
    if len(t) == 3:
        nivel_maximo_sin_capturas = max(t[1].nivel_maximo_sin_capturas, t[2].nivel_maximo_sin_capturas)
        color_primer_turno = 'Negras' if t[1].numero_jugada != None else t[2].color_primer_turno
        numero_jugada_primer_turno = t[1].numero_jugada if t[1].numero_jugada != None else t[2].numero_jugada_primer_turno

        t[0] = Turnos(color_primer_turno, numero_jugada_primer_turno, nivel_maximo_sin_capturas)

        if (t[1].numero_jugada != None and t[1].numero_jugada + 1 != t[2].numero_jugada_primer_turno):
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
    nivel_maximo_sin_capturas = 0 if t[2].nivel_maximo_sin_capturas == 0 and t[2].hay_capturas else t[2].nivel_maximo_sin_capturas + 1
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
    print("Error sintáctico en '%s'" % t.value)


import ply.yacc as yacc
parser = yacc.yacc()


f = open("./entrada.txt", "r")
input = f.read()
#print(input)
parser.parse(input)