from classes import *
import re

curr_labeltokens = Iterator([".LABEL1", "TYP", "INT", "res", "res", "EQL", "10","EOL", "PUSH", "res", "PUSH", "1", "ADD", "EOL" , "LEND"])
#tokens = Iterator(["TYP", "INT", "a", "a", "EQL", "NULL", "TYP", "INT", "b", "b", "EQL", "10", "TYP", "INT", "c", "c", "EQL", "20", "EOL"])
tokens = Iterator(["FUN", "sampleFunction", "INT", "PAR", "INT", "param1", "PAR", "BOOL", "param2", "STRT", "TYP", "INT", "a", "a", "EQL", "10", "EOL", "END"])

glbl_labeldict = {} #this contains all the labels and lines inside them
stack = Stack()

def TYP():
    #create varaible
    while (tokens.next() is not "EOL"): #this should also pop off "TYP" along with "EOL"
        varType = tokens.next() #pushes "INT, FLT, BOOL" onto stack
        varID = tokens.next() #variable identifier ("a", "b", "c")
        if tokens.next() is "EQL":#remove "EQL"
            varVal = tokens.next()
            var = Variable(varID, varVal, varType)
        else:
            var = Variable(varID, "NULL", varType)
        dict_of_symbolTabs[current_scope].add(varID, var)

def FUN():
    tokens.next()#pop FUN
    name = tokens.next() #name of function
    currentFunction = Function(tokens.next(), name) #return type
    while (tokens.next() is "PAR"):
        currentFunction.addParam(tokens.next(), tokens.next())
    tokens.next() #pop off "STRT"
    currentFunction.startPC = tokens.counter
    dict_of_symbolTabs[current_scope].add(name, currentFunction) #ideally this will be 'current_scope' = "global"

def CALL():
    tokens.next() #pop CALL
    currentFunction = dict_of_symbolTabs[current_scope].lookup(tokens.next())
    while tokens.next() is "PAR":
        currentFunction.setParamValues(tokens.next())
    currentFunction.returnPC(tokens.current())
    currentFunction.setSymbolTable(current_scope)
    stack.push(currentFunction)
    tokens.setCounter(currentFunction.getStartPC())

def RTRN():
    tokens.next() #pop RTRN
    exitedFun = stack.pop() #pop the function from the stack
    stack.push(tokens.next()) #push the returned value
    tokens.setcounter(exitedFun.getReturnPC())

def LABL(label):
    labelPat = r'\.LABEL[0-9]*'
    if re.match(labelPat, label):
        current_label = Label(curr_labeltokens.current().replace(".", ""))
        current_label.precedSymTab = glbl_vardict
        curr_labeltokens.next()
        while curr_labeltokens.current() is not "LEND":
            current_label.lInstrQueue.append(curr_labeltokens.current())
            curr_labeltokens.next()
        print label+" ~~~> Instr Queue: "+ str(current_label.lInstrQueue)
    # instrEvaluator =  Iterator(current_label.lInstrQueue
    else:
        print "Label Error: "+ label


def main():
    current_scope = "global"
    nextToken = tokens.current()
    if nextToken is "TYP":
        TYP()
    elif nextToken is "FUN":
        FUN()
    elif nextToken is "CALL":
        CALL()
    elif nextToken is "RTRN":
        RTRN()

    LABL(curr_labeltokens.current())
#Call the main method. Starts runtime.
main()
