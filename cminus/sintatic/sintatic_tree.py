from mimetypes import init
import string
from tkinter import N
from lex.token import Token, TokenType
from lex.lex import Lex
from enum import Enum


class ProductionState(Enum):
    PROGRAM = 1
    DECLARATION_LIST = 2
    DECLARATION = 3
    VAR_DECLARATION = 4
    TYPE_SPECIFIER = 5
    FUN_DECLARATION = 6
    PARAMS = 7
    PARAM_LIST_1 = 8
    PARAM_LIST_2 = 9
    PARAM = 10
    COMPOUND_STMT = 11
    LOCAL_DECLARATIONS = 12
    STATEMENT_LIST = 13
    STATEMENT = 14
    EXPRESSION_STMT = 15
    SELECTION_STMT = 16
    ITERATION_STMT = 17
    RETURN_STMT = 18
    EXPRESSION = 19
    VAR = 20
    SIMPLE_EXPRESSION = 21
    RELOP = 22
    ADDITIVE_EXPRESSION = 23
    ADDOP = 24
    TERM = 25
    MULOP = 26
    FACTOR = 27
    CALL = 28
    ARGS = 29
    ARG_LIST = 30
    ID = 31
    NUM = 32


class Node:

    def __init__(self, parent, symbol: ProductionState, token: Token = None):
        self.parent = parent
        self.symbol = symbol
        self.token = token
        self.children = []

# terminal states - num , id , mulop, , addop, relop, , ',' , [] , ; , int , void


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens

    def parse(self) -> Node:
        root = Node(parent=None, symbol=ProductionState.PROGRAM)
        self.symbol_program(root)

    def symbol_program(self, parent: Node, token: Token) -> bool:
        node = Node(parent=parent, symbol=ProductionState.DECLARATION_LIST)
        parent.append(node)
        return self.symbol_declaration_list(node)

    def symbol_declaration_list(self, token: Token, parent: Node):
        # < declaration-list > : := <declaration >  <declaration-list > | Ɛ
        node = Node(parent=parent, symbol=ProductionState.DECLARATION)
        if self.symbol_declaration(token, node):
            return True
        else:
            return False

    def symbol_declaration(self, token: Token, parent: Node) -> bool:
        # <declaration> ::= <var-declaration> | <fun-declaration>
        node = Node(parent=parent, symbol=ProductionState.DECLARATION)
        if self.symbol_var_declaration(token, node):
            return True
        elif self.symbol_fun_declaration(token, node):
            return True
        else:
            return False

    def symbol_var_declaration(self, token: Token, parent: Node) -> bool:
        # <var-declaration> ::= <type-specifier> <id>; | <type-specifier> <id> [ <num> ];
        node = Node(parent=parent, symbol=ProductionState.VAR_DECLARATION)
        if self.symbol_type_specifier(token, node):
            if self.symbol_id(node):

    def symbol_type_specifier(self, token: Token, parent: Node) -> bool:
        # <type-specifier> ::= int | void

    def symbol_declaration(self, token: Token, parent: Node) -> bool:
        # <fun-declaration> ::= <type-specifier> <id> ( <params> ) <compound-stmt>

    def symbol_declaration(self, token: Token, parent: Node) -> bool:
        # <params> ::= <param-list> | void

    def symbol_declaration(self, token: Token, parent: Node) -> bool:
        # <param-list> ::= <param> <param-list>*

    def symbol_declaration(self, token: Token, parent: Node) -> bool:
        # <param-list>* ::= , <param> <param-list>* | Ɛ

    def symbol_declaration(self, token: Token, parent: Node) -> bool:
        # <param> ::= <type-specifier> <id> | <type-specifier> <id> [ ]

    def symbol_declaration(self, token: Token, parent: Node) -> bool:
        # <compound-stmt> ::= { <local-declarations> <statement-list> }

    def symbol_declaration(self, token: Token, parent: Node) -> bool:
        # <local-declarations> ::= <var-declaration>  <local-declarations> | Ɛ

    def symbol_declaration(self, token: Token, parent: Node) -> bool:
        # <statement-list> ::= <statement> <statement-list>  | Ɛ

    def symbol_declaration(self, token: Token, parent: Node) -> bool:
        # <statement> ::= <expression-stmt> | <compound-stmt> | <selection-stmt> | <iteration-stmt> | <return-stmt>

    def symbol_declaration(self, token: Token, parent: Node) -> bool:
        # <expression-stmt> ::= <expression> ; | ;

    def symbol_declaration(self, token: Token, parent: Node) -> bool:
        # <selection-stmt> ::= if ( <expression> ) <statement> | if ( <expression> ) <statement> else <statement>

    def symbol_declaration(self, token: Token, parent: Node) -> bool:
        # <iteration-stmt> ::= while ( <expression> ) <statement>

    def symbol_declaration(self, token: Token, parent: Node) -> bool:
        # <return-stmt> ::= return ; | return <expression> ;

    def symbol_declaration(self, token: Token, parent: Node) -> bool:
        # <expression> ::= <var> = <expression> | <simple-expression>

    def symbol_declaration(self, token: Token, parent: Node) -> bool:
        # <var> ::= <id> | <id> [ <expression> ]

    def symbol_declaration(self, token: Token, parent: Node) -> bool:
        # <simple-expression> ::= <additive-expression> <relop> <additive-expression> |<additive-expression>

    def symbol_declaration(self, token: Token, parent: Node) -> bool:
        # <relop> ::= <= | < | > | >= | == | !=

    def symbol_declaration(self, token: Token, parent: Node) -> bool:
        # <additive-expression> ::=  <term> <addop> <additive-expression> | <term>

    def symbol_declaration(self, token: Token, parent: Node) -> bool:
        # <addop> ::= + | -

    def symbol_declaration(self, token: Token, parent: Node) -> bool:
        # <term> ::= <factor> <mulop> <term> | <factor>

    def symbol_declaration(self, token: Token, parent: Node) -> bool:
        # <mulop> ::= * | /

    def symbol_declaration(self, token: Token, parent: Node) -> bool:
        # <factor> ::= ( <expression> ) | <var> | <call> | <num>

    def symbol_declaration(self, token: Token, parent: Node) -> bool:
        # <call> ::= <id> ( <args> )

    def symbol_declaration(self, token: Token, parent: Node) -> bool:
        # <args> ::= <arg-list> | Ɛ

    def symbol_declaration(self, token: Token, parent: Node) -> bool:
        # <arg-list> ::=  <expression> , <arg-list>  | <expression>

    def symbol_declaration(self, token: Token, parent: Node) -> bool:
        # num

    def symbol_declaration(self, token: Token, parent: Node) -> bool:
        # id

    def factor(self, token: Token, node: Node) -> bool:
        # factor ::= (<expression>) | <var> | <call> | <num>
        if token.token_type == TokenType.NUMBER:
            node.children.append(node)


if __name__ == "__main__":
    parser = Parser()
