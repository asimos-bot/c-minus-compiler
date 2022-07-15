from cminus.lex.lex import Lex
from cminus.sintatic.parser import Parser
if __name__ == '__main__':
    lex: Lex = Lex()
    tokens = lex.get_tokens_from_file('source_code.txt')
    list_of_tokens = list(tokens)
    with open('token_list.txt', 'wt') as file:
        for i, token in enumerate(list_of_tokens):
            file.write(str(i) + " " + str(token))
            file.write("\n")
    parser = Parser(list_of_tokens)
    ast = parser.parse()
    print(ast.subtree_to_str())
    ast.to_dot("arvore.dot")
