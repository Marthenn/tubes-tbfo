from abc import abstractmethod, ABC
import string


class Automata:
    states = []
    alphabets = set()
    start_state = ""
    accept_states = []
    transition = {}

    @abstractmethod
    def evaluate(self, string):
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
        last_char = ''

        for char in variable_name:
            last_char = char
            input_c = 'IN' if char in nums else 'NIN'

            if char not in allowed:
                input_c = 'NA'

            transition_tuple = (current_state, input_c)
            current_state = self.transition.get(transition_tuple)

            if current_state is None:
                break

        res = False

        if current_state in self.accept_states:
            res = True

        return res, last_char


class OperationAutomata:

    def __init__(self):
        self.states = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11']
        self.alphabets = ['F_CALL', 'VAR', 'NUM', 'LLS', 'URY_PRE', 'URY_POST', 'COMP_OPS', 'BIN_OPS']
        self.start_state = self.states[0]
        self.accept_states = ['S2', 'S6', 'S7', 'S8', 'S9', 'S4']
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
                           ('S7', 'BIN_OPS_PRE'): 'S3',
                           ('S1', 'URY_PRE'): 'S10',
                           ('S1', 'BIN_URY_PRE'): 'S10',
                           ('S10', 'F_CALL') : 'S8',
                           ('S10', 'VAR'): 'S8',
                           ('S10', 'NUM'): 'S8',
                           ('S10', 'LLS'): 'S8',
                           ('S1', 'URY_POST_PRE_NU'): 'S11',
                           ('S11', 'VAR'): 'S8',
                           ('S1', 'LLS'): 'S9',
                           ('S9', 'BIN_OPS'): 'S3',
                           ('S9', 'BIN_URY_PRE'): 'S3',
                           ('S9', 'COMP_OPS'): 'S3',
                           ('S3', 'NUM'): 'S4',
                           ('S3', 'VAR'): 'S4',
                           ('S3', 'F_CALL'): 'S4',
                           ('S3', 'LLS'): 'S4',
                           ('S4', 'COMP_OPS'): 'S1',
                           ('S4', 'BIN_OPS'): 'S1',
                           ('S4', 'URY_POST_PRE_NU'): 'S1'}
        self.operators = {'COMP_OPS': {'==', '!=', '===', '!==', '>', '>=', '<', '<='},  # comparison operators
                          'BIN_OPS': {'*', '/', '%', '**', '&', '|', '^', '<<', '>>', '>>>', '&&', '||'},
                          # binary operators
                          'URY_POST_PRE_NU': {'++', '--'},  # unary post fix operators
                          'BIN_URY_PRE': {'+', '-'},
                          'URY_PRE': {'~', '!'}}  # unary pre fix operators
        self.var_checker = VariableAutomata()

    def evaluate(self, expression_list):
        # assignment shud be handled by the cfg
        current_state = self.start_state
        input_s = None

        for i, el in enumerate(expression_list):
            input_s = self.__get_input(el)

            if input_s is None:

                if '.' not in el or el[0] == '.' or el[len(el)-1] == '.':
                    input_s = 'NA'
                elif expression_list[i+1] == '(' and expression_list[i+2] == ')':
                    input_s = 'F_CALL'
                    expression_list.pop(i+1)
                    expression_list.pop(i+1)
                else:
                    input_s = 'VAR'

            transition_tuple = (current_state, input_s)
            print(current_state, input_s)
            current_state = self.transition.get(transition_tuple)

            if current_state is None:
                break

        res = False

        if current_state in self.accept_states:
            res = True

        return res

    def __get_input(self, el):
        input_s = None

        if self.var_checker.evaluate(el)[0]:
            input_s = 'VAR'
        elif (el[0] == "'" and el[len(el) - 1] == "'") or (el[0] == '"' and el[len(el) - 1] == '"'):
            input_s = 'LLS'
        else:
            try:
                int(el)
                input_s = 'NUM'
            except ValueError:
                keys = self.operators.keys()

                for key in keys:
                    if el in self.operators.get(key):
                        input_s = key
                        break

        return input_s


evaluator_exp = OperationAutomata()
expresyen = 'fUNc.call ( )'
print(expresyen)
print(evaluator_exp.evaluate(expresyen.split(' ')))
