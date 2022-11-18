 # Convert a text based CFG to an array
def cfgToArray(name):
    file=open(name,'r')
    lines=[line.split() for line in file]
    i=0
    while(i<len(lines)):
        if(lines[i]==[] or lines[i][0]=='/*'):
            temp=lines.pop(i)
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


#Determine whether the symbol is a terminal or a variable
def terminalOrNot(unit):
    if((ord(unit[0])>=65 and ord(unit[0])<=90) or ord(unit[0])==124):
        return False
    return True


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
                    temp=rule.pop(j)
                count-=1
            if(j<len(rule)):
                while(j<len(rule) and rule[j]=='|'):
                    j+=1
            cmp+=1
        prod+=1
    if(rule[len(rule)-1]=='|'):
        temp=rule.pop(len(rule)-1)
    return rule


# Delete a production from a rule
def removeAUnit(rule,idx):
    #print(rule)
    # Cek apakah jumlah production 1
    single=True
    for i in rule:
        if(i=='|'):
            single=False
            break
    if(single):
        while(idx<len(rule)):
            temp=rule.pop(idx)
    else:
        if(idx!=len(rule)-1):
            while(rule[idx]!='|'):
                temp=rule.pop(idx)
            temp=rule.pop(idx)
        else:
            idx-=1
            while(idx<len(rule)):
                temp=rule.pop(idx)
    #print(rule)


# Remove empty rules
def removeEmpty(cfg):
    i=0
    while(i<len(cfg)):
        if(len(cfg[i])==2):
            temp=cfg.pop(i)
        else:
            i+=1
    return cfg


# Remove useless Pipes
def removeUselessPipes(rule):
    
    # Remove pipe at the beginning
    while(rule[2]=='|'):
        temp=rule.pop(2)

    # Remove pipe at the end
    while(rule[len(rule)-1]=='|'):
        temp=rule.pop(len(rule)-1)
    
    # Remove duplicate pipes
    pipe=False
    i=2
    while(i<len(rule)):
        if(pipe and rule[i]=='|'):
            temp=rule.pop(i)
        elif(rule[i]=='|'):
            pipe=True
            i+=1
        else:
            pipe=False
            i+=1

    return rule

# Check if an epsilon still exist in the CFG
def epsilonExist(cfg):
    for rule in cfg:
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
                if(rule[i]=='EPSILON'):
                    exist=True
                    break
                i+=1
            if(exist):
                epsilons.append(rule[0])
        # print("EPSILONS")
        # print(epsilons)

        #remove epsilon from all production
        for rule in cfg:
            i=2
            while(i<len(rule)):
                if(rule[i]=='EPSILON'):
                    removeAUnit(rule,i)
                else:
                    i+=1
        cfg=removeEmpty(cfg)

        for rule in cfg:
            i=2
            start=2
            while(i<len(rule)):
                for epsilon in epsilons:
                    if(rule[i]==epsilon):
                        # Check if the replaced unit is single or not
                        if(i==start and (i==len(rule)-1 or (i+1<len(rule) and rule[i+1]=='|'))):
                            # print("went in again")
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
                        break
                i+=1
                if(i<len(rule) and rule[i]=='|'):
                    i+=1
                    start=i
            rule=removeUselessPipes(rule)
            rule=deleteDuplicates(rule)
    return cfg

# Eliminating single unit productions
def unitElimination(cfg):
    for line in cfg:
        i=2
        start=i
        prod=[]
        # count=0
        while(i<len(line)):
            if(line[i]!='|'):
                prod.append(line[i])
            i+=1
            if((i<len(line) and line[i]=='|') or i==len(line)):
                if(len(prod)==1 and not(terminalOrNot(prod[0]))):
                    # print(temp)
                    replacement=searchForProd(cfg,prod[0])
                    # print(replacement)
                    if(replacement!=None):
                        temp=line.pop(start)
                        line.append('|')
                        for re in replacement:
                            line.append(re)
                    else:
                        i+=1
                    # if(count<3):
                    #     print(i)
                    #     print(prod)
                    #     print(replacement)
                    #     print(line)
                    #     count+=1
                else:
                    i+=1
                start=i
                prod=[]
        line=deleteDuplicates(line)
        line=removeUselessPipes(line)
    return cfg
        

# Eliminating useless variables
def uselessElimination(cfg):
    # Check if the variable exist in any RHS
    i=0
    useless=[]
    while(i<len(cfg)):
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
        temp=cfg.pop(delete-minus)
        minus+=1
    # print("FIRST ELIMINATION")
    # displayCFG(cfg)
    
    #Check if a variable exist in any LHS
    useless=[]
    exist=True
    for rule in cfg:
        i=2
        # print("current rule")
        # print(rule)
        while(i<len(rule)):
            # print("current rule i")
            # print(rule[i])
            if(rule[i]=='|'):
                i+=1
            for rule2 in cfg:
                if(rule[i]!='|' and not(terminalOrNot(rule[i])) and rule[i]==rule2[0]):
                    exist=True
                    # print("rule i wnt in")
                    # print(rule[i])
                    break
                else:
                    exist=False
            if(not(exist) and not(terminalOrNot(rule[i]))):
                useless.append(rule[i])
            i+=1
    # print("useless")
    # print(useless)
 
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
                        temp=rule.pop(start-minus)
                        i-=1 
                    divider.append(i)
                start=i+1
                exist=False
            i+=1
        minus=0
        # print("THIS IS THE RULE")
        # print(rule)
        # print("THIS IS DIVIDER")
        # print(divider)
        for divide in divider:
            temp=rule.pop(divide-minus)
            minus+=1
    
    #check for unused '|' at the end
    for rule in cfg:
        last=len(rule)-1
        if(rule[last]=='|'):
            temp=rule.pop(last)
    cfg=removeEmpty(cfg)
    print("SECOND ELIMINATION")
    displayCFG(cfg)
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
    for unit in prod:
        if(terminalOrNot(unit)):
            return True
    return False

def ruleExist(cfg,rule):
    for lines in cfg:
        if(lines[0]==rule[0]):
            return True
    return False

def productionExist(rule,prod):
    i=2
    current=[]
    while(i<len(rule)):
        if(rule[i]!='|'):
            current.append(rule[i])
        i+=1
        if((i<len(rule) and rule[i]=='|') or i==len(rule)):
            if(current==prod):
                return True
            i+=1
            current=[]
    return False

def convertToCNF(cfg):
    # Create new start variable
    CNF=[['START', '->']]
    CNF[0].append(cfg[0][0])
    for rules in cfg:
        CNF.append(rules)
    
    # Get terminals
    terminal=[]
    for rules in cfg:
        for prod in rules:
            if(terminalOrNot(prod) and prod!='|'):
                i=0
                exist=False
                while(i<len(terminal)):
                    if(terminal[i]==prod):
                        exist=True
                        break
                if(not(exist)):
                    terminal.append(prod)
    
    # Create new terminal productions
    for prod in terminal:
        new=[]
        new.append(prod.upper()+'__')
        new.append('->')
        new.append(prod)
        cfg.append(new)

    print("Sebelum diganti")
    print(cfg)
    for rules in cfg:
        i=2
        prod=[]
        start=i
        while(i<len(rules)):
            if(rules[i]!='|'):
                prod.append(rules[i])
            i+=1
            # print(prod)
            # Change any terminal that's not a single terminal to a variable
            if((i<len(rules) and rules[i]=='|') or i==len(rules)):
                if(terminalExist(prod) and len(prod)>=2):
                    j=start
                    while(j<i):
                        if(terminalOrNot(rules[j])):
                            rules[j]=rules[j].upper()+'__'
                        j+=1
            
                # Change any productions that has a length of 3 or more
                if(len(prod)>2):
                    # Create new rule
                    j=start
                    change=[]
                    while(j<i-2):
                        temp=rules.pop(j)
                        change.append(temp)
                        i-=1
                    change.append(rules[j])
                    print("CHANGE")
                    print(change)
                    str=''
                    for unit in change:
                        str+=unit+'__'
                    new=[str,'->']
                    for unit in change:
                        new.append(unit)

                    # Check if the rule already exists
                    if(not(ruleExist(cfg,new))):
                        cfg.append(new)
                        # Check if the same rule also has the same production
                        # for line in cfg:
                        #     if(line[0]==str): 
                        #         if(not(productionExist(line,change))):
                    rules[j]=str
                i+=1
                start=i
                prod=[]
    return cfg
    displayCFG(cfg)

        

def displayCFG(cfg):
    for rules in cfg:
        i=0
        while(i<len(rules)):
            print(rules[i], end="")
            if(i!=len(rules)):
                print(" ",end="")
            i+=1
        print("\n")

    

def writeToFile(file,cfg):
    for lines in cfg:
        i=0
        while(i<len(lines)):
            file.write(lines[i])
            if(i!=len(lines)-1):
                file.write(" ")
            i+=1
        file.write("\n")


cfg=cfgToArray('test.txt')
# displayCFG(cfg)


#removeEmpty(cfg)
#removeAUnit(cfg[2],2)
# print("EPISOL ELIM")
# cfg=epsilonElimination(cfg)
# displayCFG(cfg)

# print("UNIT REPLACE")
# cfg=unitElimination(cfg)
# displayCFG(cfg)
cfg=uselessElimination(cfg)
# displayCFG(cfg)

#print(cfg)

                