from cminus.lex.lex import Lex
from cminus.sintatic.sintatic_tree import Parser
if __name__ == '__main__':
    lex: Lex = Lex()
    tokens = lex.get_tokens_from_file('source_code.txt')
    list_of_tokens = list(tokens)
    parser = Parser(list_of_tokens)
    print(parser.parse())
