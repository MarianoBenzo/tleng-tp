from atributos import Movimiento
import ply.lex as lex
import sys

sys.path.append("../..")


tokens = (
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
    r"\s+"
    return t


def t_TEXTO(t):
    r'[^\s{}()]+'
    return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lex.lex()

if __name__ == '__main__':
    lex.runmain()
