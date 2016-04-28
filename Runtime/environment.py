from classes import *
import re
import copy

#Globals
#highlevel code looks like:
    #integer a, b := 10, c:=20.
global current_scope
current_scope = "GLBL"

# - - - - - - - - - - - - - - - - - - -Kevin - - - - - - - - - - - - - - - - - - - - - -
# tokens = Iterator(["SDKSTRT",
# "STRT", "TYP","INT", "b",
# "STRTEX", "PUSH", "50", "EQL", "b", "ENDEX",
# "FUN", "sampleFunction", "INT", "PAR", "INT", "param1", "PAR", "INT", "param2",
#         "STRT", "TYP", "INT", "a",
#         "STRTEX", "PUSH", "param1", "PUSH", "1", "ADD","EQL", "a", "ENDEX",
# #        "CALL", "sampleFunction", "PAR", "a", "PAR", "20",
#         "RTRN", "a",
# "FUNEND",
#  "STRTEX", "CALL", "sampleFunction","PAR", "10", "PAR", "20", "EQL","b", "ENDEX", "SDKEND"])

#- - - - - - - - - - - - - - - - - - - -Shashank- - - - - - - - - - -  - -- - - - - - - - -
labelPat = r'\.LABEL[0-9]*'
whenEndPat = r'\.WLEND[0-9]*'
lendPat = r'LEND[0-9]*'
# curr_labeltokens = Iterator([".LABEL1", "TYP", "INT", "res", "res", "EQL", "10","EOL", "PUSH", "res", "PUSH", "1", "ADD", "EOL" , "LEND1"])
# loop_labeltokens = Iterator(["SDKSTRT","TYP", "INT", "a", "PUSH", "a", "PUSH", "10", "EQL", "TYP", "INT", "b", "PUSH", "b", "Push", "15", "EQL", ".LABEL2", "LOOP", "STRTEX", "PUSH", "a", "PUSH", "b", "LT", "ENDEX", "CMP", "PUSH", "a", "PUSH", "a", "ADD", "EQL", "JMP", "LABEL2", "LEND2", "SDKEND"])
# tokens = Iterator(["SDKSTRT","TYP", "INT", "a", "STRTEX", "PUSH", "10", "EQL", "a", "ENDEX", "TYP", "INT", "b", "STRTEX", "PUSH", "15", "EQL", "b","ENDEX", ".LABEL2", "LOOP", "STRTEX", "PUSH", "a", "PUSH", "b", "LT", "ENDEX", "CMP", "STRTEX", "PUSH", "a", "PUSH", "1", "ADD", "EQL", "a", "ENDEX", "JMP", "LABEL2", "LOOPLEND2", "SDKEND"])
# runTokens = Iterator(["SDKSTRT","TYP", "INT", "a", "STRTEX", "PUSH", "a", "PUSH", "10", "EQL", "ENDEX", "TYP", "INT", "b", "STRTEX", "PUSH", "b", "PUSH", "15", "EQL", "ENDEX", "LOOP", ".LABEL2", "STRTEX", "PUSH", "a", "PUSH", "b", "LT", "ENDEX", "CMP", "PUSH", "a", "PUSH", "a", "ADD", "EQL", "WHEN", "STRTEX", "PUSH", "a" , "PUSH", "12", "LT", "JEQ", "LABEL2", "WHEN",".LABEL3", "TYP", "INT", "a", "PUSH", "13", "EQL", "a", "LEND3", "JMP", "LABEL2", "LOOPLEND2", "SDKEND"])
# runTokens = Iterator(["SDKSTRT","TYP", "INT", "a", "STRTEX", "PUSH", "10", "EQL", "a", "ENDEX", "TYP", "INT", "b", "STRTEX", "PUSH", "15", "EQL", "b","ENDEX", ".LABEL2", "LOOP", "STRTEX", "PUSH", "a", "PUSH", "b", "LT", "ENDEX", "CMP", "STRTEX", "PUSH", "a", "PUSH", "1", "ADD", "EQL", "a", "ENDEX","JMP", "LABEL2", "LOOPLEND2", "SDKEND"])

# tokens = Iterator(["SDKSTRT", "TYP", "INT", "a", "STRTEX", "PUSH", "0", "EQL", "a", "ENDEX", "TYP", "INT", "counter", "STRTEX", "PUSH", "0", "EQL", "counter", "ENDEX",".LABEL1", "STRTEX", "PUSH", "a", "PUSH", "5", "LT","ENDEX", "CMP", "LOOP", "STRTEX", "PUSH", "counter", "PUSH", "1", "ADD", "ENDEX", "WHEN", "STRTEX", "PUSH", "a" , "PUSH", "2", "EEQL", "ENDEX", "JEQ", "LABEL2", ".LABEL2","STRTPRNT", "STRTEXT", "PUSH", "a", "PUSH", "29", "ADD", "ENDEX", "ENDPRNT", "LEND2", "ENDW","STRTEX", "PUSH", "a", "PUSH", "1", "ADD", "EQL", "a", "ENDEX", "JMP", "LABEL1" , "LEND1", "LOOPLEND1", "SDKEND"])
# runTokens = Iterator(["SDKSTRT", "TYP", "INT", "a", "STRTEX", "PUSH", "0", "EQL", "a", "ENDEX", "TYP", "INT", "counter", "STRTEX", "PUSH", "0", "EQL", "counter", "ENDEX",".LABEL1", "STRTEX", "PUSH", "a", "PUSH", "5", "LT","ENDEX", "CMP", "LOOP", "STRTEX", "PUSH", "counter", "PUSH", "1", "ADD", "ENDEX", "WHEN", "STRTEX", "PUSH", "a" , "PUSH", "2", "EEQL", "ENDEX", "JEQ", "LABEL2", ".LABEL2","STRTPRNT", "STRTEXT", "PUSH", "a", "PUSH", "29", "ADD", "ENDEX", "ENDPRNT", "LEND2", "ENDW", "STRTEX", "PUSH", "a", "PUSH", "1", "ADD", "EQL", "a", "ENDEX", "JMP", "LABEL1" , "LEND1", "LOOPLEND1", "SDKEND"])
# tokens = Iterator(["SDKSTRT","WHEN","STRTEX", "PUSH" , "1", "PUSH", "1", "EEQL","ENDEX", "JEQ", "LABEL0", ".LABEL0", "TYP", "INT", "a", "STRTEX", "PUSH", "10", "EQL", "a", "ENDEX", "TYP", "INT", "b", "STRTEX", "PUSH", "15", "EQL", "b","ENDEX", "WHEN", "STRTEX", "PUSH", "a", "PUSH", "b", "GT", "ENDEX", "JEQ", "LABEL1", ".LABEL1", "TYP", "INT", "a", "STRTEX", "PUSH", "10", "EQL", "a", "ENDEX",  "PRNT", "STRTPRNT", "STRTEX", "PUSH", "a", "PUSH", "b", "ADD", "ENDEX", "ENDPRNT", "LEND1", "STRTEX", "PUSH", "a", "PUSH", "b", "LT", "ENDEX", "JEQ", "LABEL2", ".LABEL2", "TYP", "INT", "a", "STRTEX", "PUSH", "11", "EQL", "a", "ENDEX", "LEND2", ".LABEL3", "TYP", "INT", "z", "STRTEX", "PUSH", "120", "EQL", "z", "ENDEX", "LEND3", "ENDW", "TYP", "INT", "REZ", "PUSH", "REZ", "EQL", "1", "LEND0", "ENDW", "TYP", "BOOL", "vboo", "STRTEX", "PUSH", "1", "EQL", "vboo", "ENDEX", "ENDEX", "TYP", "FLT", "vfl", "STRTEX", "PUSH", "10.23", "EQL", "vfl", "ENDEX", "SDKEND"])
# runTokens = Iterator(["SDKSTRT", "WHEN", "STRTEX", "PUSH" , "1", "PUSH", "1", "EEQL","ENDEX", "JEQ", "LABEL0", ".LABEL0", "TYP", "INT", "a", "STRTEX", "PUSH", "10", "EQL", "a", "ENDEX", "TYP", "INT", "b", "STRTEX", "PUSH", "15", "EQL", "b","ENDEX", "WHEN", "STRTEX", "PUSH", "a", "PUSH", "b", "GT", "ENDEX", "JEQ", "LABEL1", ".LABEL1", "TYP", "INT", "a", "STRTEX", "PUSH", "10", "EQL", "a", "ENDEX", "PRNT", "STRTPRNT", "STRTEX", "PUSH", "a", "PUSH", "b", "ADD", "ENDEX", "ENDPRNT", "LEND1", "STRTEX", "PUSH", "a", "PUSH", "b", "LT", "ENDEX", "JEQ", "LABEL2", ".LABEL2", "TYP", "INT", "a", "STRTEX", "PUSH", "11", "EQL", "a", "ENDEX", "LEND2", ".LABEL3", "TYP", "INT", "z", "STRTEX", "PUSH", "120", "EQL", "z", "ENDEX", "LEND3", "ENDW", "TYP", "INT", "REZ", "PUSH", "REZ", "EQL", "1", "LEND0", "ENDW", "TYP", "BOOL", "vboo", "STRTEX", "PUSH", "1", "EQL", "vboo", "ENDEX", "ENDEX", "TYP", "FLT", "vfl", "STRTEX", "PUSH", "10.23", "EQL", "vfl", "ENDEX", "ENDEX", "SDKEND"])


#tokens = Iterator(["SDKSTRT","WHEN","STRTEX", "PUSH" , "1", "PUSH", "1", "EEQL","ENDEX", "JEQ", "LABEL0", ".LABEL0", "TYP", "INT", "a", "STRTEX", "PUSH", "10", "EQL", "a", "ENDEX", "TYP", "INT", "b", "STRTEX", "PUSH", "15", "EQL", "b","ENDEX", "WHEN", "STRTEX", "PUSH", "a", "PUSH", "b", "LT", "ENDEX", "JEQ", "LABEL1", ".LABEL1", "TYP", "INT", "a", "STRTEX", "PUSH", "10", "EQL", "a", "ENDEX",  "PRNT", "STRTPRNT", "STRTEX", "PUSH", "a", "PUSH", "b", "ADD", "ENDEX", "ENDPRNT", "LEND1", "STRTEX", "PUSH", "a", "PUSH", "b", "GT", "JEQ", "LABEL2", ".LABEL2", "TYP", "INT", "a", "STRTEX", "PUSH", "11", "EQL", "a", "ENDEX", "LEND2", "ENDW", "TYP", "INT", "REZ", "PUSH", "REZ", "EQL", "1", "LEND0", "ENDW", "SDKEND"])
# runTokens = Iterator(["SDKSTRT", "WHEN", "STRTEX", "PUSH" , "1", "PUSH", "1", "EEQL","ENDEX", "JEQ", "LABEL0", ".LABEL0", "TYP", "INT", "a", "STRTEX", "PUSH", "10", "EQL", "a", "ENDEX", "TYP", "INT", "b", "STRTEX", "PUSH", "15", "EQL", "b","ENDEX", "WHEN", "STRTEX", "PUSH", "a", "PUSH", "b", "LT", "ENDEX", "JEQ", "LABEL1", ".LABEL1", "TYP", "INT", "a", "STRTEX", "PUSH", "10", "EQL", "a", "ENDEX", "PRNT", "STRTPRNT", "STRTEX", "PUSH", "a", "PUSH", "b", "ADD", "ENDEX", "ENDPRNT", "LEND1", "STRTEX", "PUSH", "a", "PUSH", "b", "GT", "JEQ", "LABEL2", ".LABEL2", "TYP", "INT", "a", "STRTEX", "PUSH", "11", "EQL", "a", "ENDEX", "LEND2", "ENDW", "TYP", "INT", "REZ", "PUSH", "REZ", "EQL", "1", "LEND0", "ENDW", "SDKEND"])

filename = file_processor("../Compiler/Intermediate.sdk")
tokens = Iterator(filename.getToks())
runTokens = Iterator(filename.getToks())


#- - - - - - - - - - - - - - - - - - - - -All - - - - - - - - - - - - - - - - - - -
global glbl_sym_table
glbl_sym_table = SymbolTable('GLBL', None)
symtab_add(glbl_sym_table)
stack = Stack()
global isInExpression
isInExpression = False
global isInFunction
isInFunction = False
current_scope = "GLBL"
global recentPopFun
global whenStack
whenStack= Stack()

def TYP():
    global current_scope
    tokens.next() #this should pop off "TYP"
    varType = tokens.next() #pushes "INT, FLT, BOOL" onto stack
    varID = tokens.next() #variable identifier ("a", "b", "c")
    var = Variable(varID, None, varType)
    dict_of_symbolTabs[current_scope].add(varID, var)


def FUN():
    tokens.next()#pop FUN
    name = tokens.next() #name of function
    currentFunction = Function(tokens.next(), name) #return type
    while (tokens.next() == "PAR"):
        currentFunction.addParam(tokens.next(), tokens.next())
    currentFunction.startPC = tokens.counter
    dict_of_functions[name] = currentFunction
    while tokens.current() != "FUNEND":
        tokens.next()
    tokens.next()#pop End

def CALL():
    currentFunction = copy.deepcopy(dict_of_functions[tokens.next()])#functions should only be declared in global
    while tokens.next() == "PAR": #add all parameters
        global current_scope
        nextValue = tokens.next()
        try:
            if dict_of_symbolTabs[current_scope].lookup(nextValue) is not None:
                nextValue = dict_of_symbolTabs[current_scope].lookup(nextValue).getValue()
        except ValueError:
            print("value Not Found")

        currentFunction.setParamValues(nextValue)

    currentFunction.returnPC(tokens.getCounter()-1)#set return PC

    name = currentFunction.getName()
    counter = 0
    while (name + str(counter)) in dict_of_symbolTabs:
        counter += 1



    currentFunction.setName(name + str(counter))

    symbTable = SymbolTable(name + str(counter), current_scope)
    for key in currentFunction.getParams():
        symbTable.add(key, currentFunction.getParams()[key])

    dict_of_symbolTabs[name + str(counter)] = symbTable
    current_scope = name + str(counter) #set current_scope to the name of the function + number
    print "SCOPE HERE ----> "+current_scope
    stack.push(currentFunction)

    tokens.setCounter(currentFunction.getStartPC())
    global isInExpression
    if isInExpression:
        main()

def RTRN():
    global current_scope
    global isInExpression
    global recentPopFun
    print "Is in expression: " + str(isInExpression)
    tokens.next() #pop RTRN
    exitedFun = stack.pop() #pop the function from the stack
    recentPopFun = copy.deepcopy(exitedFun)
    stack.push(dict_of_symbolTabs[exitedFun.getName()].lookup(tokens.next()).getValue()) #push the returned value
    tokens.setCounter(exitedFun.getReturnPC())
    current_scope = dict_of_symbolTabs[exitedFun.getName()].getPrevScope()

def LABL_TRACK():
    while runTokens.current() != "SDKEND":
        label = runTokens.current()
        if re.match(labelPat, label):
            global current_scope
            # print "Current Scope: " + current_scope
            current_label = Label(runTokens.current().replace(".", ""), runTokens.getCounter()+1, current_scope)
            # ltermnum = label[:-1]
            current_scope = label.replace(".", "")
        if re.match(lendPat, label):
            global current_scope
            # print "Exit Scope: " + current_scope
            current_scope = dict_of_symbolTabs[current_scope].getPrevScope()
        runTokens.next()
    current_scope = "GLBL"


def STARTEX():
    global isInExpression
    isInExpression = True

    while tokens.current() != "ENDEX":
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
                nextToken = tokens.next()

                varObj = dict_of_symbolTabs[current_scope].lookup(nextToken)
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
        elif nextToken == "CALL":
            #tokens.setCounter(tokens.getCounter()-1)
            CALL()
            global recentPopFun
            if recentPopFun.getName()[-1:] == 0:
                print "RECENT POP FUN: " + recentPopFun.getName()
                isInExpression = False

    tokens.next()


def FUNEND():
    finishedFunction = stack.pop()
    tokens.setCounter(finishedFunction.getRetrunPC())

def LABL():
    lname = tokens.current().replace(".", "")
    global current_scope
    current_scope = lname
    tokens.next()

def CMP():
    if stack.pop() >= 1:
        tokens.next()
    else:
        global current_scope
        while tokens.current() != "LOOPLEND"+str(current_scope[-1:]):
            tokens.next()
def JMP():
    tokens.next()
    label = tokens.next()
    global current_scope
    current_scope = label
    dict_of_symbolTabs[label].emptyTable()
    tokens.setCounter(dict_of_labels[label].getStart())

def JEQ():
    if stack.pop() >= 1:
        tokens.next()
        global current_scope
        global isInFunction
        current_scope = tokens.next()
        tokens.setCounter(dict_of_labels.get(current_scope).getStart())
    else:
        tokens.next()
        curr_scope = tokens.current()
        num = curr_scope[-1:]
        while tokens.current() != "LEND"+str(num) :
            tokens.next()
        # if current_scope is not "GLBL":
        #    current_scope = dict_of_symbolTabs[current_scope].getPrevScope()

def WHEN():
    global whenStack
    global current_scope
    whenStack.push(current_scope)
    tokens.next()

def WLEND():
    while tokens.current() != "ENDW":
        tokens.next()
    if tokens.current() == "ENDW":
        global current_scope
        global whenStack
        current_scope = whenStack.pop()
    # global current_scope
    # current_scope = dict_of_symbolTabs.get(current_scope).getPrevScope()

def LOOPLEND():
    global current_scope
    current_scope = dict_of_symbolTabs[current_scope].getPrevScope()
    tokens.next()

def PRNT():
    expression = stack.pop()
    print "HELLO   --> "+str(expression)+" <-- HELLO"
    tokens.next()

def main():
    global isInExpression
    if not isInExpression:
        LABL_TRACK()
    while tokens.current() != "SDKEND":
        nextToken = tokens.current()
        print nextToken
        #print(nextToken)
        if nextToken == "TYP":
            TYP()
        elif nextToken == "FUN":
            FUN()
        elif nextToken == "CALL":
            CALL()
        elif nextToken == "RTRN":
            RTRN()
            if isInExpression:
                return
        elif nextToken == "STRTEX":
            STARTEX()
        elif nextToken == "FUNEND":
            FUNEND()
        elif re.match(labelPat, nextToken):
            LABL()
        elif nextToken == "CMP":
            CMP()
        elif nextToken == "JMP":
            JMP()
        elif nextToken == "JEQ":
            JEQ()
        # elif nextToken is "JNEQ":
        #     JNEQ()
        elif nextToken == "LEND"+current_scope[-1:] :
            WLEND()
        elif nextToken == "LOOPLEND"+current_scope[-1:]:
            LOOPLEND()
        elif nextToken == "ENDPRNT":
            PRNT()
        elif nextToken == "WHEN":
            WHEN()
        else:
            tokens.next()
    print dict_of_symbolTabs
    #LABL(curr_labeltokens.current())
#Call the main method. Starts runtime.
main()