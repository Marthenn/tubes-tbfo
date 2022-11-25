import os

from src.grammar.convertCNF import fileToCNF, getTerminalSet
from src.evaluator import automata
from src.evaluator import cyk


def parse_comments(word_list, start_idx):
    # this means the element at start_idx is a comment starter

    # find the comment's last element

    # remove elements from start_idx to end_dx (last comment's element)

    # done!

    if word_list[start_idx] != '//' and word_list[start_idx] != '/*':
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


def parse_fa_cfg(list_r):
    stn = ''.join(list_r)

    splitters = ['.', ',', '(', ')', '[', ']']

    for splitter in splitters:
        stn = stn.replace(splitter, ' ' + splitter + ' ')

    sp_list = stn.split(' ')

    terms = {'.', '(', ')', '[', ']', 'var_name', 'expr'}

    aum = automata.VariableAutomata()
    aus = automata.OperationAutomata()

    for i, el in enumerate(sp_list):
        if el not in terms:
            val_s = aum.evaluate(el)

            if val_s:
                sp_list[i] = 'var_name'
                continue

            parse = parse_words(sp_list[i])

            for j, elp in enumerate(parse):
                if elp == '"':
                    end_idx = j + 1
                    while end_idx < len(parse) and parse[end_idx] != "'":
                        end_idx += 1

                    if end_idx >= len(parse):
                        continue

                    parse[j:end_idx + 1] = [''.join(parse[j:end_idx + 1])]
                elif elp == "'":

                    end_idx = j + 1
                    while end_idx < len(parse) and parse[end_idx] != "'":
                        end_idx += 1

                    if end_idx >= len(parse):
                        continue

                    parse[j:end_idx + 1] = [''.join(parse[j:end_idx + 1])]

            val_x = aus.evaluate(parse)

            if val_x:
                sp_list[i] = 'expr'
                continue

    for idx in range(len(sp_list) - 1, -1, -1):
        parse_comments(sp_list, idx)
        if sp_list[idx] == '':
            sp_list.pop(idx)

    return sp_list


def parse_words(snt):
    special_group = ['//', '{', '}', '(', ')', '+', '-', '*', '/', '%', '!', '<=', '>=', '>', '<', ';',
                     '&&', '||', '==', '=', '\n', '?', '"', "'", '[', ']', ':', ',']

    for special in special_group:
        snt = snt.replace(special, ' ' + special + ' ')

    special_group_multiple = ['=  =  =', '=  =', '!  =', '!  =  =', '>  =', '<  =', '*  *', '>  >  >', '<  <',
                              '>  >', '&  &', '|  |', '+  +', '-  -', '/  /', '*  /', '/  *']

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
            line = parse_words(line)

            list_of_words.extend(line)

    return list_of_words


def parse_with_fa(word_list):
    in_ops, found_in = False, False
    variable_fa = automata.VariableAutomata()
    call_cfg = fileToCNF(
        "automata/terminal_cnf.txt")

    t_setx = getTerminalSet(
        'automata/terminal_no_ops.txt')

    __parse_call(word_list, call_cfg, t_setx)

    for i, el in enumerate(word_list):
        parse_comments(word_list, i)

        if el in t_setx:
            found_in = True

        if found_in:
            found_in = False

            __parse_assignable(word_list, i)
            __parse_repeatable(word_list, i)

            continue

        op_set = {'==', '!=', '===', '!==', '>', '>=', '<', '<=', '*', '/', '%', '**', '&', '|', '^', '<<', '>>', '>>>',
                  '&&', '||', '++', '--', '+', '-', "'", '"'}

        is_num = True
        asnmt = False

        try:
            int(el)
        except ValueError:
            is_num = False

        for plus in range(5):
            if i + plus >= len(word_list):
                break

            if '=' in word_list[i + plus] and word_list[i + plus] not in op_set:
                asnmt = True
                break

        if el in op_set or (i + 1 < len(word_list) and word_list[i + 1] in op_set and not asnmt) or is_num:

            __parse_expr(word_list, i, False)

        else:

            eval_s = variable_fa.evaluate(el)

            if eval_s:
                word_list[i] = 'var_name'

    return word_list


def __parse_call(word_list, call_cfg, t_set):
    ex_set = {';', '{', '(', 'return'}
    for i, el in enumerate(word_list):
        list_len = len(word_list)

        if el in t_set:
            continue

        if i + 1 < list_len and word_list[i + 1] == '(' and not (i - 1 >= 0 and (word_list[i] in t_set or
                                                                                 (word_list[i - 1] in t_set and
                                                                                  word_list[i - 1] not in ex_set))):
            end_idx = i
            while end_idx < list_len and word_list[end_idx] != ')':
                end_idx += 1

            if end_idx == list_len:
                continue

            if word_list[i] == 'document.getElementById':
                print(word_list[i:end_idx], 'HAHAYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY')

            is_func_call = cyk.evaluate_cyk(parse_fa_cfg(word_list[i:end_idx + 1]), call_cfg, 'FUNCTION_CALL')

            if is_func_call:
                word_list[i:end_idx + 1] = ['func_call']

            continue

        if i + 1 < list_len and word_list[i + 1] == '[':
            end_idx = i

            while end_idx < list_len and word_list[end_idx] != ']':
                end_idx += 1

            if end_idx == list_len:
                continue

            parsed = parse_fa_cfg(word_list[i:end_idx + 1])

            is_list_acc = cyk.evaluate_cyk(parsed, call_cfg, 'FUNCTION_CALL')

            if is_list_acc:
                word_list[i:end_idx + 1] = ['func_call']

            continue

        if '.' in el and el[0] != '.' and el[len(el) - 1] != '.':

            is_obj_props = cyk.evaluate_cyk(parse_fa_cfg([word_list[i]]), call_cfg, 'FUNCTION_CALL')

            if is_obj_props:
                word_list[i] = 'func_call'

            continue


def __parse_repeatable(word_list, start_idx):
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

    list_fa = parse_with_fa(word_list[start_idx + repeating + 1:end_idx - repeating])
    word_list[start_idx + 1:end_idx] = list_fa


def __parse_assignable(word_list, start_idx):
    if word_list[start_idx] != '=':
        return

    __parse_expr(word_list, start_idx + 1, True)


def __parse_expr(word_list, start_idx, asn):
    expr_fa = automata.OperationAutomata()
    ternary_fa = automata.TernaryAutomata()
    end_idx = start_idx
    eval_list = []
    list_len = len(word_list)
    literal = ''
    in_literal = False
    ternary = False

    t_set = getTerminalSet(
        'automata/terminal_no_ops.txt')
    rb_ex = {'{', ';'}

    if asn:
        while end_idx < list_len and word_list[end_idx] != ';':

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

    else:
        while end_idx < list_len and ((word_list[end_idx] not in t_set) or word_list[end_idx] == '(' or (word_list[end_idx] == ':' and ternary) or (
                word_list[end_idx] == ')' and end_idx + 1 < list_len and word_list[end_idx + 1] not in rb_ex)):

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

    cnf = fileToCNF("D:/Kuliah/Semester 3/TBFO/tubes-tbfo/automata/result.txt")
    arr_rs = (parse_words_from_file("D:/Kuliah/Semester 3/TBFO/tubes-tbfo/test/test6.js"))

    lst = parse_with_fa(arr_rs)

    for idx in range(len(lst) - 1, -1, -1):
        if lst[idx] == '' or lst[idx] == ';':
            lst.pop(idx)

    print(' '.join(lst))

    for idx in range(len(lst) - 1, -1, -1):
        if lst[idx] == '' or lst[idx] == '\n' or lst[idx] == ';':
            lst.pop(idx)

    print(cyk.evaluate_cyk(lst, cnf, 'MAIN_STATE'))