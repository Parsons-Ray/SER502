from classes import *

#Globals
#highlevel code looks like:
    #integer a, b := 10, c:=20.
#tokens = Iterator(["TYP", "INT", "a", "a", "EQL", "NULL", "TYP", "INT", "b", "b", "EQL", "10", "TYP", "INT", "c", "c", "EQL", "20", "EOL"])
tokens = Iterator(["FUN", "sampleFunction", "INT", "PAR", "INT", "param1", "PAR", "BOOL", "param2", "STRT", "TYP", "INT", "a", "a", "EQL", "10", "EOL", "END"])
varDict = {} #this contains all our variables and their values
stack = Stack()

def TYP():
    #create varaible
    while (tokens.next() is not "EOL"): #this should also pop off "TYP" along with "EOL"
        stack.push(tokens.next()) #pushes "INT, FLT, BOOL" onto stack
        varID = tokens.next() #variable identifier ("a", "b", "c")
        varDict[varID] = Variable() #create varaibale object in map
        varDict[varID].setValueType(stack.pop())
        tokens.next() #remove the extra identifier ("a", "b", "c")
        tokens.next()#remove "EQL"
        varDict[varID].setValue(tokens.next())

def FUN():
    tokens.next()#pop FUN
    name = tokens.next() #name of function
    currentFunction = Function(tokens.next()) #return type
    while (tokens.next() is "PAR"):
        currentFunction.addParam(tokens.next(), tokens.next())
    tokens.next() #pop off "STRT"
    currentFunction.startPC = tokens.counter
    varDict[name] = currentFunction
    print(varDict)


def main():
    nextToken = tokens.current()
    if nextToken is "TYP":
        TYP()
    elif nextToken is "FUN":
        FUN()
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
