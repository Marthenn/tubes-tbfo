import automata

def parse_words(file_path):
    list_of_words = []
    with open(file_path) as lines:
        for line in lines:
            special_group = ['//', '{', '}', '(', ')', '+', '-', '*', '%', '!', '<=', '>=', '>', '<', ';',
                             '&&', '||', '==', '=', '\n', '?']

            for special in special_group:
                line = line.replace(special, ' ' + special + ' ')

            special_group_multiple = ['=  =', '!  =', '=  =  =', '!  =  =', '>  =', '<  =', '*  *', '>  >  >', '<  <',
                                      '>  >', '&  &', '|  |', '+  +', '-  -']

            for special_mltp in special_group_multiple:
                line = line.replace(special_mltp, special_mltp.replace(' ', ''))

            line = line.split(' ')

            for idx in range(len(line) - 1, -1, -1):
                if line[idx] == '':
                    line.pop(idx)

            list_of_words.extend(line)

    return list_of_words


def parse_with_fa(word_list, prod):
    in_ops, found_in = False, False
    prod_key = prod.keys()
    variable_fa = automata.VariableAutomata()

    for i, el in enumerate(word_list):

        for key in prod_key:
            if el in prod.get(key):
                found_in = True
                break

        if found_in:
            found_in = False
            continue

        if i + 1 < len(word_list) and (word_list[i+1] == '=' or word_list[i+1] == ';'):
            eval_s = variable_fa.evaluate(el)

            if eval_s:
                word_list[i] = 'var_name'

            continue

        parse_expr(word_list, i)

    return word_list


def parse_expr(word_list, start_idx):
    expr_fa = automata.OperationAutomata()
    ternary_fa = automata.TernaryAutomata()
    end_idx = start_idx
    list_len = len(word_list)
    ternary = False

    while end_idx < list_len and word_list[end_idx] != ';' and word_list[end_idx] != ')':
        if word_list[end_idx] == '?':
            ternary = True

        end_idx += 1

    if not end_idx < list_len:
        return

    eval_s = ternary_fa.evaluate(word_list[start_idx:end_idx]) if ternary else expr_fa.evaluate(word_list[start_idx:end_idx])

    if not eval_s:
        return

    repl_string = 'ternary' if ternary else 'expr'
    word_list[start_idx:end_idx] = [repl_string]


prod = {'IF': 'if',
        'ELSE': 'else',
        'KURUNG_BUKA': '(',
        'KURUNG TUTUP': ')',
        'KURUNGC_BUKA': '{',
        'KURUNGC TUTUP': '}',
        'EQUAL': '=',
        'LET': 'let'}

arr_rs = (parse_words('test.txt'))
#print(arr_rs)
arr_1 = ['if', '(', 'konts', '+', '3', '===', '9', ')']
arr_2 = ['x', '=', 'konts', '+', '3', '===', '9', '+', ';']
arr_3 = ['let', 'x', ';']
print(' '.join(parse_with_fa(arr_3, prod)))

def parse_comments(word_list, start_idx):
    # this means the element at start_idx is a comment starter

    # find the comment's last element

    # remove elements from start_idx to end_dx (last comment's element)

    # done!
    
    if word_list[start_idx] != '//' or word_list[start_idx] != '/*':
        return

    if word_list[start_idx] == '//':
        while word_list[start_idx] != '\n':
            word_list.pop(start_idx)
        word_list.pop(start_idx)
        return

    if word_list[start_idx] == '/*':
        while word_list[start_idx] != '*/':
            word_list.pop(start_idx)
        word_list.pop(start_idx)
        return