
grammar CTL;
 
options {
    language = Python;
}

@header {
import sys
import traceback
 
from SimpleCalcLexer import SimpleCalcLexer
}
 
@main {
def main(argv, otherArg=None):
  char_stream = ANTLRFileStream(sys.argv[1])
  lexer = SimpleCalcLexer(char_stream)
  tokens = CommonTokenStream(lexer)
  parser = SimpleCalcParser(tokens);
 
  try:
        parser.expr()
  except RecognitionException:
    traceback.print_stack()
}
 
/*------------------------------------------------------------------
 * PARSER RULES
 *------------------------------------------------------------------*/
 
expr    : term ( ( AND | UNTIL )  term )* ;
 
term    : factor ( ( AND | UNTIL ) factor )* 
		| (( NOT | NEXT | ALWAYS ) factor )*;
 
factor  : ATOM ;

AND    	: '&' ;
NOT   	: '!' ;
NEXT    : 'X' ;
EXISTS 	: 'E' ;
UNTIL 	: 'U' ;
ALWAYS 	: 'B' ;
 
 
/*------------------------------------------------------------------
 * LEXER RULES
 *------------------------------------------------------------------*/
 
ATOM  :   [a-z]+ ; 
 
WHITESPACE : ( '\t' | ' ' | '\r' | '\n'| '\u000C' )+ ;