from cminus.lex.lex import Lex

if __name__ == '__main__':
    lex : Lex = Lex()
    with open('token_list.txt', 'w') as f:
        for token in lex.get_tokens_from_file('source_code.txt'):
            f.write(f'{token}\n')
