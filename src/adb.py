# -----------------------------------------------------------------------------
# http://www.dabeaz.com/ply/example.html
# adb.py
#
# A simple calculator with variables -- all in one file.
# -----------------------------------------------------------------------------

reserved = {
    'begin': 'BEGIN',
    'beginro': 'BEGIN_READONLY',
    'end': 'END',
    'dump': 'DUMP',
    }

tokens = ['NAME', 'NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'LPAREN','RPAREN',
    #~ 'BEGIN', 'BEGIN_READONLY', 'END', 'DUMP',
    #~ 'FAIL', 'RECOVER',
    #~ 'READ', 'WRITE',
    ] + list(reserved.values())

# Tokens

t_PLUS            = r'\+'
t_MINUS           = r'-'
t_TIMES           = r'\*'
t_DIVIDE          = r'/'
t_EQUALS          = r'='
t_LPAREN          = r'\('
t_RPAREN          = r'\)'

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value.lower(), 'NAME')
    return t

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# Ignored characters
t_ignore = " \t"

def t_COMMENT(t):
    r'//.*'
    pass # No return value. Token discarded

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),
    )

# dictionary of names
names = { }

def p_statement_begin_transaction(t):
    'statement : BEGIN LPAREN expression RPAREN'
    print('begin', t[3])

def p_statement_begin_readonly_transaction(t):
    'statement : BEGIN_READONLY LPAREN expression RPAREN'
    print('beginRO', t[3])

def p_statement_end_transaction(t):
    'statement : END LPAREN expression RPAREN'
    print('end', t[3])

def p_statement_dump(t):
    'statement : DUMP LPAREN RPAREN'
    print('nothing to dump')

def p_statement_assign(t):
    'statement : NAME EQUALS expression'
    names[t[1]] = t[3]

def p_statement_expr(t):
    'statement : expression'
    print(t[1])

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if t[2] == '+'  : t[0] = t[1] + t[3]
    elif t[2] == '-': t[0] = t[1] - t[3]
    elif t[2] == '*': t[0] = t[1] * t[3]
    elif t[2] == '/': t[0] = t[1] / t[3]

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = -t[2]

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_number(t):
    'expression : NUMBER'
    t[0] = t[1]

def p_expression_name(t):
    'expression : NAME'
    try:
        t[0] = names[t[1]]
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()

while True:
    try:
        s = raw_input('adb > ')   # Use raw_input on Python 2
    except EOFError:
        break
    parser.parse(s)
