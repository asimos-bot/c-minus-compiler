from ..lex.token import Token, TokenType
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


class Node:

    def __init__(self, parent, symbol: ProductionState, token: Token = None, depth: int = 0):
        self.parent = parent
        self.symbol = symbol
        self.token = token
        self.children = []
        self.depth = depth

    def append(self, node):
        node.depth = self.depth + 1
        self.children.append(node)

    def append_all(self, nodes):
        for node in nodes:
            node.depth = self.depth + 1
        self.children += nodes

    def __repr__(self):
        half = len(self.children)//2
        tabs = "".join(["\t"] * self.depth)
        s = ""
        for child in self.children[half:][::-1]:
            s += str(child.__repr__())
        s += tabs
        # has self.token -> leaf (terminal)
        # has self.symbol -> trunk (non terminal)
        if self.token is None:
            s += str(self.symbol.name)
        else:
            s += str(self.token)
        for child in self.children[:half][::-1]:
            s += str(child.__repr__())
        return s


# terminal states - num , id , mulop, , addop, relop, , ',' , [] , ; , int , void


class ParserException(Exception):
    def __init__(self, token):
        self.message = "Error at line {}: {}".format(token.line, token.content)
        super().__init__(self.message)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self) -> Node:
        return self.symbol_program()

    def symbol_program(self) -> bool:
        root = Node(parent=None, symbol=ProductionState.PROGRAM)
        self.symbol_declaration_list(root)
        return root

    def symbol_declaration_list(self, parent: Node):
        # < declaration-list > : := <declaration >  <declaration-list > | Ɛ
        node = Node(parent=parent, symbol=ProductionState.DECLARATION_LIST)
        if self.symbol_declaration(node):
            parent.append(node)
            return True
        return False

    def symbol_declaration(self, parent: Node) -> bool:
        # <declaration> ::= <var-declaration> | <fun-declaration>
        pos = self.pos
        node = Node(parent=parent, symbol=ProductionState.DECLARATION)
        if self.symbol_var_declaration(node):
            parent.children.append(node)
            return True

        # reset node children
        self.pos = pos
        node.children = []
        if self.symbol_fun_declaration(node):
            parent.children.append(node)
            return True
        return False

    def symbol_var_declaration(self, parent: Node) -> bool:
        # <var-declaration> ::= <type-specifier> <id> ; | <type-specifier> <id> [ <num> ];
        pos = self.pos
        node = Node(parent=parent, symbol=ProductionState.VAR_DECLARATION)
        if self.symbol_type_specifier(node):
            pos = self.pos
            if self.symbol_identifier(node):
                if self.symbol_semicolon(node):
                    parent.children.append(node)
                    return True
                else:
                    return False
            # reset node children
            self.pos = pos
            node.children = []
            if self.symbol_bracket_open(node):
                if self.symbol_number(node):
                    if self.symbol_bracket_close(node) and self.symbol_semicolon(node):
                        parent.children.append(node)
                        return True
        return False

    def symbol_type_specifier(self, parent: Node) -> bool:
        # <type-specifier> ::= int | void
        pos = self.pos
        node = Node(parent=parent, symbol=ProductionState.TYPE_SPECIFIER)
        if self.tokens[0].token_type == TokenType.KEYWORD_INT:
            self.match(node)
            return True
        elif self.tokens[0].token_type == TokenType.KEYWORD_VOID:
            self.match(node)
            return True
        return False
        parent.children.append(node)
        return True

    def symbol_fun_declaration(self, parent: Node) -> bool:
        # <fun-declaration> ::= <type-specifier> <id> ( <params> ) <compound-stmt>
        node = Node(parent=parent, symbol=ProductionState.FUN_DECLARATION)
        if self.symbol_type_specifier(node) and self.tokens[0].token == TokenType.IDENTIFIER:
            if self.tokens[1].token_type == TokenType.SPECIAL_PARENTHESIS_OPEN:
                if self.symbol_params(node):
                    if self.tokens[2].token_type == TokenType.SPECIAL_PARENTHESIS_CLOSE:
                        if self.symbol_compound_stmt():
                            self.match(node)
                            self.match(node)
                            parent.children.append(node)
                            return True
        return False

    def symbol_params(self, parent: Node) -> bool:
        # <params> ::= <param-list> | void
        node = Node(parent=parent, symbol=ProductionState.PARAMS)
        if self.symbol_params(node):
            parent.children.append(node)
            return True
        elif self.tokens[0].token_type == TokenType.KEYWORD_VOID:
            self.match(node)
            parent.children.append(node)
            return True
        return False

    def symbol_param_list_1(self, parent: Node) -> bool:
        # <param-list> ::= <param> <param-list>*
        node = Node(parent=parent, symbol=ProductionState.PARAM_LIST_1)
        if self.symbol_param(node):
            self.symbol_param_list_2(node)
            parent.children.append(node)
            return True
        return False

    def symbol_param_list_2(self, parent: Node) -> bool:
        # <param-list>* ::= , <param> <param-list>* | Ɛ
        node = Node(parent=parent, symbol=ProductionState.PARAM_LIST_2)
        if self.tokens[0].token_type == TokenType.SPECIAL_COMMA:
            if self.symbol_param(node):
                self.match(node)
                self.symbol_param_list_2(node)
                parent.children.append(node)
                return True
        return False

    def symbol_param(self, parent: Node) -> bool:
        # <param> ::= <type-specifier> <id> | <type-specifier> <id> [ ]
        node = Node(parent=parent, symbol=ProductionState.PARAM)
        if self.symbol_type_specifier(node) and self.tokens[0].token_type == TokenType.IDENTIFIER:
            if self.tokens[1].token_type == TokenType.SPECIAL_BRACKET_OPEN:
                if self.tokens[2].token_type == TokenType.SPECIAL_BRACKET_CLOSE:
                    self.match(node)
                    self.match(node)
                    self.match(node)
                    parent.children.append(node)
                    return True
            parent.children.append(node)
            return True
        return False

    def symbol_compound_stmt(self, parent: Node) -> bool:
        # <compound-stmt> ::= { <local-declarations> <statement-list> }
        node = Node(parent=parent, symbol=ProductionState.COMPOUND_STMT)
        if self.tokens[0].token_type == TokenType.SPECIAL_CURLY_BRACKET_OPEN:
            if self.symbol_local_declarations(node):
                if self.symbol_statement_list(node):
                    if self.tokens[0].token_type == TokenType.SPECIAL_CURLY_BRACKET_CLOSE:
                        self.match(node)
                        parent.children.append(node)
                        return True
        return False

    def symbol_local_declarations(self, parent: Node) -> bool:
        # <local-declarations> ::= <var-declaration>  <local-declarations> | Ɛ
        node = Node(parent=parent, symbol=ProductionState.LOCAL_DECLARATIONS)
        if self.symbol_var_declaration(node):
            self.symbol_local_declarations(node)
            parent.children.append(node)
            return True
        return False

    def symbol_statement_list(self, parent: Node) -> bool:
        # <statement-list> ::= <statement> <statement-list>  | Ɛ
        node = Node(parent=parent, symbol=ProductionState.STATEMENT_LIST)
        if self.symbol_statement(node):
            self.symbol_statement_list(node)
            parent.children.append(node)
            return True
        return False

    def symbol_statement(self, parent: Node) -> bool:
        # <statement> ::= <expression-stmt> | <compound-stmt> | <selection-stmt> | <iteration-stmt> | <return-stmt>
        node = Node(parent=parent, symbol=ProductionState.STATEMENT)
        if self.symbol_expression_stmt(node):
            parent.children.append(node)
            return True
        elif self.symbol_compound_stmt(node):
            parent.children.append(node)
            return True
        elif self.symbol_selection_stmt(node):
            parent.children.append(node)
            return True
        elif self.symbol_iteration_stmt(node):
            parent.children.append(node)
            return True
        elif self.symbol_return_stmt(node):
            parent.children.append(node)
            return True
        return False

    def symbol_expression_stmt(self, parent: Node) -> bool:
        # <expression-stmt> ::= <expression> ; | ;
        node = Node(parent=parent, symbol=ProductionState.EXPRESSION_STMT)
        if self.symbol_expression(node):
            if self.tokens[0].token_type == TokenType.SPECIAL_COMMA:
                self.match(node)
                parent.children.append(node)
                return True
        elif self.tokens[0].token_type == TokenType.SPECIAL_COMMA:
            self.match(node)
            parent.children.append(node)
            return True
        return False

    def symbol_selection_stmt(self, parent: Node) -> bool:
        # <selection-stmt> ::= if ( <expression> ) <statement> | if ( <expression> ) <statement> else <statement>
        node = Node(parent=parent, symbol=ProductionState.SELECTION_STMT)
        if self.tokens[0].token_type == TokenType.KEYWORD_IF:
            self.match(node)
            if self.tokens[1].token_type == TokenType.SPECIAL_PARENTHESIS_OPEN:
                if self.symbol_expression(node):
                    if self.tokens[1].token_type == TokenType.SPECIAL_PARENTHESIS_CLOSE:
                        self.match(node)
                        if self.symbol_statement(node):
                            if self.tokens[3].token_type == TokenType.KEYWORD_ELSE:
                                if self.symbol_expression(node):
                                    parent.children.append(node)
                                    return True
                            else:
                                return True
        return False

    def symbol_iteration_stmt(self, parent: Node) -> bool:
        # <iteration-stmt> ::= while ( <expression> ) <statement>
        node = Node(parent=parent, symbol=ProductionState.ITERATION_STMT)
        if self.tokens[0].token_type == TokenType.KEYWORD_WHILE:
            if self.tokens[1].token_type == TokenType.SPECIAL_PARENTHESIS_OPEN:
                if self.symbol_expression(node):
                    if self.tokens[2].token_type == TokenType.SPECIAL_PARENTHESIS_CLOSE:
                        if self.symbol_statement(node):
                            self.match(node)
                            self.match(node)
                            self.match(node)
                            parent.children.append(node)
                            return True
        return False

    def symbol_return_stmt(self, parent: Node) -> bool:
        # <return-stmt> ::= return ; | return <expression> ;
        node = Node(parent=parent, symbol=ProductionState.RETURN_STMT)
        if self.tokens[0].token_type == TokenType.KEYWORD_RETURN:
            self.match(node)
            if self.tokens[0].token_type == TokenType.SPECIAL_SEMICOLON:
                self.match(node)
                return True
            if self.symbol_expression(node):
                if self.tokens[0].token_type == TokenType.SPECIAL_SEMICOLON:
                    self.match(node)
                    return True
        return False

    def symbol_expression(self, parent: Node) -> bool:
        # <expression> ::= <var> = <expression> | <simple-expression>
        node = Node(parent=parent, symbol=ProductionState.EXPRESSION)
        if self.symbol_var(node):
            if self.tokens[0].token_type == TokenType.SPECIAL_SEMICOLON:
                self.match(node)
                if self.symbol_expression(node):
                    return True
        elif self.symbol_simple_expression(node):
            return True
        return False

    def symbol_var(self, parent: Node) -> bool:
        # <var> ::= <id> | <id> [ <expression> ]
        node = Node(parent=parent, symbol=ProductionState.VAR)
        if self.tokens[0].token_type == TokenType.IDENTIFIER:
            if self.tokens[1].token_type == TokenType.SPECIAL_BRACKET_OPEN:
                if self.symbol_expression(node):
                    if self.tokens[2].token_type == TokenType.SPECIAL_BRACKET_CLOSE:
                        self.match(node)
                        self.match(node)
                        self.match(node)
                        return True
                return False
            self.match(node)
            return True
        return False

    def symbol_simple_expression(self, parent: Node) -> bool:
        # <simple-expression> ::= <additive-expression> <relop> <additive-expression> |<additive-expression>
        node = Node(parent=parent, symbol=ProductionState.SIMPLE_EXPRESSION)
        if self.symbol_additive_expression(node):
            if self.symbol_relop(node):
                if self.symbol_additive_expression(node):
                    parent.children.append(node)
                    return True
            else:
                parent.children.append(node)
                return True
        return False

    def symbol_relop(self, parent: Node) -> bool:
        # <relop> ::= <= | < | > | >= | == | !=
        node = Node(parent=parent, symbol=ProductionState.RELOP)
        if self.tokens[0].token_type in {TokenType.SPECIAL_LT, TokenType.SPECIAL_LE, TokenType.SPECIAL_GT, TokenType.SPECIAL_GE, TokenType.SPECIAL_EQ, TokenType.SPECIAL_NE}:
            self.match(node)
            parent.children.append(node)
            return True

    def symbol_additive_expression(self, parent: Node) -> bool:
        # <additive-expression> ::=  <term> <addop> <additive-expression> | <term>
        node = Node(parent=parent, symbol=ProductionState.ADDITIVE_EXPRESSION)
        if self.symbol_term(node):
            if self.symbol_addop(node):
                if self.symbol_additive_expression(node):
                    parent.children.append(node)
                    return True
                else:
                    return False
            parent.children.append(node)
            return True
        return False

    def symbol_addop(self, parent: Node) -> bool:
        # <addop> ::= + | -
        node = Node(parent=parent, symbol=ProductionState.ADDOP)
        if self.tokens[0].token_type == TokenType.SPECIAL_ADD:
            self.match(node)
            parent.children.append(node)
            return True
        elif self.tokens[0].token_type == TokenType.SPECIAL_SUB:
            self.match(node)
            parent.children.append(node)
            return True
        return False

    def symbol_term(self, parent: Node) -> bool:
        # <term> ::= <factor> <mulop> <term> | <factor>
        node = Node(parent=parent, symbol=ProductionState.TERM)
        if self.symbol_factor(node):
            if self.symbol_mulop(node):
                if self.symbol_term(node):
                    parent.children.append(node)
                    return True
                else:
                    return False
            parent.children.append(node)
            return True
        return False

    def symbol_mulop(self, parent: Node) -> bool:
        # <mulop> ::= * | /
        node = Node(parent=parent, symbol=ProductionState.MULOP)
        if self.tokens[0].token_type == TokenType.SPECIAL_MUL:
            self.match(node)
            parent.children.append(node)
            return True
        elif self.tokens[0].token_type == TokenType.SPECIAL_DIV:
            self.match(node)
            parent.children.append(node)
            return True
        return False

    def symbol_factor(self, parent: Node) -> bool:
        # <factor> ::= ( <expression> ) | <var> | <call> | <num>
        node = Node(parent=parent, symbol=ProductionState.FACTOR)
        if self.tokens[0].token_type == TokenType.SPECIAL_PARENTHESIS_OPEN:
            if self.symbol_expression(node):
                if self.tokens[1].token_type == TokenType.SPECIAL_PARENTHESIS_CLOSE:
                    self.match(node)
                    self.match(node)
                    parent.children.append(node)
                    return True
        elif self.symbol_var(node):
            parent.children.append(node)
            return True
        elif self.symbol_call(node):
            parent.children.append(node)
            return True
        elif self.tokens[0].token_type == TokenType.NUMBER:
            self.match(node)
            parent.children.append(node)
            return True
        return False

    def symbol_call(self, parent: Node) -> bool:
        # <call> ::= <id> ( <args> )
        node = Node(parent=parent, symbol=ProductionState.CALL)
        if self.tokens[0].token_type == TokenType.IDENTIFIER:
            if self.tokens[1].token_type == TokenType.SPECIAL_PARENTHESIS_OPEN:
                if self.symbol_args(node):
                    if self.tokens[2].token_type == TokenType.SPECIAL_PARENTHESIS_CLOSE:
                        self.match(node)
                        self.match(node)
                        self.match(node)
                        parent.children.append(node)
                        return True
        return False

    def symbol_args(self, parent: Node) -> bool:
        # <args> ::= <arg-list> | Ɛ
        node = Node(parent=parent, symbol=ProductionState.ARGS)
        self.symbol_arg_list(node)
        parent.children.append(node)
        return True

    def symbol_arg_list(self, parent: Node) -> bool:
        # <arg-list> ::=  <expression> , <arg-list>  | <expression>
        node = Node(parent=parent, symbol=ProductionState.ARG_LIST)
        if self.symbol_expression(node):
            if self.tokens[0].token_type == TokenType.SPECIAL_COMMA:
                if self.arg_list(node):
                    self.match(node)
                    parent.children.append(node)
                    return True
                return False
            parent.children.append(node)
            return True
        return False

    def symbol_identifier(self, parent: Node) -> bool:
        if self.tokens[self.pos].token_type == TokenType.IDENTIFIER:
            node = Node(parent=parent, symbol=None, token=self.tokens[self.pos])
            parent.append(node)
            self.pos += 1
            return True
        return False

    def symbol_number(self, parent: Node) -> bool:
        if self.tokens[self.pos].token_type == TokenType.NUMBER:
            node = Node(parent=parent, symbol=None, token=self.tokens[self.pos])
            parent.append(node)
            self.pos += 1
            return True
        return False

    def symbol_comment(self, parent: Node) -> bool:
        if self.tokens[self.pos].token_type == TokenType.COMMENT:
            node = Node(parent=parent, symbol=None, token=self.tokens[self.pos])
            parent.append(node)
            self.pos += 1
            return True
        return False

    def symbol_add(self, parent: Node) -> bool:
        if self.tokens[self.pos].token_type == TokenType.SPECIAL_ADD:
            node = Node(parent=parent, symbol=None, token=self.tokens[self.pos])
            parent.append(node)
            self.pos += 1
            return True
        return False

    def symbol_sub(self, parent: Node) -> bool:
        if self.tokens[self.pos].token_type == TokenType.SPECIAL_SUB:
            node = Node(parent=parent, symbol=None, token=self.tokens[self.pos])
            parent.append(node)
            self.pos += 1
            return True
        return False

    def symbol_mul(self, parent: Node) -> bool:
        if self.tokens[self.pos].token_type == TokenType.SPECIAL_MUL:
            node = Node(parent=parent, symbol=None, token=self.tokens[self.pos])
            parent.append(node)
            self.pos += 1
            return True
        return False

    def symbol_div(self, parent: Node) -> bool:
        if self.tokens[self.pos].token_type == TokenType.SPECIAL_DIV:
            node = Node(parent=parent, symbol=None, token=self.tokens[self.pos])
            parent.append(node)
            self.pos += 1
            return True
        return False

    def symbol_lt(self, parent: Node) -> bool:
        if self.tokens[self.pos].token_type == TokenType.SPECIAL_LT:
            node = Node(parent=parent, symbol=None, token=self.tokens[self.pos])
            parent.append(node)
            self.pos += 1
            return True
        return False

    def symbol_le(self, parent: Node) -> bool:
        if self.tokens[self.pos].token_type == TokenType.SPECIAL_LE:
            node = Node(parent=parent, symbol=None, token=self.tokens[self.pos])
            parent.append(node)
            self.pos += 1
            return True
        return False

    def symbol_gt(self, parent: Node) -> bool:
        if self.tokens[self.pos].token_type == TokenType.SPECIAL_GT:
            node = Node(parent=parent, symbol=None, token=self.tokens[self.pos])
            parent.append(node)
            self.pos += 1
            return True
        return False

    def symbol_ge(self, parent: Node) -> bool:
        if self.tokens[self.pos].token_type == TokenType.SPECIAL_GE:
            node = Node(parent=parent, symbol=None, token=self.tokens[self.pos])
            parent.append(node)
            self.pos += 1
            return True
        return False

    def symbol_eq(self, parent: Node) -> bool:
        if self.tokens[self.pos].token_type == TokenType.SPECIAL_EQ:
            node = Node(parent=parent, symbol=None, token=self.tokens[self.pos])
            parent.append(node)
            self.pos += 1
            return True
        return False

    def symbol_ne(self, parent: Node) -> bool:
        if self.tokens[self.pos].token_type == TokenType.SPECIAL_NE:
            node = Node(parent=parent, symbol=None, token=self.tokens[self.pos])
            parent.append(node)
            self.pos += 1
            return True
        return False

    def symbol_assign(self, parent: Node) -> bool:
        if self.tokens[self.pos].token_type == TokenType.SPECIAL_ASSIGN:
            node = Node(parent=parent, symbol=None, token=self.tokens[self.pos])
            parent.append(node)
            self.pos += 1
            return True
        return False

    def symbol_semicolon(self, parent: Node) -> bool:
        if self.tokens[self.pos].token_type == TokenType.SPECIAL_SEMICOLON:
            node = Node(parent=parent, symbol=None, token=self.tokens[self.pos])
            parent.append(node)
            self.pos += 1
            return True
        return False

    def symbol_comma(self, parent: Node) -> bool:
        if self.tokens[self.pos].token_type == TokenType.SPECIAL_COMMA:
            node = Node(parent=parent, symbol=None, token=self.tokens[self.pos])
            parent.append(node)
            self.pos += 1
            return True
        return False

    def symbol_parenthesis_open(self, parent: Node) -> bool:
        if self.tokens[self.pos].token_type == TokenType.SPECIAL_PARENTHESIS_OPEN:
            node = Node(parent=parent, symbol=None, token=self.tokens[self.pos])
            parent.append(node)
            self.pos += 1
            return True
        return False

    def symbol_parenthesis_close(self, parent: Node) -> bool:
        if self.tokens[self.pos].token_type == TokenType.SPECIAL_PARENTHESIS_CLOSE:
            node = Node(parent=parent, symbol=None, token=self.tokens[self.pos])
            parent.append(node)
            self.pos += 1
            return True
        return False

    def symbol_bracket_open(self, parent: Node) -> bool:
        if self.tokens[self.pos].token_type == TokenType.SPECIAL_BRACKET_OPEN:
            node = Node(parent=parent, symbol=None, token=self.tokens[self.pos])
            parent.append(node)
            self.pos += 1
            return True
        return False

    def symbol_bracket_close(self, parent: Node) -> bool:
        if self.tokens[self.pos].token_type == TokenType.SPECIAL_BRACKET_CLOSE:
            node = Node(parent=parent, symbol=None, token=self.tokens[self.pos])
            parent.append(node)
            self.pos += 1
            return True
        return False

    def symbol_curly_bracket_open(self, parent: Node) -> bool:
        if self.tokens[self.pos].token_type == TokenType.SPECIAL_CURLY_BRACKET_OPEN:
            node = Node(parent=parent, symbol=None, token=self.tokens[self.pos])
            parent.append(node)
            self.pos += 1
            return True
        return False

    def symbol_curly_bracket_close(self, parent: Node) -> bool:
        if self.tokens[self.pos].token_type == TokenType.SPECIAL_CURLY_BRACKET_CLOSE:
            node = Node(parent=parent, symbol=None, token=self.tokens[self.pos])
            parent.append(node)
            self.pos += 1
            return True
        return False

    def symbol_else(self, parent: Node) -> bool:
        if self.tokens[self.pos].token_type == TokenType.KEYWORD_ELSE:
            node = Node(parent=parent, symbol=None, token=self.tokens[self.pos])
            parent.append(node)
            self.pos += 1
            return True
        return False

    def symbol_if(self, parent: Node) -> bool:
        if self.tokens[self.pos].token_type == TokenType.KEYWORD_IF:
            node = Node(parent=parent, symbol=None, token=self.tokens[self.pos])
            parent.append(node)
            self.pos += 1
            return True
        return False

    def symbol_int(self, parent: Node) -> bool:
        if self.tokens[self.pos].token_type == TokenType.KEYWORD_INT:
            node = Node(parent=parent, symbol=None, token=self.tokens[self.pos])
            parent.append(node)
            self.pos += 1
            return True
        return False

    def symbol_return(self, parent: Node) -> bool:
        if self.tokens[self.pos].token_type == TokenType.KEYWORD_RETURN:
            node = Node(parent=parent, symbol=None, token=self.tokens[self.pos])
            parent.append(node)
            self.pos += 1
            return True
        return False

    def symbol_void(self, parent: Node) -> bool:
        if self.tokens[self.pos].token_type == TokenType.KEYWORD_VOID:
            node = Node(parent=parent, symbol=None, token=self.tokens[self.pos])
            parent.append(node)
            self.pos += 1
            return True
        return False

    def symbol_while(self, parent: Node) -> bool:
        if self.tokens[self.pos].token_type == TokenType.KEYWORD_WHILE:
            node = Node(parent=parent, symbol=None, token=self.tokens[self.pos])
            parent.append(node)
            self.pos += 1
            return True
        return False


if __name__ == "__main__":
    parser = Parser()
