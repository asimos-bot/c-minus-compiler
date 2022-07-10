from cminus.lex.lex import Lex
from cminus.sintatic.sintatic_tree import Parser

if __name__ == '__main__':
    lex: Lex = Lex()
    tokens = lex.get_tokens_from_file('source_code.txt')
    parser = Parser(list(tokens))
    print(parser.parse())
