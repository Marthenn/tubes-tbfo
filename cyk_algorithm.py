def getReverse(char):
    if char == ')': return '('
    if char == '}': return '{'


def getWords(str):
    listOw = []
    f_found = False
    found_char = ''
    c_string = ''

    for char in str:
        if (char == '(' or char == '{') and not f_found:
            f_found = True
            found_char = char

        c_string += char

        if (char == ')' or char == '}') and f_found and getReverse(char) == found_char:
            f_found = False
            listOw.append(c_string.strip())
            c_string = ''
            found_char = ''

        if char == ' ' and not f_found and c_string.strip() != '':
            listOw.append(c_string.strip())
            c_string = ''

    if c_string.strip() != '':
        listOw.append(c_string.strip())

    return listOw


CNF = {
    'S': {'IF IF_N_R', 'B B'},
    'IF_N_R': {'EXPR IF_N_R_2'},
    'IF_N_R_2': {'STATEMENTS IF_N_R_3'},
    'IF_N_R_3': {'ELSE_IF IF_N_R_4'},
    'IF_N_R_4': {'EXPR STATEMENTS'},
    'EXPR': {'(2+2 == 4)', '(3+c == 5)', '(3p+5+732)'},
    'STATEMENTS': {'{foo.call()}'},
    'ELSE_IF': {'elif'},
    'IF': {'if', 'if'},
    'A': {'C C', 'A B', 'a'},
    'B': {'B B', 'C A', 'b'},
    'C': {'B A', 'A A', 'b'}
}

cnf_k_list = CNF.keys()
# "if (2+2 == 4) {foo.call()} elif (3+c == 5) {foo.call()}"
list = getWords('if (3p+5+732) {foo.call()} elif (3+c == 5) {foo.call()}')
string = 'aaaaa'
str_n = len(string)
arr_table = [['!' for j in range(str_n - i)] for i in range(str_n)]

# iterate string length 1 to str_n
for i in range(1, str_n + 1):
    # generate strings
    for j in range(0, str_n - i + 1):
        cur_string = string[j:j + i]
        forms = []

        # build possibilities of string
        tup = (cur_string[0:1],) if i == 1 else (cur_string[0:1], cur_string[1:])
        forms.append(tup)

        for k in range(2, i):
            tup = (cur_string[0:k],) if k == i else (cur_string[0:k], cur_string[k:])
            forms.append(tup)

        if i == 1:
            c_char = forms[0][0]
            str_pos = set()

            # check which variable could produce a word
            for el in cnf_k_list:
                if c_char[0] in CNF.get(el):
                    str_pos.add(el)

            if len(str_pos) == 0:
                arr_table[0][j] = str_pos
            else:
                arr_table[0][j] = str_pos

        else:
            r_idx = i - 1
            str_pos = set()

            for fi, form in enumerate(forms):
                # print(form[0])

                first_l = arr_table[len(form[0]) - 1][j]
                # print(len(forms[0][1]) - 1, len(forms[0][0]) - 1, forms)
                second_l = arr_table[len(form[1]) - 1][len(form[0]) + j]
                # print(form, first_l, second_l)

                for f_el in first_l:
                    for s_el in second_l:
                        c_str = f_el + ' ' + s_el
                        # print(c_str)
                        # print(c_str)
                        for el in cnf_k_list:
                            if c_str in CNF.get(el):
                                str_pos.add(el)

                if len(str_pos) == 0:
                    arr_table[r_idx][j] = str_pos
                else:
                    arr_table[r_idx][j] = str_pos

    # print('-------------------------')

print(
    '\n'.join('{}'.format(str(arr_table[k])[1:len(str(arr_table[k])) - 1]) for k in range(len(arr_table) - 1, -1, -1)))

if 'S' in arr_table[len(string) - 1][0]:
    print('string {} could be formed using CNF'.format(' '.join(string)))
else:
    print('string {} could not be formed using CNF'.format(string))

# for i in range(str_n):
#     for j in range(i-1, -1, -1):
#         print('{} '.format(j), end='')
#     print('')
