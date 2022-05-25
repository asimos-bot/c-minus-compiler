from .token import Token, TokenType
from typing import Tuple
from enum import Enum

class LexError(Exception):
    def __init__(self, message="LexError"):
        self.message = message
        super().__init__(message)
    pass

class LexState(Enum):
        SPACE=1
        IDENTIFIER=2
        NUMBER=3
        OPERATOR=4
        COMPARATOR=4
        DELIMITER=5
        COMMENT = 6
        ERROR=8

class Lex:
    
    def __init__(self):
       self.LETTER= [c for c in "qwertyuiopasdfghjklzxcvbnm"]
       self.NUMBER = ['0','1','2','3','4','5','6','7','8','9']
       self.OPERATOR = ['+','-','*','/']
       self.COMPARATOR = ['<','>','=', '!']
       self.DELIMITER = [';',',','(',')','[',']','{','}']

    def get_tokens_from_file(self, filename: str):
        with open(filename, 'rt') as file:
            return self.get_tokens(file.read())

    def get_tokens(self, source: str):
        i = 0
        add, token = self.get_token(source[i:])
        i += add
        while token.get_type() != TokenType.EOF and i < len(source):
            yield token
            add, token = self.get_token(source[i:])
            i += add
        yield token


    def get_token(self, source: str) -> Tuple[int, Token]:
        state = LexState.SPACE
        token = ''
        i = 0
        for idx, c in enumerate(source):
            next_c = ''
            if idx < len(source)-1:
                next_c = source[idx+1]
            if state == LexState.SPACE:
                if c.lower() in self.LETTER:
                    token += c
                    state = LexState.IDENTIFIER
                elif c == '0':
                    if next_c in self.NUMBER:
                        raise LexError("ERRO\n\tO numero não pode comecar com 0") 
                    token += c     
                    i += 1               
                    return (i, Token(token, TokenType.NUMBER))
                elif c in self.NUMBER:
                    token += c
                    state = LexState.NUMBER
                elif c == '/' and next_c == '*':
                    state = LexState.COMMENT
                elif c in self.DELIMITER :
                    token += c
                    i += 1
                    return (i, Token(token))
                elif c in self.OPERATOR:
                    token += c
                    i += 1
                    return (i, Token(token))
                elif c in self.COMPARATOR:
                    token += c
                    state = LexState.COMPARATOR

            elif state == LexState.IDENTIFIER:
                if c.lower() in self.LETTER or c in self.NUMBER:
                    token += c
                else:
                    return (i, Token(token, TokenType.IDENTIFIER))
                
            elif state == LexState.NUMBER:
                if c.lower() in self.LETTER:
                    state = LexState.ERROR
                    raise LexError(f'ERRO\n\tO numero {token} não pode ser seguido por {c}.')
                elif c in self.NUMBER:
                    token += c
                    state = LexState.NUMBER
                else:
                    return (i, Token(token, TokenType.NUMBER))

            elif state == LexState.COMPARATOR:
                if c == '=':
                    token += c
                    i+=1
                    return (i, Token(token))
                elif c in self.COMPARATOR or c in self.OPERATOR or c in [',',';']:
                    state = LexState.ERROR
                    raise LexError(f'ERRO\n\tO comparador {token+c} é inválido .')
                else:
                    return (i, Token(token))

            elif state == LexState.COMMENT:
                if c == '*' and next_c == '/':
                    return (i, Token(token))
            i+=1