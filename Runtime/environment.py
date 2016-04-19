from classes import *
import re
#Globals
#highlevel code looks like:
    #integer a, b := 10, c:=20.
#tokens = Iterator(["TYP", "INT", "a", "a", "EQL", "NULL", "TYP", "INT", "b", "b", "EQL", "10", "TYP", "INT", "c", "c", "EQL", "20", "EOL"])


tokens = Iterator(["FUN", "sampleFunction", "INT", "PAR", "INT", "param1", "PAR", "BOOL", "param2", "STRT", "TYP", "INT", "a", "a", "EQL", "10", "EOL", "END"])
glbl_vardict = {} #this contains all our variables and their values
glbl_labeldict = {} #this contains all the labels and lines inside them
curr_labeltokens = Iterator([".LABEL1", "TYP", "INT", "res", "res", "EQL", "10","EOL", "PLUS", "res", "1", "MOV", "res", "Register_Add", "EOL" , "END"])
stack = Stack()

def TYP():
    #create varaible
    while (tokens.next() is not "EOL"): #this should also pop off "TYP" along with "EOL"
        stack.push(tokens.next()) #pushes "INT, FLT, BOOL" onto stack
        varID = tokens.next() #variable identifier ("a", "b", "c")
        glbl_vardict[varID] = Variable() #create varaibale object in map
        glbl_vardict[varID].setValueType(stack.pop())
        tokens.next() #remove the extra identifier ("a", "b", "c")
        tokens.next()#remove "EQL"
        glbl_vardict[varID].setValue(tokens.next())

def FUN():
    tokens.next()#pop FUN
    name = tokens.next() #name of function
    currentFunction = Function(tokens.next()) #return type
    while (tokens.next() is "PAR"):
        currentFunction.addParam(tokens.next(), tokens.next())
    tokens.next() #pop off "STRT"
    currentFunction.startPC = tokens.counter
    glbl_vardict[name] = currentFunction
    print(glbl_vardict)

def LABL(label):
    labelPat = r'\.LABEL[0-9]*'
    if re.match(labelPat, label):
        current_label = Label(curr_labeltokens.current().replace(".", ""))
        current_label.precedSymTab = glbl_vardict
        curr_labeltokens.next()
        while curr_labeltokens.current() is not "END":
            current_label.lInstrQueue.append(curr_labeltokens.current())
            curr_labeltokens.next()
        print label+" ~~~> Instr Queue: "+ str(current_label.lInstrQueue)
    # instrEvaluator =  Iterator(current_label.lInstrQueue
    else:
        print "Label Error: "+ label


def main():
    nextToken = tokens.current()
    if nextToken is "TYP":
        TYP()
    elif nextToken is "FUN":
        FUN()
    LABL(curr_labeltokens.current())
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
