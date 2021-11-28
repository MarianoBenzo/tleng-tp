import sys
sys.path.insert(0, "../..")

import lexer
import parser

from ply import *

if len(sys.argv) == 1:
    print("usage : gramatica.py [-nocode] inputfile")
    raise SystemExit

if len(sys.argv) == 3:
    if sys.argv[1] == '-nocode':
        parser.emit_code = 0
    else:
        print("Unknown option '%s'" % sys.argv[1])
        raise SystemExit
    filename = sys.argv[2]
else:
    filename = sys.argv[1]

yacc.parse(open(filename).read())
