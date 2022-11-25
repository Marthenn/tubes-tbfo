from abc import abstractmethod, ABC
import string


class Automata:
    states = []
    alphabets = set()
    start_state = ""
    accept_states = []
    transition = {}

    @abstractmethod
    def evaluate(self, evaluation_object):
        pass


class VariableAutomata(Automata, ABC):

    def __init__(self):
        self.states = ['S1', 'S2']
        self.alphabets = ['NIN', 'IN', 'NA']
        self.start_state = self.states[0]
        self.accept_states = [self.states[1]]
        self.transition = {(self.states[0], self.alphabets[0]): self.states[1],
                           (self.states[1], self.alphabets[0]): self.states[1],
                           (self.states[1], self.alphabets[1]): self.states[1]}

    def evaluate(self, variable_name):
        current_state = self.start_state

        allowed = set(string.ascii_letters)
        allowed.update(['{}'.format(i) for i in range(0, 10)])
        allowed.update(['_', '$'])

        # generate list of alphabets (lower and upper case)
        nums = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}

        for char in variable_name:
            fa_input = 'IN' if char in nums else 'NIN'

            if char not in allowed:
                fa_input = 'NA'

            transition_tuple = (current_state, fa_input)
            current_state = self.transition.get(transition_tuple)

            if current_state is None:
                break

        res = False

        if current_state in self.accept_states:
            res = True

        return res


# unfortunately we made the dfa without ternary in consideration, so rather than reconstructing the correct dfa,
# we decided (not happily) to create another evaluator function for ternary operations
class TernaryAutomata(Automata, ABC):

    def __init__(self):
        self.states = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6']
        self.alphabets = ['?', ':', 'VALID']
        self.start_state = self.states[0]
        self.accept_states = ['S6']
        self.transition = {('S1', 'VALID'): 'S2',
                           ('S2', '?'): 'S3',
                           ('S3', 'VALID'): 'S4',
                           ('S4', ':'): 'S5',
                           ('S5', 'VALID'): 'S6',
                           ('S6', '?'): 'S3'}
        self.expr_checker = OperationAutomata()

    def evaluate(self, expression_list):
        ter_ops = {'?', ':'}
        current_state = self.start_state

        for i, el in enumerate(expression_list):

            if el in ter_ops:
                fa_input = el
            else:
                eval_s = self.__evaluate_exp(expression_list, i)

                fa_input = 'VALID' if eval_s else 'INVALID'

            transition_tuple = (current_state, fa_input)

            current_state = self.transition.get(transition_tuple)

            if current_state is None:
                return False

        return True

    def __evaluate_exp(self, expression_list, start_idx):
        end_idx = start_idx

        list_len = len(expression_list)

        # fishy, check
        while end_idx < (list_len - 1) and expression_list[end_idx] != '?' and expression_list[end_idx] != ':' \
                and expression_list[end_idx] != ')' and expression_list[end_idx] != ';':
            end_idx += 1

        if not end_idx < list_len:
            return False

        end_idx = end_idx + 1 if end_idx == start_idx else end_idx

        eval_s = self.expr_checker.evaluate(expression_list[start_idx:end_idx])

        if eval_s:
            expression_list[start_idx:end_idx] = ['expr']

        return eval_s


class OperationAutomata(Automata, ABC):

    def __init__(self):
        self.states = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11']
        self.alphabets = ['F_CALL', 'VAR', 'NUM', 'LLS', 'URY_PRE', 'URY_POST', 'COMP_OPS', 'BIN_OPS']
        self.start_state = self.states[0]
        self.accept_states = ['S2', 'S6', 'S7', 'S8', 'S9', 'S4', 'S5']
        self.transition = {('S1', 'VAR'): 'S2',
                           ('S2', 'BIN_OPS'): 'S3',
                           ('S2', 'BIN_URY_PRE'): 'S3',
                           ('S2', 'COMP_OPS'): 'S3',
                           ('S2', 'URY_POST_PRE_NU'): 'S8',
                           ('S1', 'NUM'): 'S6',
                           ('S6', 'BIN_OPS'): 'S3',
                           ('S6', 'BIN_URY_PRE'): 'S3',
                           ('S6', 'COMP_OPS'): 'S3',
                           ('S1', 'F_CALL'): 'S7',
                           ('S7', 'COMP_OPS'): 'S3',
                           ('S7', 'BIN_OPS'): 'S3',
                           ('S7', 'BIN_URY_PRE'): 'S3',
                           ('S1', 'URY_PRE'): 'S10',
                           ('S1', 'BIN_URY_PRE'): 'S10',
                           ('S10', 'F_CALL'): 'S8',
                           ('S10', 'VAR'): 'S8',
                           ('S10', 'NUM'): 'S8',
                           ('S10', 'LLS'): 'S8',
                           ('S1', 'URY_POST_PRE_NU'): 'S11',
                           ('S11', 'VAR'): 'S8',
                           ('S8', 'COMP_OPS'): 'S3',
                           ('S8', 'BIN_OPS'): 'S3',
                           ('S8', 'BIN_URY_PRE'): 'S3',
                           ('S1', 'LLS'): 'S9',
                           ('S9', 'BIN_OPS'): 'S3',
                           ('S9', 'BIN_URY_PRE'): 'S3',
                           ('S9', 'COMP_OPS'): 'S3',
                           ('S3', 'NUM'): 'S4',
                           ('S3', 'VAR'): 'S5',
                           ('S3', 'F_CALL'): 'S4',
                           ('S3', 'URY_PRE'): 'S3',
                           ('S3', 'URY_POST_PRE_NU'): 'S3',
                           ('S3', 'LLS'): 'S4',
                           ('S4', 'COMP_OPS'): 'S1',
                           ('S4', 'BIN_OPS'): 'S1',
                           # ('S4', 'URY_POST_PRE_NU'): 'S1',
                           ('S4', 'BIN_URY_PRE'): 'S1',
                           ('S5', 'URY_POST_PRE_NU'): 'S5',
                           ('S5', 'COMP_OPS'): 'S1',
                           ('S5', 'BIN_OPS'): 'S1',
                           # ('S5', 'URY_POST_PRE_NU'): 'S1',
                           ('S5', 'BIN_URY_PRE'): 'S1'}
        self.operators = {'COMP_OPS': {'==', '!=', '===', '!==', '>', '>=', '<', '<='},  # comparison operators
                          'BIN_OPS': {'*', '/', '%', '**', '&', '|', '^', '<<', '>>', '>>>', '&&', '||'},
                          # binary operators
                          'URY_POST_PRE_NU': {'++', '--'},  # unary post fix operators
                          'BIN_URY_PRE': {'+', '-'},
                          'URY_PRE': {'~', '!'}}  # unary pre fix operators
        self.var_checker = VariableAutomata()

    # this function assumes that expression_list is already free of ( or ) or any other symbols such that
    # the expression is not regular when they r members of the list
    def evaluate(self, expression_list):
        # assignment shud be handled by the cfg
        current_state = self.start_state
        fa_input = None

        for i, el in enumerate(expression_list):
            fa_input = self.__get_input(expression_list[i])

            transition_tuple = (current_state, fa_input)
            current_state = self.transition.get(transition_tuple)

            if current_state is None:
                break

        res = False

        if current_state in self.accept_states:
            res = True

        return res

    def __get_input(self, el):
        fa_input = None

        # check for func call
        if el == 'func_call':
            return 'F_CALL'

        if self.var_checker.evaluate(el):
            fa_input = 'VAR'
        elif (el[0] == "'" and el[len(el) - 1] == "'") or (el[0] == '"' and el[len(el) - 1] == '"'):
            fa_input = 'LLS'
        else:
            try:
                int(el)
                fa_input = 'NUM'
            except ValueError:
                keys = self.operators.keys()

                for key in keys:
                    if el in self.operators.get(key):
                        fa_input = key
                        break

        return fa_input


if __name__ == '__main__':
    evaluator_exp = OperationAutomata()
    evaluator_var = VariableAutomata()
    evaluator_ternary = TernaryAutomata()
    expresyen = '++ x'.split(' ')
    ls = 'func_call + func_call'
    print(evaluator_exp.evaluate(expresyen))