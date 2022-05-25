from cminus.lex.lex import Lex

if __name__ == '__main__':
    # while_table = {
    #     1: { "w": 2 },
    #     2: {"h": 3},
    #     3: {"i": 4},
    #     4: {"l": 5},
    #     5: {"e": 6},
    #     6: FINAL
    # }
    lex : Lex = Lex()
    with open('token_list.txt', 'w') as f:
        for token in lex.get_tokens_from_file('source_code.txt'):
            f.write(f'{token}\n')