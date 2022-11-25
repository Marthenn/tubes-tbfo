from src.evaluator import automata
from src.evaluator import cyk
from src.evaluator import *
from src.evaluator.parser import *
from src.grammar.convertCNF import *
import sys,os

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python src/main.py <js_file_path>")
        sys.exit(1)
    cfg=cfgToArray('automata/cfg.txt')
    cfg=epsilonElimination(cfg)
    cfg=unitElimination(cfg)
    cfg=uselessElimination(cfg)
    cfg=convertToCNF(cfg)
    writeToFile("automata/cnf.txt",cfg)
    cnf = fileToCNF("automata/cnf.txt")
    arr_rs = (parse_words_from_file(sys.argv[1]))

    lst = parse_with_fa(arr_rs)

    for idx in range(len(lst) - 1, -1, -1):
        if lst[idx] == '' or lst[idx] == ';':
            lst.pop(idx)

    #print(' '.join(lst))

    for idx in range(len(lst) - 1, -1, -1):
        if lst[idx] == '' or lst[idx] == '\n' or lst[idx] == ';':
            lst.pop(idx)

    if cyk.evaluate_cyk(lst, cnf, 'MAIN_STATE'):
        print("Accepted")
    else:
        print("Syntax Error")