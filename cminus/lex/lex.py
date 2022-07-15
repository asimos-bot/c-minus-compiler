from .token import Token, TokenType
from typing import Tuple
from enum import Enum


class LexError(Exception):
    def __init__(self, message="LexError"):
        self.message = message
        super().__init__(message)
    pass


class LexState(Enum):
    SPACE = 1
    IDENTIFIER = 2
    NUMBER = 3
    OPERATOR = 4
    COMPARATOR = 4
    DELIMITER = 5
    COMMENT = 6
    ERROR = 8
    INITIAL_ZERO = 9
    SPACE_TO_SLASH = 10
    COMMENT_TO_ASTERISK = 11


class Lex:

    def __init__(self):

        self.state = LexState.SPACE
        self.LETTER = [c for c in "qwertyuiopasdfghjklzxcvbnm"]
        self.NUMBER = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.OPERATOR = ['+', '-', '*', '/']
        self.COMPARATOR = ['<', '>', '=', '!']
        self.DELIMITER = [';', ',', '(', ')', '[', ']', '{', '}']
        self.WHITESPACE = ['\n', '\t', ' ']
        self.VALID = self.LETTER + self.NUMBER + self.OPERATOR + \
            self.COMPARATOR + self.DELIMITER + self.WHITESPACE

    def get_tokens_from_file(self, filename: str):
        with open(filename, 'rt') as file:
            for idx, line in enumerate(file.readlines()):
                for token in self.get_tokens(line, idx+1):
                    yield token

    def get_tokens(self, source: str, line: str):
        i = 0
        add, token = self.get_token(source[i:], line)

        i += add
        while token.get_type() != TokenType.EOF and i < len(source):
            if token.get_type() != TokenType.SKIP:
                yield token
            add, token = self.get_token(source[i:], line)
            if token is None:
                return
            i += add
        if token.get_type() != TokenType.SKIP:
            yield token

    def get_token(self, source: str, line: int) -> Tuple[int, Token]:
        token = ''
        i = 0
        for idx, c in enumerate(source):
            if c not in self.VALID and self.state != LexState.COMMENT:
                raise LexError(
                    f"Error at line {line}:  '{c}' character is invalid")
            if self.state == LexState.SPACE:
                if c.lower() in self.LETTER:
                    token += c
                    self.state = LexState.IDENTIFIER
                elif c == '0':
                    self.state = LexState.INITIAL_ZERO
                    token += c
                elif c in self.NUMBER:
                    token += c
                    self.state = LexState.NUMBER
                elif c == '/':
                    token += c
                    self.state = LexState.SPACE_TO_SLASH
                elif c in self.DELIMITER:
                    token += c
                    i += 1
                    self.state = LexState.SPACE
                    return (i, Token(token, line))
                elif c in self.OPERATOR:
                    token += c
                    i += 1
                    self.state = LexState.SPACE
                    return (i, Token(token, line))
                elif c in self.COMPARATOR:
                    token += c
                    self.state = LexState.COMPARATOR
                elif c in self.WHITESPACE:
                    if c == '\n':
                        token += c
                        i += 1
                        return (i, Token(token, line, TokenType.SKIP))

            elif self.state == LexState.INITIAL_ZERO:
                if c in self.NUMBER:
                    raise LexError(
                        f"Error at line {line}:  The number can't start with a 0")
                self.state = LexState.SPACE
                return (i, Token(token, line, TokenType.NUMBER))
            elif self.state == LexState.SPACE_TO_SLASH:
                if c == '*':
                    token += c
                    self.state = LexState.COMMENT
                    i += 1
                    return (i, Token(token, line, TokenType.COMMENT))
                else:
                    self.state = LexState.SPACE
                    return (i, Token(token, line))
            elif self.state == LexState.IDENTIFIER:
                if c.lower() in self.LETTER or c in self.NUMBER:
                    token += c
                else:
                    self.state = LexState.SPACE
                    return (i, Token(token, line, TokenType.IDENTIFIER))

            elif self.state == LexState.NUMBER:
                if c.lower() in self.LETTER:
                    self.state = LexState.ERROR
                    raise LexError(
                        f'Error at line {line}: The number {token} cant be followed by {c}')
                elif c in self.NUMBER:
                    token += c
                    self.state = LexState.NUMBER
                else:
                    self.state = LexState.SPACE
                    return (i, Token(token, line, TokenType.NUMBER))

            elif self.state == LexState.COMPARATOR:
                if c == '=':
                    token += c
                    i += 1
                    self.state = LexState.SPACE
                    return (i, Token(token, line))
                elif c in self.COMPARATOR or c in self.OPERATOR or c in [',', ';']:
                    self.state = LexState.ERROR
                    raise LexError(
                        f'Error at line {line}: The comparator {token+c} is invalid')
                else:
                    self.state = LexState.SPACE
                    return (i, Token(token, line))

            elif self.state == LexState.COMMENT:
                if c == '*':
                    self.state = LexState.COMMENT_TO_ASTERISK
                    token += c
                else:
                    token += c
            elif self.state == LexState.COMMENT_TO_ASTERISK:
                if c == '/':
                    self.state = LexState.SPACE
                    token += c
                    i += 1
                    return (i, Token(token, line, token_type=TokenType.COMMENT))
                else:
                    self.state = LexState.COMMENT
                    token += c
            i += 1
        if self.state == LexState.COMMENT:
            return (len(token), Token(token, line, TokenType.COMMENT,))
        return (i, None)


if __name__ == "__main__":
    lex: Lex = Lex()
    with open('output/token_list.txt', 'w') as f:
        for token in lex.get_tokens_from_file('source_code.txt'):
            f.write(f'{token}\n')
