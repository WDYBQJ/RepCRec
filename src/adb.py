# -----------------------------------------------------------------------------
# http://www.dabeaz.com/ply/example.html
# adb.py
#
# A simple calculator with variables -- all in one file.
# -----------------------------------------------------------------------------

from transaction import ReadWriteTransaction, ReadOnlyTransaction

reserved = {
	'begin': 'BEGIN',
	'beginro': 'BEGIN_READONLY',
	'end': 'END',
	'dump': 'DUMP',
	'fail': 'FAIL',
	'recover': 'RECOVER',
	'r': 'READ',
	'w': 'WRITE',
	'quit': 'QUIT',
	}

tokens = ['NAME', 'NUMBER',
	'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
	'LPAREN','RPAREN',
	'COMMA', 'SEMICOLON',
	] + list(reserved.values())

# Tokens

t_PLUS            = r'\+'
t_MINUS           = r'-'
t_TIMES           = r'\*'
t_DIVIDE          = r'/'
t_EQUALS          = r'='
t_LPAREN          = r'\('
t_RPAREN          = r'\)'
t_COMMA           = r','
t_SEMICOLON       = r';'

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

def p_stmtlist_0(t):
	'stmtlist : '
	pass

def p_stmtlist_1(t):
	'stmtlist : statement'
	pass

def p_stmtlist_2(t):
	'stmtlist : statement SEMICOLON stmtlist'
	pass

def p_statement_quit(t):
	'statement : QUIT'
	raise SystemExit

def p_statement_begin_transaction(t):
	'statement : BEGIN LPAREN namelist RPAREN'
	for name in t[3]:
		if name in names:
			print('Error: transaction %s has started!!!' % name)
		assert name not in names
		names[name] = ReadWriteTransaction(name)
	print('begin', t[3]) # debug

def p_statement_begin_readonly_transaction(t):
	'statement : BEGIN_READONLY LPAREN namelist RPAREN'
	for name in t[3]:
		if name in names:
			print('Error: transaction %s has started!!!' % name)
		assert name not in names
		names[name] = ReadOnlyTransaction(name)
	print('beginRO', t[3]) # debug

def p_statement_end_transaction(t):
	'statement : END LPAREN exprlist RPAREN'
	for trans in t[3]:
		trans.commit()
	print('end', t[3])

def p_statement_fail(t):
	'statement : FAIL LPAREN exprlist RPAREN'
	for val in t[3]:
		print('cite %d is failed' % val)

def p_statement_recover(t):
	'statement : RECOVER LPAREN exprlist RPAREN'
	for val in t[3]:
		print('cite %d is recovered' % val)

def p_statement_read(t):
	'statement : READ LPAREN expression COMMA NAME RPAREN'
	print 'reading %s (transaction %s)' % (t[5], t[3].name)

def p_statement_write(t):
	'statement : WRITE LPAREN expression COMMA NAME COMMA expression RPAREN'
	print 'writing %d to %s (transaction %s)' % (t[7], t[5], t[3].name)

def p_statement_dump(t):
	'statement : DUMP LPAREN RPAREN'
	print('nothing to dump')

def p_statement_assign(t):
	'statement : NAME EQUALS expression'
	names[t[1]] = t[3]

def p_statement_expr(t):
	'statement : expression'
	print(t[1])

def p_namelist_1(t):
	'namelist : NAME'
	t[0] = [t[1]]

def p_namelist_2(t):
	'namelist : NAME COMMA namelist'
	t[0] = [t[1]] + t[3]

def p_exprlist_1(t):
	'exprlist : expression'
	t[0] = [t[1]]

def p_exprlist_2(t):
	'exprlist : expression COMMA exprlist'
	t[0] = [t[1]] + t[3]

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
