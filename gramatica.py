
tokens  = (
    'PARENTESIS_IZQ',
    'PARENTESIS_DER',
    'LLAVE_IZQ',
    'LLAVE_DER',
    'CORCHETE_IZQ',
    'CORCHETE_DER',
    'COMILLAS',
    'ESPACIO',
    'TEXTO',
    'MOVIMIENTO',
    'NUM_JUGADAS_NEGRAS',
    'NUM_JUGADAS_BLANCAS',
    'GANA_BLANCAS',
    'GANA_NEGRAS',
    'TABLAS'
)

# Tokens
t_PARENTESIS_IZQ    = r'\('
t_PARENTESIS_DER    = r'\)'
t_LLAVE_IZQ         = r'\{'
t_LLAVE_DER         = r'\}'
t_CORCHETE_IZQ      = r'\['
t_CORCHETE_DER      = r'\]'
t_COMILLAS          = r'"'
t_ESPACIO           = r'\s'
t_TEXTO             = r'[a-zA-Z0-9áÁéÉíÍóÓúÚñÑ]+'


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

def t_GANA_BLANCAS(t):
    r'1-0'
    return t

def t_GANA_NEGRAS(t):
    r'0-1'
    return t

def t_TABLAS(t):
    r'1/2-1/2'
    return t

def t_MOVIMIENTO(t):
    r'([PNBRQK]?[a-h]?[1-8]?x?[a-h][1-8](\+\+|\+)?|O-O-O|O-O)(\!|\?)?'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
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
    'partida : descripciones turnos'

def p_descripciones(t):
    '''descripciones    : descripcion descripciones
                        | descripcion'''

def p_descripcion(t):
    'descripcion : CORCHETE_IZQ TEXTO ESPACIO COMILLAS TEXTO COMILLAS CORCHETE_DER'

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
                            | TEXTO
                            | NUM_JUGADAS_BLANCAS
                            | NUM_JUGADAS_NEGRAS
                            | MOVIMIENTO'''

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