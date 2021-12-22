"""
<s-exp-list> ::= <s-exp> <s-exp-list> | <empty>
<s-exp> ::=  "(" + name + <data> + ")"
<name> ::= name | empty
<data> ::= <string> | <number> | <s-exp> 
 
"""
from json.encoder import JSONEncoder
import sys
import json
from pathlib import Path
from pprint import pprint
from sly import Lexer, Parser
 
counter = 0
 
class ConfLexer(Lexer):
    tokens = {BEGIN, END, NAME, NUMBER, STRING}
    BEGIN = r'\('
 
    ignore = r' \t'
    ignore_newline = r'\n'
    NAME = r'[^ \(\)0123456789\t\nйцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮЁ]+'
    NUMBER = r'[0123456789]+'
    STRING = r'[^\(\)\t\#\nqwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM]+'
 
    END = r'\)' 
 
class ConfParser(Parser):
    tokens = ConfLexer.tokens
 
    @_('sexp sexp sexp')
    def sexplist(self, p):
        return [p.sexp0] + [p.sexp1] + [p.sexp2]
 
    @_('BEGIN NAME sexp sexplist END')
    def sexp(self, p):
        return [p.NAME] + [p.sexp] + p.sexplist
 
    @_('BEGIN sexp sexplist END')
    def sexp(self, p):
        return [p.sexp] + p.sexplist
 
    @_('BEGIN NAME data END')
    def sexp(self, p):
        global counter
        counter += 1
        if (counter < 62):
              return [p.data]
        else:
              return [p.NAME] + [p.data]
 
    @_('sexp sexplist')
    def sexplist(self, p):
        return [p.sexp] + p.sexplist
 
    @_('empty')
    def sexplist(self, p):
        return []
 
    @_('STRING')
    def data(self, p):
        return [p.STRING]
 
    @_('NUMBER')
    def data(self, p):
        return [p.NUMBER]
 
    @_('empty')
    def data(self, p):
        return []
 
    @_('')
    def empty(self, p):
        pass
 
arg = sys.argv[1]
file = open(str(arg), 'r')
text = file.read()
lexer = ConfLexer()
parser = ConfParser()
data = parser.parse(lexer.tokenize(text))
Path("result.json").write_text(json.dumps(data, indent=2, ensure_ascii=False))
pprint(parser.parse(lexer.tokenize(text)))