

def evaluate_cyk(code_arr, cnf):
    cnf_k_list = cnf.keys()
    code_len = len(code_arr)
    arr_table = [['!' for _ in range(code_len - i)] for i in range(code_len)]

    # iterate string length 1 to code_len
    for i in range(1, code_len + 1):
        # generate strings
        for j in range(0, code_len - i + 1):
            cur_string = code_arr[j:j + i]
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
                    if c_char[0] in cnf.get(el):
                        str_pos.add(el)

                if len(str_pos) == 0:
                    arr_table[0][j] = str_pos

                else:
                    arr_table[0][j] = str_pos

            else:
                r_idx = i - 1
                str_pos = set()

                for fi, form in enumerate(forms):

                    first_l = arr_table[len(form[0]) - 1][j]
                    second_l = arr_table[len(form[1]) - 1][len(form[0]) + j]

                    for f_el in first_l:
                        for s_el in second_l:
                            c_str = f_el + ' ' + s_el

                            for el in cnf_k_list:
                                if c_str in cnf.get(el):
                                    str_pos.add(el)

                    if len(str_pos) == 0:
                        arr_table[r_idx][j] = str_pos
                    else:
                        arr_table[r_idx][j] = str_pos

    return True if 'S' in arr_table[len(list) - 1][0] else False


