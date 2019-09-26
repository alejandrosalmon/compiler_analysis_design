#!/usr/bin/python
# from __future__ import annotations

import os, sys
import ply.lex as lex
from ply import yacc as yacc
import re

reserved = {
	# DEFINING
	'define': 'DEFINE',
	'let': 'LOCAL_DEFINE',
	# CONDITIONALS
	'if' :'IF',
	'cond': 'CONDITIONAL',
	'else': 'ELSE',
	# LIST
	'car': 'LIST_HEAD',
	'cdr': 'LIST_TAIL',
	'cons': 'LIST_CONC',
	'empty': 'LIST_EMPTY',
	'last': 'LIST_LAST', 
	# OPERATORS
	'expt': 'OP_ARITH_EXPONENT',
	'modulo': 'OP_ARITH_MODULO',
	'remainder': 'OP_ARITH_REMAINDER',
	'not': 'OP_LOGIC_NOT',
	'and': 'OP_LOGIC_AND',
	'or': 'OP_LOGIC_OR',
	# IO
	'newline': 'IO_NEWLINE',
	'display': 'IO_DISPLAY_CONSOLE',
	'read': 'IO_READ',
	# LAMBDA CALC
	'lambda': 'LAMBDA',
	'map': 'MAP',
	# LOOP
	'loop': 'LOOP',
	'do': 'DO'
}

tokens = [
	 #IDENTIFIERS
    'ID',
    #COMMENTS
    'SINGLE_COM', # ;...
    'BLOCK_COM', # #|...|#
    #LITERALS
    'LIT_STRING', # "HOla34"  'holGC456'
    'LIT_CHAR', # 'a' 'b'
    'LIT_INT', # 9
    'LIT_FLOAT', # 9.1
    'LIT_LIST', # '()  '(1 2 3 4)
    # BOOLEAN VALUES
	'FALSE',
	'TRUE',
    #SYMBOLS
    'S_LPAREN', # (
    'S_RPAREN', # )
    'S_LBRACKET', # [
    'S_RBRACKET', # ]
    'S_HASH',
    #ARITHMETIC OPERATOR
    'OP_ARITH_ADD', # +
    'OP_ARITH_SUBSTRACT', # -
    'OP_ARITH_MULTIPLY', # *
    'OP_ARITH_DIVIDE', # /
    #OPERATOR EQUALITY AND RELATIONAL
    'OP_EQUALITY_GREATER', # >
    'OP_EQUALITY_LESSER', # <
    'OP_EQUALITY_EQUAL', # =
    'OP_EQUALITY_LESSER_EQUAL',
    'OP_EQUALITY_GREATER_EQUAL',
    # IS OPERATORS
    'OP_IS_EQUAL', # eq?
    'OP_IS_NOT_EQUAL', # neq?
	'OP_IS_EQUAL2', # equal?
	'OP_IS_EMPTY', # empty?
	'OP_IS_NULL', # null?
	'OP_IS_NUMBER', # number?
	'OP_IS_POSITIVE', # positive?
	'OP_IS_NEGATIVE', # negative?
	'OP_IS_STRING', # string?
	'OP_IS_LIST', # list?
	'OP_IS_EXISTS', # exists-in?
    # IO
    'IO_INPUT_FILE',
    'IO_OUTPUT_FILE',
    'IO_READ_CONSOLE',
    # ERROR
    'ERROR',
	] + list(reserved.values())

# ------------REGULAR EXPRESSIONS
# Comments
def t_SINGLE_COM(t):
	r';.*(\n)*'
	pass

def t_BLOCK_COM(t):
	r'\#\|(.*\s*)*\|\#'
	pass

# IO
def t_INPUT_FILE(t):
	r'open-input-file'
	return t

def t_OUTPUT_FILE(t):
	r'open-output-file'
	return t

def t_IO_READ_CONSOLE(t):
	r'read\-line'
	return t

# IS OPERATORS
def t_OP_IS_EQUAL(t):
	r'eq\?'
	return t

def t_OP_IS_NOT_EQUAL(t):
	r'neq\?'
	return t

def t_OP_IS_EQUAL2(t):
	r'equal\?'
	return t

def t_OP_IS_EMPTY(t):
	r'empty\?'
	return t

def t_OP_IS_NULL(t):
	r'null\?'
	return t

def t_OP_IS_NUMBER(t):
	r'number\?'
	return t

def t_OP_IS_POSITIVE(t):
	r'positive\?'
	return t

def t_OP_IS_NEGATIVE(t):
	r'negative\?'
	return t

def t_OP_IS_STRING(t):
	r'string\?'
	return t

def t_OP_IS_LIST(t):
	r'list\?'
	return t

def t_OP_IS_EXISTS(t):
	r'exists-in\?'
	return t

#SYMBOLS
t_S_LPAREN = r'\(' # (
t_S_RPAREN = r'\)' # )
t_S_LBRACKET = r'\[' # [
t_S_RBRACKET = r'\]' # ]
t_S_HASH = r'\#' # #

#Operator EQUALITY
t_OP_EQUALITY_EQUAL = r'\=' # =
t_OP_EQUALITY_GREATER = r'\>' # >
t_OP_EQUALITY_LESSER = r'\<' # <
t_OP_EQUALITY_LESSER_EQUAL = r'\<\='
t_OP_EQUALITY_GREATER_EQUAL = r'\>\='

#ARITHMETIC OPERATOR
t_OP_ARITH_ADD = r'\+' # +
t_OP_ARITH_SUBSTRACT = r'\-' # -
t_OP_ARITH_MULTIPLY = r'\*' # *
t_OP_ARITH_DIVIDE = r'\/' # /

#IGNORED CHARACTERS
t_ignore_space = r'\s'
t_ignore_newline = r'\n'
t_ignore_tab = r'\t'
t_ignore_vcmd = r'\v'

#Lit
t_LIT_INT = r'[+-]?([0-9]+)'
t_LIT_FLOAT = r'[+-]?([0-9]+)(\.[0-9]+)'
t_LIT_STRING = r'(?:\'(?:[^\']+|\'\')*\'|\"(?:[^\"]+|\"\")*\")' # (?:\'(?:[^\']+|\'\')*\'|\"(?:[^"]+|\"\")*\")
t_LIT_CHAR = r'\'[^\']+\''

# BOOLEAN VALUES
t_TRUE = r'\#t'
t_FALSE = r'\#f'

def t_LIT_LIST(t):
	r"'\(.*\)"
	return t

def t_ID(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	t.type = reserved.get(t.value, "ID")
	return t

def t_error(t): 
	print("\nIllegal character: '%s' encountered" % t.value[0])
	t.type = "ERROR"
	t.value = t.value[0]
	t.lexer.skip(1)
	return t

# BUILD THE LEXER
lexer = lex.lex()

#########################################################
# BUILD THE PARSER
def p_program(p):
	'''
	program : form
	'''
	print('Program detected')

def p_form_a(p):
	'''
	form : definition
		 | expression
	'''
	print('PROGRAM FORM A')

def p_form_b(p):
	'''
	form : definition definition
	'''
	print('PROGRAM FORM B')

def p_definition(p):
	'''
	definition : S_LPAREN DEFINE ID body S_RPAREN
	'''
	print('DEFINITION')

def p_definition_function(p):
	'''
	definition :  S_LPAREN DEFINE function body S_RPAREN
	'''
	print('FUNCTION DEFINITION')

def p_function_vars(p):
	'''
	function : S_LPAREN ID ID S_RPAREN
		 	 | S_LPAREN ID ID ID S_RPAREN
	'''

def p_body_exp(p):
	'''
	body : expression
		 | definition
	'''
	# print('BODY')

def p_expression(p):
	'''
	expression : constant
			   | if_expression
			   | do_expression
			   | cond_expression
			   | comparison_expression
			   | ID
			   | display
	'''
	# print('EXPRESSION')

def p_if_expression_a(p):
	'''
	if_expression : S_LPAREN IF comparison_expression expression S_RPAREN
	'''
	print('IF EXPRESSION')

def p_if_expression_b(p):
	'''
	if_expression : S_LPAREN IF comparison_expression expression expression S_RPAREN
	'''
	print('IF-ELSE EXPRESSION')

def p_cond_expression_a(p):
    '''
    cond_expression : S_LPAREN CONDITIONAL S_LBRACKET comparison_expression expression S_RBRACKET S_RPAREN
    '''
    print('COND EXPRESSION A')

def p_cond_expression_b(p):
    '''
    cond_expression : S_LPAREN CONDITIONAL S_LBRACKET comparison_expression expression S_RBRACKET S_LBRACKET ELSE expression S_RBRACKET S_RPAREN
    '''
    print('COND-ELSE EXPRESSION B')

def p_comparison_expression(p):
	'''
	comparison_expression : S_LPAREN comparison expression expression S_RPAREN
	'''
	print('COMPARISON')

def p_comparison(p):
	'''
	comparison : OP_EQUALITY_GREATER
			   | OP_EQUALITY_LESSER
			   | OP_EQUALITY_EQUAL
			   | OP_EQUALITY_LESSER_EQUAL
			   | OP_EQUALITY_GREATER_EQUAL
			   | OP_IS_EQUAL
			   | OP_IS_NOT_EQUAL
			   | OP_IS_EQUAL2
			   | OP_IS_EMPTY
			   | OP_IS_NULL
			   | OP_IS_NUMBER
			   | OP_IS_POSITIVE
			   | OP_IS_NEGATIVE
			   | OP_IS_STRING
			   | OP_IS_LIST
	'''

def p_do_expression(p):
	'''
	do_expression : S_LPAREN DO id_set operation comparison_expression expression S_RPAREN
	'''
	print('CYCLE')

def p_id_set(p):
	'''
	id_set : S_LPAREN ID constant S_RPAREN
	'''
	# print('SET ID')

def p_operation(p):
    '''
    operation : S_LPAREN symbol expression expression S_RPAREN
    '''

def p_boolean(p):
	'''
	boolean : TRUE
			| FALSE
	'''	
	# print('BOOLEAN')

def p_constant(p):
	'''
	constant : LIT_INT
			 | LIT_FLOAT
			 | LIT_CHAR
			 | LIT_STRING
			 | boolean
	'''
	# print('CONSTANT')

def p_symbol(p):
    '''
    symbol : OP_ARITH_ADD
           | OP_ARITH_SUBSTRACT
           | OP_ARITH_DIVIDE
           | OP_ARITH_MULTIPLY
           | OP_ARITH_EXPONENT
           | OP_ARITH_MODULO
           | OP_ARITH_REMAINDER
    '''

def p_display(p):
    '''
    display : S_LPAREN IO_DISPLAY_CONSOLE expression S_RPAREN
    '''

def p_error(t):
	print("Syntax error.")
	# sys.exit()

parser = yacc.yacc()

def main(argv):
    if (len(sys.argv) != 2):
        print ('usage: python lexer.py <test_file>')
        return -1
    try:        
        f = open(sys.argv[1], "r") 
        tests = f.read()

        for test in tests.split('\n\n'):
        	lexer.input(test)
        	print('========= TEST ============{ \n\n' +test+ '\n}======================')
        	
        	# CHECAR TOKENS
        	while True:
        		tok = lexer.token()
        		if not tok:
        			break
        		print(tok)
        	if(sys.argv[1].startswith('prueba_parser')):
        		print("\nParser:")
        		parser.parse(test)

    except Exception as e:        
        print ('lexer.py: File does not exist')  
        print ("\t" + str(e))
        return -2    

if __name__ == "__main__":
    main(sys.argv[1:])