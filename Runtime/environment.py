from classes import *
import re

#Globals
#highlevel code looks like:
    #integer a, b := 10, c:=20.

current_scope = "GLBL"
tokens = Iterator(["FUN", "sampleFunction", "INT", "PAR", "INT", "param1", "PAR", "INT", "param2", "STRT", "TYP", "INT", "a", "STRTEX", "PUSH", "10", "EQL", "a", "ENDEX", "FUNEND", "CALL", "sampleFunction", "PAR", "10", "PAR", "20", "SDK"])
labelPat = r'\.LABEL[0-9]*'
glbl_labeldict = {} #this contains all the labels and lines inside them
curr_labeltokens = Iterator([".LABEL1", "TYP", "INT", "res", "res", "EQL", "10","EOL", "PUSH", "res", "PUSH", "1", "ADD", "EOL" , "LEND1"])
loop_labeltokens = Iterator(["SDKSTRT","TYP", "INT", "a", "PUSH", "a", "PUSH", "10", "EQL", "TYP", "INT", "b", "PUSH", "b", "Push", "15", "EQL", ".LABEL2", "LOOP", "STRTEX", "PUSH", "a", "PUSH", "b", "LT", "ENDEX", "CMP", "PUSH", "a", "PUSH", "a", "ADD", "EQL", "JMP", "LABEL2", "LEND2", "SDKEND"])
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
        currentFunction.setParamValues(tokens.next())
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
    while loop_labeltokens.current() is not "SDKEND":
        label = loop_labeltokens.current()
        if re.match(labelPat, label):
            loop_labeltokens.next()
            current_label = Label(loop_labeltokens.current().replace(".", ""), loop_labeltokens.getCounter())
        # ltermnum = label[:-1]
        loop_labeltokens.next()
    print dict_of_symbolTabs.values()
    # for key in dict_of_labels.keys():
    #     pc, name = dict_of_labels.get(key).getStart(), dict_of_labels.get(key).name
    #     print name + " Starts at ---->" + str(pc)
        # while curr_labeltokens.current() is not "LEND"+ltermnum:
            # current_label.lInstrQueue.append(curr_labeltokens.current())
            # curr_labeltokens.next()
        # print label+" ~~~> Instr Queue: "+ str(current_label.lInstrQueue)
        # print current_label.lSymbTab.getTable().keys()
        # for lInstrQueue
    # instrEvaluator =  Iterator(current_label.lInstrQueue
    # else:
    #     print "Label Error: "+ label



def STARTEX():
    while tokens.current() is not "ENDEX":
        nextToken = tokens.next()
        if nextToken == "PUSH":
            varName = tokens.next()
            if re.match(r'[+-]?(\d+(\.\d*)?|\.\d+)', varName):
                stack.push(varName)
            else:
                try:
                    stack.push(dict_of_symbolTabs[current_scope].lookup(varName).getValue())
                except ValueError:
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

def main():
    dict_of_symbolTabs[current_scope] = GlblSymTab()
    while tokens.current() is not "SDK":
        print("dict_of_symbolTabs: {0}".format(dict_of_symbolTabs))
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
        else:
            tokens.next()

    #LABL(curr_labeltokens.current())
#Call the main method. Starts runtime.
main()
