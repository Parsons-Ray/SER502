__author__ = 'Shashank'
from classes import *
import re
#Globals
#highlevel code looks like:
    #integer a, b := 10, c:=20.
#tokens = Iterator(["TYP", "INT", "a", "a", "EQL", "NULL", "TYP", "INT", "b", "b", "EQL", "10", "TYP", "INT", "c", "c", "EQL", "20", "EOL"])
current_scope = "GLBL"
# tokens = Iterator(["FUN", "sampleFunction", "INT", "PAR", "INT", "param1", "PAR", "BOOL", "param2", "STRT", "TYP", "INT", "a", "a", "EQL", "10", "EOL", "END"])
labelPat = r'\.LABEL[0-9]*'
whenEndPat = r'\.WLEND[0-9]*'
# glbl_vardict = {} #this contains all our variables and their values
# glbl_labeldict = {} #this contains all the labels and lines inside them
# curr_labeltokens = Iterator([".LABEL1", "TYP", "INT", "res", "res", "EQL", "10","EOL", "PUSH", "res", "PUSH", "1", "ADD", "EOL" , "LEND1"])
tokens = Iterator(["SDKSTRT","TYP", "INT", "a", "STRTEX", "PUSH", "a", "PUSH", "10", "EQL", "ENDEX", "TYP", "INT", "b", "STRTEX", "PUSH", "b", "PUSH", "15", "EQL", "ENDEX", ".LABEL2", "LOOP", "STRTEX", "PUSH", "a", "PUSH", "b", "LT", "ENDEX", "CMP", "PUSH", "a", "PUSH", "a", "ADD", "EQL", "JMP", "LABEL2", "LEND2", "SDKEND"])
runTokens = Iterator(["SDKSTRT","TYP", "INT", "a", "STRTEX", "PUSH", "a", "PUSH", "10", "EQL", "ENDEX", "TYP", "INT", "b", "STRTEX", "PUSH", "b", "PUSH", "15", "EQL", "ENDEX", "LOOP", ".LABEL2", "STRTEX", "PUSH", "a", "PUSH", "b", "LT", "ENDEX", "CMP", "PUSH", "a", "PUSH", "a", "ADD", "EQL", "WHEN", "STRTEX", "PUSH", "a" , "PUSH", "12", "LT", "JEQ", "LABEL2", "WHEN",".LABEL3", "TYP", "INT", "a", "PUSH", "13", "EQL", "a", "WLEND3", "JMP", "LABEL2", "LOOPLEND2", "SDKEND"])
symtab_add("GLBL")
stack = Stack()


# def TYP():

#     #create varaible
#     while (tokens.next() is not "EOL"): #this should also pop off "TYP" along with "EOL"
#         stack.push(tokens.next()) #pushes "INT, FLT, BOOL" onto stack
#         varID = tokens.next() #variable identifier ("a", "b", "c")
#         glbl_vardict[varID] = Variable() #create varaibale object in map
#         glbl_vardict[varID].setValueType(stack.pop())
#         tokens.next() #remove the extra identifier ("a", "b", "c")
#         tokens.next()#remove "EQL"
#         glbl_vardict[varID].setValue(tokens.next())
#
# def FUN():
#     tokens.next()#pop FUN
#     name = tokens.next() #name of function
#     currentFunction = Function(tokens.next()) #return type
#     while (tokens.next() is "PAR"):
#         currentFunction.addParam(tokens.next(), tokens.next())
#     tokens.next() #pop off "STRT"
#     currentFunction.startPC = tokens.counter
#     glbl_vardict[name] = currentFunction
#     print(glbl_vardict)

def LABL_TRACK():
    while runTokens.current() is not "SDKEND":
        label = runTokens.current()
        if re.match(labelPat, label):
            current_label = Label(runTokens.current().replace(".", ""), runTokens.getCounter()+1)
            # ltermnum = label[:-1]
        runTokens.next()
    # print dict_of_symbolTabs.values()
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

def TYP():
    print "type def"
    tokens.next()
    # varType = tokens.current()
    # varName = tokens.next()
    # variable = Variable()


def LABL():
    lname = tokens.current().replace(".", "")
    global current_scope
    current_scope = lname
    tokens.next()

def CMP():
    if stack.pop() >= 1:
        tokens.next()
    else:
        while tokens.current() is not "LOOPLEND"+current_scope[:-1]:
            tokens.next()
def JMP():
    label = tokens.next()
    global current_scope
    current_scope = label
    tokens.setCounter(dict_of_labels.get(label).getStart())

def JEQ():
    if stack.pop() >= 1:
        global current_scope
        current_scope = tokens.next()
        tokens.setCounter(dict_of_labels.get(current_scope).getStart())
    else:
        while tokens.current() is not "WLEND"+ current_scope[:-1]:
            tokens.next()

def WLEND():
    while tokens.current() is not "ENDW":
        tokens.next()

# def JNEQ():
#     if stack.pop() == 0:
#         global current_scope
#         current_scope = tokens.next()
#         tokens.setCounter(dict_of_labels.get(current_scope).getStart())
#     else:
#         while tokens.current() is not "LEND"+ current_scope[:-1]:
#             tokens.next()

def main():
    # nextToken = tokens.current()
    # if nextToken is "TYP":
    #     TYP()
    # elif nextToken is "FUN":
    #     FUN()
    LABL_TRACK()
    print "lbl track"
    print dict_of_labels.keys()
    if tokens.current() is "SDKSTRT":
        nextToken = tokens.next()
        while tokens.current() is not "SDKEND":
            nextToken = tokens.current()
            if nextToken is "TYP":
                TYP()
            elif re.match(labelPat, nextToken):
                LABL()
            elif nextToken is "CMP":
                CMP()
            elif nextToken is "JMP":
                JMP()
            elif nextToken is "JEQ":
                JEQ()
            elif nextToken is "JNEQ":
                JNEQ()
            elif re.match(whenEndPat, nextToken):
                WLEND()
            else:
                tokens.next()
            # elif nextToken is "INT" or "FLT" or "BOOL":
                # compstack.push(nextToken)
                # loop_labeltokens.next()
            # elif nextToken is

#Call the main method. Starts runtime.
main()


# FUN sampleFunction INT        #using 'integer' so we can push it onto stack and check return type at end.
#     PAR INT param1
#     PAR BOOL param2
#     STRT
#       TYP INT x
#       x EQL 10
#       TYP INT y
#       y EQL 20
#       EOL
#       TYP INT z
#       z EQL x y ADD
#       RTRN z
#     END
