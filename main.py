import sys
from cminus.lex.lex import Lex
from cminus.sintatic.parser import Parser
if __name__ == '__main__':
    lex: Lex = Lex()
    tokens = lex.get_tokens_from_file(f'source_code/{sys.argv[1]}.txt')
    list_of_tokens = list(tokens)
    with open(f'output/token_list.txt', 'wt') as file:
        for i, token in enumerate(list_of_tokens):
            file.write(str(i) + " " + str(token))
            file.write("\n")
    parser = Parser(list_of_tokens)
    ast = parser.parse()
    print(ast.subtree_to_str())
    ast.to_dot("output/arvore.dot")
