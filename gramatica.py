
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



# Definición de la gramática
def p_partidas(t):
    '''partidas : partida partidas
                | partida '''

def p_partida(t):
    'partida : descriptores turnos'

def p_descriptores(t):
    '''descriptores : DESCRIPTOR descriptores
                    | DESCRIPTOR'''

def p_turnos(t):
    '''turnos   : jugada_blancas turnos_aux
                | resultado'''

def p_turnos_aux(t):
    '''turnos_aux   : jugada_negras turnos
                    | resultado'''

def p_resultado(t):
    '''resultado    : GANA_BLANCAS
                    | GANA_NEGRAS
                    | TABLAS'''

def p_jugada_blancas(t):
    'jugada_blancas : NUM_JUGADAS_BLANCAS ESPACIO movimiento'

def p_jugada_negras(t):
    '''jugada_negras    : NUM_JUGADAS_NEGRAS ESPACIO movimiento 
                        | movimiento'''

def p_movimiento(t):
    'movimiento : MOVIMIENTO ESPACIO movimiento_aux'

def p_movimiento_aux(t):
    '''movimiento_aux   : comentario ESPACIO
                        | empty'''  

def p_comentario(t):
    '''comentario   : LLAVE_IZQ comentario_contenidos LLAVE_DER
                    | PARENTESIS_IZQ comentario_contenidos PARENTESIS_DER'''

def p_comentario_contenidos(t):
    '''comentario_contenidos    : comentario_contenido ESPACIO comentario_contenidos
                                | comentario_contenido'''

def p_comentario_contenido(t):
    '''comentario_contenido : comentario
                            | MOVIMIENTO
                            | TEXTO'''

def p_empty(p):
     'empty :'
     pass

def p_error(t):
    print("Error sintáctico en '%s'" % t.value)


import ply.yacc as yacc
parser = yacc.yacc()


f = open("./entrada.txt", "r")
input = f.read()
print(input)
parser.parse(input)