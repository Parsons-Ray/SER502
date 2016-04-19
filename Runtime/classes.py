#Classes we will need
class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)

class Iterator:
    def __init__(self, values):
        self.items = values
        self.counter = 0

    def current(self):
        if self.counter < len(self.items):
            return self.items[self.counter]
        else:
            return None

    def next(self): #NOTE: counter is incremented AFTER we pick out the value we are returning.
        if self.counter < len(self.items):
            val = self.items[self.counter]
            self.counter += 1
            return val
        else:
            return None

    def setCounter(self, newCounter):
        self.counter = newCounter

    def getCounter(self):
        return self.counter

class Variable:
    def getValue(self):
        return self.value

    def getType(self):
        return self.valueType

    def setValueType(self, valueType):
        self.valueType = valueType #should be string ("INT", "FLT", "BOOL")

    def setValue(self, value):#check and set the value to the appropriate type.
        if value is "NULL":
            self.value = "NULL"
        elif self.valueType is "INT":
            self.value = int(value)
        elif self.valueType is "FLT":
            self.value = float(value)
        elif self.valueType is "BOOL":
            if value is "true" or value is "false":
                self.value = value

    def __repr__(self):
        return ("Value: {0}, Type: {1}".format(self.value, self.valueType))

class Function:
    #this section should be done on declaration
    def __init__(self, returnType):
        self.paramValues = {} #format: {'paramName': value}
        self.paramTypes = {} #format: {'paramType': Type}
        self.returnType = returnType

    def addParam(self, paramType, paramName):
        self.paramValues[paramName] = "NULL" #this value will be set when function is called
        self.paramTypes[paramName] = paramType

    def startPC(self, startPC): #where the start of the body of the funciton is.
        self.startPC = startPC

    #this section should be used when the function is called
    def setParamValues(self, paramName, value):
        self.paramValues[paramName] = value

    def returnPC(self, returnPC): #place in the enviroment above it to return to after completeing.
        self.returnPC = returnPC

    def setSymbolTable(self, symbolTable):
        self.symbolTable = symbolTable #This allows us to use all symbols defined in the environment above.

    def __repr__(self):
        return "ReturnType: {0}, ParamValues: {1}, paramType: {2}, startPC: {3}".format(self.returnType, self.paramValues, self.paramTypes, self.startPC)


class Label:

    def __init__(self, name):
        self.name = name
        self.lSymbolTab = {}
        self.lInstrQueue =  []
        self.precedSymTab = {}

    def setSymbolTable(self, symbolTable):
        self.precedSymTab = symbolTable