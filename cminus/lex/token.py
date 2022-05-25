from enum import Enum


class TokenType(Enum):
    IDENTIFIER = 1
    NUMBER = 2
    COMMENT = 3
    SPECIAL_ADD = '+'
    SPECIAL_SUB = '-'
    SPECIAL_MUL = '*'
    SPECIAL_DIV = '/'
    SPECIAL_LT = '<'
    SPECIAL_LE = '<='
    SPECIAL_GT = '>'
    SPECIAL_GE = '>='
    SPECIAL_EQ = '=='
    SPECIAL_NE = '!='
    SPECIAL_ASSIGN = '='
    SPECIAL_SEMICOLON = ';'
    SPECIAL_COMMA = ','
    SPECIAL_PARENTHESIS_OPEN = '('
    SPECIAL_PARENTHESIS_CLOSE = ')'
    SPECIAL_BRACKET_OPEN = '['
    SPECIAL_BRACKET_CLOSE = ']'
    SPECIAL_CURLY_BRACKET_OPEN = '{'
    SPECIAL_CURLY_BRACKET_CLOSE = '}'
    KEYWORD_ELSE = 'else'
    KEYWORD_IF = 'if'
    KEYWORD_INT = 'int'
    KEYWORD_RETURN = 'return'
    KEYWORD_VOID = 'void'
    KEYWORD_WHILE = 'while'
    EOF = ''


class Token:
    def __init__(self,  content: str, token_type: TokenType = None):
        if token_type is None:
            token_type = TokenType(content)
        if token_type == TokenType.IDENTIFIER:
            try:
                token_type = TokenType(content)
            except Exception as e:
                pass
        self.token_type = token_type
        self.content = content

    def get_type(self) -> TokenType:
        return self.token_type

    def __repr__(self) -> str:
        return f"[type = {self.token_type.name}, token = '{self.content}']"

