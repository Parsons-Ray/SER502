from classes import *
import re

#Globals
#highlevel code looks like:
    #integer a, b := 10, c:=20.
global current_scope
current_scope = "GLBL"
tokens = Iterator(["SDKSTRT", "STRT", "TYP", "INT", "b", "STRTEX", "PUSH", "50", "EQL", "b", "ENDEX", "FUN", "sampleFunction", "INT", "PAR", "INT", "param1", "PAR", "INT", "param2", "STRT", "TYP", "INT", "a", "STRTEX", "PUSH", "b", "EQL", "a", "ENDEX", "FUNEND", "CALL", "sampleFunction", "PAR", "30", "PAR", "20", "SDKEND"])
labelPat = r'\.LABEL[0-9]*'
whenEndPat = r'\.WLEND[0-9]*'
# curr_labeltokens = Iterator([".LABEL1", "TYP", "INT", "res", "res", "EQL", "10","EOL", "PUSH", "res", "PUSH", "1", "ADD", "EOL" , "LEND1"])
# loop_labeltokens = Iterator(["SDKSTRT","TYP", "INT", "a", "PUSH", "a", "PUSH", "10", "EQL", "TYP", "INT", "b", "PUSH", "b", "Push", "15", "EQL", ".LABEL2", "LOOP", "STRTEX", "PUSH", "a", "PUSH", "b", "LT", "ENDEX", "CMP", "PUSH", "a", "PUSH", "a", "ADD", "EQL", "JMP", "LABEL2", "LEND2", "SDKEND"])
# tokens = Iterator(["SDKSTRT","TYP", "INT", "a", "STRTEX", "PUSH", "10", "EQL", "a", "ENDEX", "TYP", "INT", "b", "STRTEX", "PUSH", "15", "EQL", "b","ENDEX", ".LABEL2", "LOOP", "STRTEX", "PUSH", "a", "PUSH", "b", "LT", "ENDEX", "CMP", "STRTEX", "PUSH", "a", "PUSH", "1", "ADD", "EQL", "a", "ENDEX", "JMP", "LABEL2", "LOOPLEND2", "SDKEND"])
# runTokens = Iterator(["SDKSTRT","TYP", "INT", "a", "STRTEX", "PUSH", "a", "PUSH", "10", "EQL", "ENDEX", "TYP", "INT", "b", "STRTEX", "PUSH", "b", "PUSH", "15", "EQL", "ENDEX", "LOOP", ".LABEL2", "STRTEX", "PUSH", "a", "PUSH", "b", "LT", "ENDEX", "CMP", "PUSH", "a", "PUSH", "a", "ADD", "EQL", "WHEN", "STRTEX", "PUSH", "a" , "PUSH", "12", "LT", "JEQ", "LABEL2", "WHEN",".LABEL3", "TYP", "INT", "a", "PUSH", "13", "EQL", "a", "WLEND3", "JMP", "LABEL2", "LOOPLEND2", "SDKEND"])
# runTokens = Iterator(["SDKSTRT","TYP", "INT", "a", "STRTEX", "PUSH", "10", "EQL", "a", "ENDEX", "TYP", "INT", "b", "STRTEX", "PUSH", "15", "EQL", "b","ENDEX", ".LABEL2", "LOOP", "STRTEX", "PUSH", "a", "PUSH", "b", "LT", "ENDEX", "CMP", "STRTEX", "PUSH", "a", "PUSH", "1", "ADD", "EQL", "a", "ENDEX","JMP", "LABEL2", "LOOPLEND2", "SDKEND"])

#tokens = Iterator(["SDKSTRT","WHEN","STRTEX", "PUSH" , "1", "PUSH", "1", "EEQL","ENDEX", "JEQ", "LABEL0", ".LABEL0", "TYP", "INT", "a", "STRTEX", "PUSH", "10", "EQL", "a", "ENDEX", "TYP", "INT", "b", "STRTEX", "PUSH", "15", "EQL", "b","ENDEX", "WHEN", "STRTEX", "PUSH", "a", "PUSH", "b", "LT", "ENDEX", "JEQ", "LABEL1", ".LABEL1", "TYP", "INT", "a", "STRTEX", "PUSH", "10", "EQL", "a", "ENDEX",  "PRNT", "STRTPRNT", "STRTEX", "PUSH", "a", "PUSH", "b", "ADD", "ENDEX", "ENDPRNT", "LEND1", "STRTEX", "PUSH", "a", "PUSH", "b", "GT", "JEQ", "LABEL2", ".LABEL2", "TYP", "INT", "a", "STRTEX", "PUSH", "11", "EQL", "a", "ENDEX", "LEND2", "ENDW", "TYP", "INT", "REZ", "PUSH", "REZ", "EQL", "1", "LEND0", "ENDW", "SDKEND"])
runTokens = Iterator(["SDKSTRT", "WHEN", "STRTEX", "PUSH" , "1", "PUSH", "1", "EEQL","ENDEX", "JEQ", "LABEL0", ".LABEL0", "TYP", "INT", "a", "STRTEX", "PUSH", "10", "EQL", "a", "ENDEX", "TYP", "INT", "b", "STRTEX", "PUSH", "15", "EQL", "b","ENDEX", "WHEN", "STRTEX", "PUSH", "a", "PUSH", "b", "LT", "ENDEX", "JEQ", "LABEL1", ".LABEL1", "TYP", "INT", "a", "STRTEX", "PUSH", "10", "EQL", "a", "ENDEX", "PRNT", "STRTPRNT", "STRTEX", "PUSH", "a", "PUSH", "b", "ADD", "ENDEX", "ENDPRNT", "LEND1", "STRTEX", "PUSH", "a", "PUSH", "b", "GT", "JEQ", "LABEL2", ".LABEL2", "TYP", "INT", "a", "STRTEX", "PUSH", "11", "EQL", "a", "ENDEX", "LEND2", "ENDW", "TYP", "INT", "REZ", "PUSH", "REZ", "EQL", "1", "LEND0", "ENDW", "SDKEND"])
global glbl_sym_table
glbl_sym_table = SymbolTable('GLBL', None)
symtab_add(glbl_sym_table)
stack = Stack()

def TYP():
    tokens.next() #this should pop off "TYP"
    varType = tokens.next() #pushes "INT, FLT, BOOL" onto stack
    varID = tokens.next() #variable identifier ("a", "b", "c")
    var = Variable(varID, None, varType)
    dict_of_symbolTabs[current_scope].add(varID, var)


def FUN():
    tokens.next()#pop FUN
    name = tokens.next() #name of function
    currentFunction = Function(tokens.next(), name) #return type
    while (tokens.next() is "PAR"):
        currentFunction.addParam(tokens.next(), tokens.next())
    currentFunction.startPC = tokens.counter
    dict_of_functions[name] = currentFunction
    while tokens.current() is not "FUNEND":
        print(tokens.next())
    tokens.next()#pop End

def CALL():
    tokens.next() #pop CALL
    currentFunction = dict_of_functions[tokens.next()]#functions should only be declared in global
    while tokens.next() is "PAR": #add all parameters
        nextValue = tokens.next()

        try:
            if dict_of_symbolTabs[current_scope].lookup(nextValue) is not None:
                nextValue = dict_of_symbolTabs[current_scope].lookup(nextValue).getValue()
        except ValueError:
            print("value Not Found")

        currentFunction.setParamValues(nextValue)
    currentFunction.returnPC(tokens.getCounter()-1)#set return PC
    print("returnPC: {0}".format(tokens.getCounter()))

    name = currentFunction.getName()
    counter = 0
    while (name + str(counter)) in dict_of_symbolTabs:
        counter += 1

    global current_scope
    symbTable = SymbolTable(name, current_scope)
    for key in currentFunction.getParams():
        symbTable.add(key, currentFunction.getParams()[key])

    dict_of_symbolTabs[name + str(counter)] = symbTable
    current_scope = name + str(counter) #set current_scope to the name of the function + number
    stack.push(currentFunction)
    tokens.setCounter(currentFunction.getStartPC())

def RTRN():
    tokens.next() #pop RTRN
    exitedFun = stack.pop() #pop the function from the stack
    stack.push(tokens.next()) #push the returned value
    tokens.setcounter(exitedFun.getReturnPC())

def LABL_TRACK():
    while runTokens.current() is not "SDKEND":
        label = runTokens.current()
        if re.match(labelPat, label):
            global current_scope
            print "Current Scope: " + current_scope
            current_label = Label(runTokens.current().replace(".", ""), runTokens.getCounter()+1, current_scope)
            # ltermnum = label[:-1]
            current_scope = label.replace(".", "")
        runTokens.next()
    current_scope = 'GLBL'


def STARTEX():
    while tokens.current() is not "ENDEX":
        nextToken = tokens.next()
        if nextToken == "PUSH":
            varName = tokens.next()
            if re.match(r'[+-]?(\d+(\.\d*)?|\.\d+)', varName):
                stack.push(eval(varName))
            else:
                try:
                    stack.push(dict_of_symbolTabs[current_scope].lookup(varName).getValue())

                except:
                    print("Symbol not found")

        elif nextToken == "ADD":
            result = stack.pop() + stack.pop()
            stack.push(result)
        elif nextToken == "SUB":
            first = stack.pop()
            result = stack.pop() - first
            stack.push(result)
        elif nextToken == "MUL":
            result = stack.pop() * stack.pop()
            stack.push(result)
        elif nextToken == "DIV":
            first = stack.pop()
            result = stack.pop() / first
            stack.push(result)
        elif nextToken == "GT":
            top = stack.pop()
            if stack.pop() > top:
                stack.push(1)
            else:
                stack.push(0)
        elif nextToken == "LT":
            top = stack.pop()
            if stack.pop() < top:
                stack.push(1)
            else:
                stack.push(0)
        elif nextToken == "GE":
            top = stack.pop()
            if stack.pop() >= top:
                stack.push(1)
            else:
                stack.push(0)
        elif nextToken == "LE":
            top = stack.pop()
            if stack.pop() <= top:
                stack.push(1)
            else:
                stack.push(0)
        elif nextToken == "EEQL":
            if stack.pop() == stack.pop():
                stack.push(1)
            else:
                stack.push(0)
        elif nextToken == "NEQL":
            if stack.pop() != stack.pop():
                stack.push(1)
            else:
                stack.push(0)
        elif nextToken == "NOT":
            if stack.pop() >= 1:
                stack.push(0)
            else:
                stack.push(1)
        elif nextToken == "EQL":
            try:
                print current_scope
                varObj = dict_of_symbolTabs[current_scope].lookup(tokens.next())
                varObj.setValue(stack.pop())
            except ValueError:
                print("Identifier not found")
        elif nextToken == "AND":
            if stack.pop() and stack.pop():
                stack.push(1)
            else:
                stack.push(0)
        elif nextToken == "OR":
            if stack.pop() or stack.pop():
                stack.push(1)
            else:
                stack.push(0)
    tokens.next()

def FUNEND():
    finishedFunction = stack.pop()
    print("here: {0}".format(finishedFunction.getRetrunPC()))
    tokens.setCounter(finishedFunction.getRetrunPC())
    print dict_of_symbolTabs

def LABL():
    lname = tokens.current().replace(".", "")
    global current_scope
    current_scope = lname
    tokens.next()

def CMP():
    if stack.pop() >= 1:
        tokens.next()
    else:
        while tokens.current() is not "LOOPLEND"+str(current_scope[-1:]):
            tokens.next()
def JMP():
    tokens.next()
    label = tokens.next()
    global current_scope
    current_scope = label
    tokens.setCounter(dict_of_labels[label].getStart())

def JEQ():
    if stack.pop() >= 1:
        tokens.next()
        global current_scope
        current_scope = tokens.next()
        tokens.setCounter(dict_of_labels.get(current_scope).getStart())
    else:
        tokens.next()
        current_scope = tokens.current()
        num = current_scope[-1:]
        while tokens.current() != "LEND"+str(num) :
            tokens.next()
        current_scope = dict_of_symbolTabs[current_scope].getScope()[0]

def WLEND():
    while tokens.current() is not "ENDW":
        tokens.next()
    global current_scope
    current_scope = dict_of_symbolTabs.get(current_scope).getScope()[0]

def LOOPLEND():
    global current_scope
    current_scope = dict_of_symbolTabs[current_scope].getScope()[0]
    tokens.next()

def PRNT():
    expression = stack.pop()
    print expression
    tokens.next()

def main():
    LABL_TRACK()
    while tokens.current() is not "SDKEND":
        nextToken = tokens.current()
        print(nextToken)
        if nextToken is "TYP":
            TYP()
        elif nextToken is "FUN":
            FUN()
        elif nextToken is "CALL":
            CALL()
        elif nextToken is "RTRN":
            RTRN()
        elif nextToken is "STRTEX":
            STARTEX()
        elif nextToken is "FUNEND":
            FUNEND()
        elif re.match(labelPat, nextToken):
            LABL()
        elif nextToken is "CMP":
            CMP()
        elif nextToken is "JMP":
            JMP()
        elif nextToken is "JEQ":
            JEQ()
        # elif nextToken is "JNEQ":
        #     JNEQ()
        elif nextToken is "LEND"+current_scope[-1:]:
            WLEND()
        elif nextToken is "LOOPLEND"+current_scope[-1:]:
            LOOPLEND()
        elif nextToken == "ENDPRNT":
            PRNT()
        else:
            tokens.next()

    #LABL(curr_labeltokens.current())
#Call the main method. Starts runtime.
main()
