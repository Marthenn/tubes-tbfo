# Get terminals from a text file
def getTerminal(name):
    terminals = []
    file=open(name,'r')
    lines = file.readlines()
    for line in lines:
        terminals.append(line.replace('\n',''))
    file.close()
    return terminals

def getTerminalSet(name):
    return set(getTerminal(name))   

 # Convert a text based CFG to an array
def cfgToArray(name):
    file=open(name,'r')
    lines=[line.split() for line in file]
    i=0
    while(i<len(lines)):
        if(lines[i]==[] or lines[i][0]=='/*'):
            lines.pop(i)
        else:
            i+=1
    file.close()
    return lines

# Search for a spesific variable production
def searchForProd(cfg, prod):
    for rule in cfg:
        if(rule[0]==prod):
            searched=[]
            i=2
            while(i<len(rule)):
                searched.append(rule[i])
                i+=1
            return searched

def searchForTermRule(cfg,term):
    for rules in cfg:
        if len(rules) == 3:
            if rules[2] == term:
                return rules[0]
    
#Determine whether the symbol is a terminal or a variable
def terminalOrNot(unit):
    terminals=getTerminal('automata/terminals.txt')
    for terminal in terminals:
        if terminal == unit:
            return True
    return False


# Delete production duplicates in a rule
def deleteDuplicates(rule):
    count=1
    for divide in rule:
        if(divide=='|'):
            count+=1
    prod=1
    i=2
    while(prod<=count):
        while(i<len(rule) and rule[i]=='|'):
            i+=1
        current=[]
        while(i<len(rule) and rule[i]!='|'):
            current.append(rule[i])
            i+=1
        cmp=prod+1
        i+=1
        j=i
        while(j<len(rule) and rule[j]=='|'):
            j+=1
        while(cmp<=count):
            compare=[]
            while(j<len(rule) and rule[j]!='|'):
                compare.append(rule[j])
                j+=1
            if(current==compare):
                j-=len(compare)
                for delete in compare:
                    rule.pop(j)
                count-=1
            if(j<len(rule)):
                while(j<len(rule) and rule[j]=='|'):
                    j+=1
            cmp+=1
        prod+=1
    if(rule[len(rule)-1]=='|'):
        rule.pop(len(rule)-1)
    return rule


# Delete a production from a rule
def removeAUnit(rule,idx):
    # Cek apakah jumlah production 1
    single=True
    for i in rule:
        if(i=='|'):
            single=False
            break
    if(single):
        while(idx<len(rule)):
            rule.pop(idx)
    else:
        if(idx!=len(rule)-1):
            while(rule[idx]!='|'):
                rule.pop(idx)
            rule.pop(idx)
        else:
            idx-=1
            while(idx<len(rule)):
                rule.pop(idx)


# Remove empty rules
def removeEmpty(cfg):
    i=0
    while(i<len(cfg)):
        if(len(cfg[i])==2):
            cfg.pop(i)
        else:
            i+=1
    return cfg


# Remove useless Pipes
def removeUselessPipes(rule):
    
    # Remove pipe at the beginning
    i=2 
    while rule[0] != 'OR' and (rule[i] == ' ' or rule[i] == '|'):
        while rule[i] == ' ':
            i += 1
        if rule[i] == '|':
            rule.pop(i)

    # Remove pipe at the end
    while(rule[len(rule)-1]=='|' or rule[len(rule)-1]==' '):
        rule.pop(len(rule)-1)
    
    # Remove duplicate pipes
    i=2
    # print(rule)
    while(i<len(rule)):
        if rule[i] == '|':
            i += 1
            
            while rule[i] == '|':
                rule.pop(i)
        else:
            i+=1
    return rule

# Check if an epsilon still exist in the CFG
def epsilonExist(cfg):
    for rule in cfg:
        if(rule[0]!='EPSILON'):
            for prod in rule:
                if(prod=='EPSILON'):
                    return True
    return False

# Eliminating epsilon production
def epsilonElimination(cfg):
    while(epsilonExist(cfg)):
        epsilons=[]
        for rule in cfg:
            i=2
            exist=False
            while(i<len(rule)):
                if(rule[i]=='|'):
                    i+=1
                if(i < len(rule) and rule[i]=='EPSILON'):
                    exist=True
                    break
                i+=1
            if(exist):
                epsilons.append(rule[0])

        #remove epsilon from all production
        for rule in cfg:
            i=2
            while(i<len(rule)):
                if(rule[i]=='EPSILON'):
                    removeAUnit(rule,i)
                else:
                    i+=1
            rule=removeUselessPipes(rule)
        cfg=removeEmpty(cfg)

        for rule in cfg:
            i=2
            start=2
            while(i<len(rule)):
                for epsilon in epsilons:
                    flag=False
                    if(rule[i]==epsilon):
                        # Check if the replaced unit is single or not
                        if(i==start and (i+1==len(rule) or rule[i+1]=='|') and epsilon!=rule[0]):
                            j=start
                            rule.append('|')
                            rule.append('EPSILON')
                        else:
                            rule.append('|')
                            j=start
                            while(rule[j]!='|'):
                                if(j!=i):
                                    rule.append(rule[j])
                                j+=1
                i+=1
                if(i<len(rule) and rule[i]=='|'):
                    i+=1
                    start=i
                    
            rule=removeUselessPipes(rule)
            rule=deleteDuplicates(rule)
    for rule in cfg:
        rule=removeUselessPipes(rule)
    return cfg

# Eliminating single unit productions
def unitElimination(cfg):
    for line in cfg:
        
        i=2
        start=i
        prod=[]
        count=0
        while(i<len(line)):
            if(line[i]!='|'):
                prod.append(line[i])
            i+=1
            if((i<len(line) and line[i]=='|') or i==len(line)):
                if(len(prod)==1 and not(terminalOrNot(prod[0]))):
                    replacement=searchForProd(cfg,prod[0])
                    if(replacement!=None):
                        line.append('|')
                        for re in replacement:
                            line.append(re)
                        line.pop(start)
                    else:
                        i+=1
                else:
                    i+=1
                start=i
                prod=[]
            line=deleteDuplicates(line)
            count+=1
        line=deleteDuplicates(line)
        line=removeUselessPipes(line)
    return cfg
        

# Eliminating useless variables
def uselessElimination(cfg):
    # Check if the variable exist in any RHS
    i=1
    useless=[]
    while(i<len(cfg)):
        if not(len(cfg[i]) == 3 and terminalOrNot(cfg[i][2])):
            exist=False
            cmp=cfg[i][0]
            j=0
            while(j<len(cfg)):
                if(j!=i):
                    k=2
                    while(k<len(cfg[j])):
                        if(cmp==cfg[j][k]):
                            exist=True
                            break
                        k+=1
                if(exist):
                    break
                j+=1
            if(not(exist)):
                useless.append(i)
        i+=1
    minus=0
    for delete in useless:
        cfg.pop(delete-minus)
        minus+=1
    
    #Check if a variable exist in any LHS
    useless=[]
    exist=True
    for rule in cfg:
        i=2
        while(i<len(rule)):
            if(rule[i]=='|'):
                i+=1
            for rule2 in cfg:
                if(rule[i]!='|' and not(terminalOrNot(rule[i])) and rule[i]==rule2[0]):
                    exist=True
                    break
                else:
                    exist=False
            if(not(exist) and not(terminalOrNot(rule[i]))):
                useless.append(rule[i])
            i+=1
 
    useless=list(set(useless))
    for rule in cfg:
        exist=False
        i=2
        start=i
        divider=[]
        while(i<len(rule)):
            j=0
            while(j<len(useless)):
                if(rule[i]==useless[j]):
                    exist=True
                    break
                j+=1
            
            if(i+1>=len(rule) or rule[i]=='|'):
                if(exist):
                    minus=0
                    while(start<i):
                        rule.pop(start-minus)
                        i-=1 
                    divider.append(i)
                start=i+1
                exist=False
            i+=1
        minus=0
        for divide in divider:
            rule.pop(divide-minus)
            minus+=1
    
    #check for unused '|' at the end
    for rule in cfg:
        last=len(rule)-1
        if(rule[last]=='|'):
            rule.pop(last)
    cfg=removeEmpty(cfg)
    return cfg


# Count the amount of terminal in a production
def countTerminal(prod):
    count=0
    for i in prod:
        if(terminalOrNot(i)):
            count+=1
    return count


# Count the amount of nonterminal in a production
def countNonTerminal(prod):
    count=0
    for i in prod:
        if(not(terminalOrNot(i))):
            count+=1
    return count


# Determine whether if the CFG abides the CNF criteria
def isCNF(cfg):
    cnf=True
    for rule in cfg:
        prod=[]
        i=2
        while(i<len(rule)):
            if(rule[i]!='|'):
                prod.append(rule[i])
            else:
                if(not(countTerminal(prod)==1 and len(prod)==1) or not(countNonTerminal(prod)!=2 and len(rule)==2)):
                    cnf=False
                    return cnf
                prod=[]
            i+=1
    return cnf

def terminalExist(prod):
    idx=[]
    count=0
    exist = False
    for unit in prod:
        if(terminalOrNot(unit)):
            exist = True
            idx.append(count)
        count += 1
    return exist,idx

def ruleExist(cfg,rule):
    for lines in cfg:
        if(len(lines)-2==len(rule)):
            i=0
            flag=True
            while(i<len(rule)):
                if(lines[i+2]!=rule[i]):
                    flag=False
                    break
                i+=1
            if(flag):
                return True, lines[0]
    return False, None

def CreateRule(cfg,prod,num):
    new=[]
    stri = 'T'+str(num)
    new.append(stri)
    new.append('->')
    for unit in prod:
        new.append(unit)
    cfg.append(new)
    return stri

def convertToCNF(cfg):
    num = 1
    for rules in cfg:
        i=2
        prod=[]
        start=i
        while i < len(rules):
            if rules[i] != '|':
                prod.append(rules[i])
            i += 1
            if i >= len(rules) or rules[i] == '|':
                
                # Check if there are no-term combined with term
                exist,idx=terminalExist(prod)
                if exist and len(prod) > 1:
                        for id in idx:
                            var = searchForTermRule(cfg,prod[id])
                            prod[id] = var
                            rules[start + id] = var

                # Change prod with length of 3 or more
                if len(prod) > 2:
                    new=[]
                    id = 0
                    while id < len(prod)-1:
                        new.append(prod[id])
                        id += 1
                    
                    exist,var = ruleExist(cfg,new)
                    if not(exist):
                        var = CreateRule(cfg,new,num)
                        num += 1
                    trav = start
                    while trav < i-2:
                        rules.pop(trav)
                        i -= 1
                    rules[trav] = var
                start = i + 1
                prod = []
                i += 1
    return cfg

def writeToFile(file,cfg):
    file=open(file,"w")
    for lines in cfg:
        i=0
        while(i<len(lines)):
            file.write(lines[i])
            if(i!=len(lines)-1):
                file.write(" ")
            i+=1
        file.write("\n")

def fileToCNF(file):
    file=open(file,'r')
    lines = file.readlines()
    file.close()
    cnf = {}
    for line in lines:
        line = line.strip()
        line = line.split()
        prod = set()
        production = ''
        for i in range(2,len(line)):
            if(line[i]!='|'):
                if(production!=''):
                    production+=' '
                production += line[i]
            else:
                prod.add(production)
                production = ''
        prod.add(production)
        cnf[line[0]] = prod
    return cnf  