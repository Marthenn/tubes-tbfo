import time

from convertCNF import fileToCNF, getTerminalSet
from src.evaluator import automata
from src.evaluator import cyk


def parse_fa_cfg(list):
    stn = ''.join(list)

    splitters = ['.', ',', '(', ')', '[', ']']

    for splitter in splitters:
        stn = stn.replace(splitter, ' ' + splitter + ' ')

    sp_list = stn.split(' ')

    terms = {'.', '(', ')', '[', ']'}

    aum = automata.VariableAutomata()
    aus = automata.OperationAutomata()

    for i, el in enumerate(sp_list):
        if el not in terms:
            val_s = aum.evaluate(el)

            if val_s:
                sp_list[i] = 'var_name'
                continue
            print(el)
            val_x = aus.evaluate(el)

            if val_x:
                sp_list[i] = 'expr'

            print(sp_list[i])

    return sp_list


def parse_words(snt):
    special_group = ['//', '{', '}', '(', ')', '+', '-', '*', '%', '!', '<=', '>=', '>', '<', ';',
                     '&&', '||', '==', '=', '\n', '?', '"', "'", '[', ']']

    for special in special_group:
        snt = snt.replace(special, ' ' + special + ' ')

    special_group_multiple = ['=  =', '!  =', '=  =  =', '!  =  =', '>  =', '<  =', '*  *', '>  >  >', '<  <',
                              '>  >', '&  &', '|  |', '+  +', '-  -']

    for special_mltp in special_group_multiple:
        snt = snt.replace(special_mltp, special_mltp.replace(' ', ''))

    snt = snt.split(' ')

    for idx in range(len(snt) - 1, -1, -1):
        if snt[idx] == '':
            snt.pop(idx)

    return snt


def parse_words_from_file(file_path):
    list_of_words = []
    with open(file_path) as lines:
        for line in lines:
            special_group = ['//', '{', '}', '(', ')', '+', '-', '*', '%', '!', '<=', '>=', '>', '<', ';',
                             '&&', '||', '==', '=', '\n', '?', '"', "'", '[', ']']

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
    call_cfg = fileToCNF(
        "/home/zidane/kuliah/Semester 3/IF2124 - Teori Bahasa Formal dan Otomata/tubes-tbfo/automata/fa_res.txt")

    t_setx = getTerminalSet(
        '/home/zidane/kuliah/Semester 3/IF2124 - Teori Bahasa Formal dan Otomata/tubes-tbfo/automata/terminal_no_ops.txt')

    for i, el in enumerate(word_list):

        if el in t_setx:
            found_in = True

        if found_in:
            found_in = False
            __parse_assignable(word_list, i, call_cfg)
            __parse_repeatable(word_list, i, prod)

            continue

        if i + 1 < len(word_list) and (word_list[i + 1] == '=' or word_list[i + 1] == ';' or word_list[i + 1] == '('):
            eval_s = variable_fa.evaluate(el)

            if eval_s:
                word_list[i] = 'var_name'
                continue

        __parse_expr(word_list, i, call_cfg)

    return word_list


def __parse_call(word_list, call_cfg):
    for i, el in enumerate(word_list):
        list_len = len(word_list)

        if '.' in el and el[0] != '.' and el[len(el) - 1] != '.' and not (i + 1 < list_len and word_list[i+1] == '[') :

            if (i + 1 < list_len and word_list[i + 1] != '(') or i + 1 == list_len:

                is_obj_props = cyk.evaluate_cyk(parse_fa_cfg([word_list[i]]), call_cfg, 'FUNCTION_CALL')

                if is_obj_props:
                    word_list[i] = 'func_call'
                continue

            end_idx = i

            while end_idx < list_len and word_list[end_idx] != ')':
                end_idx += 1

            if end_idx == list_len:
                continue

            is_func_call = cyk.evaluate_cyk(parse_fa_cfg(word_list[i:end_idx + 1]), call_cfg, 'FUNCTION_CALL')

            if is_func_call:
                word_list[i:end_idx + 1] = 'func_call'

            continue

        # not function call and not a list access
        if (i + 1 < list_len and word_list[i + 1] != '[') or i + 1 == list_len:
            continue

        # parse for list access
        end_idx = i

        while end_idx < list_len and word_list[end_idx] != ']':
            end_idx += 1

        if end_idx == list_len:
            continue

        is_list_acc = cyk.evaluate_cyk(parse_fa_cfg(word_list[i:end_idx + 1]), call_cfg, 'FUNCTION_CALL')

        if is_list_acc:
            word_list[i:end_idx + 1] = 'func_call'


def __parse_repeatable(word_list, start_idx, prod):
    if word_list[start_idx] != '(':
        return

    repeating = 0
    len_list = len(word_list)

    while start_idx + repeating + 1 < len_list and word_list[start_idx + repeating + 1] == '(':
        repeating += 1

    if repeating == 0:
        return

    end_idx = start_idx + repeating

    while end_idx + 1 < len_list and not (word_list[end_idx] == ')' and word_list[end_idx + 1] != ')'):
        end_idx += 1

    list_fa = parse_with_fa(word_list[start_idx + repeating + 1:end_idx - repeating], prod)
    word_list[start_idx + 1:end_idx] = list_fa


def __parse_assignable(word_list, start_idx, call_cfg):
    if word_list[start_idx] != '=':
        return

    __parse_expr(word_list, start_idx + 1)


def __parse_expr(word_list, start_idx, call_cfg):
    expr_fa = automata.OperationAutomata()
    ternary_fa = automata.TernaryAutomata()
    end_idx = start_idx
    eval_list = []
    list_len = len(word_list)
    literal = ''
    in_literal = False
    ternary = False

    while end_idx < list_len and word_list[end_idx] != ';' and (word_list[end_idx] != ')' or not (
            word_list[end_idx] == ')' and end_idx + 1 < list_len and (
            word_list[end_idx + 1] == '{' or word_list[end_idx + 1] == ';'))):
        word = word_list[end_idx]

        if (word == '"' or word == "'") and in_literal:
            eval_list.append(literal + word)
            literal = ''
            in_literal = False
            end_idx += 1
            continue

        if (word == '"' or word == "'") and not in_literal:
            in_literal = True

        if in_literal:
            literal += word
            end_idx += 1
            continue

        if word == '?':
            ternary = True

        if word_list[end_idx] != '(' and word_list[end_idx] != ')':
            eval_list.append(word_list[end_idx])

        end_idx += 1

    if not end_idx < list_len:
        return

    __parse_call(eval_list, call_cfg)

    eval_s = ternary_fa.evaluate(eval_list) if ternary else expr_fa.evaluate(eval_list)

    if not eval_s:
        return

    word_list[start_idx:end_idx] = ['expr']


prod = {'IF': 'if',
        'ELSE': 'else',
        'KURUNG_BUKA': '(',
        'KURUNG TUTUP': ')',
        'KURUNGC_BUKA': '{',
        'KURUNGC TUTUP': '}',
        'EQUAL': '=',
        'LET': 'let',
        'SEMICOL': ';',
        'RETURN': 'return',
        'NEWLINE': '\n',
        'EXPR': 'expr',
        'FOR': 'for',
        'BREAK': 'break'}

if __name__ == '__main__':
    x = time.time()

    cnf = fileToCNF(
        "/home/zidane/kuliah/Semester 3/IF2124 - Teori Bahasa Formal dan Otomata/tubes-tbfo/automata/res.txt")
    arr_rs = (
        parse_words_from_file('/home/zidane/kuliah/Semester 3/IF2124 - Teori Bahasa Formal dan Otomata/tubes-tbfo/contoh.txt'))
    arr_1 = ['if', '(', 'konts', '+', '3', '===', '9', ')']
    arr_2 = ['x', '=', 'konts', '+', '3', '===', '9', '+', ';']
    arr_3 = ['let', 'x', ';']

    lst = parse_with_fa(arr_rs, prod)

    # print(' '.join(lst))

    for idx in range(len(lst) - 1, -1, -1):
        if lst[idx] == '' or lst[idx] == '\n' or lst[idx] == ';':
            lst.pop(idx)

    print(lst)
    #
    print(cyk.evaluate_cyk(lst, cnf, 'MAIN_STATE'))
    # y = time.time()

    # print(y - x)


def parse_comments(word_list, start_idx):
    # this means the element at start_idx is a comment starter

    # find the comment's last element

    # remove elements from start_idx to end_dx (last comment's element)

    # done!

    if word_list[start_idx] != '//' or word_list[start_idx] != '/*':
        return
    end_idx = start_idx
    if word_list[start_idx] == '//':
        while word_list[end_idx] != '\n':
            end_idx += 1
        while start_idx <= end_idx:
            word_list.pop(start_idx)
            end_idx -= 1
        return

    if word_list[start_idx] == '/*':
        while word_list[end_idx] != '*/':
            end_idx += 1
        while start_idx <= end_idx:
            word_list.pop(start_idx)
            end_idx -= 1
        return
