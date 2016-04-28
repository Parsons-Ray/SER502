#Classes we will need
global dict_of_symbolTabs
dict_of_symbolTabs = {}
global dict_of_labels
dict_of_labels = {}
global dict_of_functions
dict_of_functions = {}



def symtab_add(name):
    if name.symName not in dict_of_symbolTabs:
        dict_of_symbolTabs[name.symName] = name
    else:
        raise KeyError("Symbol table exists, compilation error")

def label_add(Label):
    if Label.name not in dict_of_labels:
        dict_of_labels[Label.name] = Label
    else:
        raise KeyError("Label exists, cannot redeclare label")

def label_del(name):
    if name in dict_of_labels:
        dict_of_labels.remove(name)
    else:
        raise KeyError("Label does not exist")

def symtab_del(name):
    if name.symName in dict_of_symbolTabs:
        dict_of_symbolTabs.remove(name)
    else:
        raise KeyError("Symbol table not in dict")


global glbl_sym_table

class file_processor:
    def __init__(self, text_file):
        self.filename = text_file

    def getToks(self):
        return [word for line in open(self.filename, 'r') for word in line.split()]


class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)
         #print("Stack: {0}".format(self.items))

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
    def __init__(self, name, value, valueType):
        self.name = name
        self.value = value
        self.valueType = valueType

    def getValue(self):
        return self.value

    def getType(self):
        return self.valueType

    def setValueType(self, valueType):
        self.valueType = valueType #should be string ("INT", "FLT", "BOOL")

    def setValue(self, value):#check and set the value to the appropriate type.
        if value == "NULL":
            self.value = None
        elif self.valueType == "INT":
            self.value = int(value)
        elif self.valueType == "FLT":
            self.value = float(value)
        elif self.valueType == "BOOL":
            if value == "true" or value == "false":
                self.value = value

    def __repr__(self):
        return ("Value: {0}, Type: {1}".format(self.value, self.valueType))

class Function:
    #this section should be done on declaration
    def __init__(self, returnType, name):
        self.tbl = {}
        self.name = name
        #self.lSymbTab = SymbolTable(name, 'GLBL')
        self.params = {}
        self.order = []
        self.returnType = returnType

    def addParam(self, paramType, paramName):
        var = Variable(paramName, "NULL", paramType)
        self.params[paramName] = var
        self.order.append(paramName)

    def startPC(self, startPC): #where the start of the body of the funciton is.
        self.startPC = startPC

    #this section should be used when the function is called
    # def setScope(self, previousScope):
    #     self.lSymbTab.setScope(previousScope)

    def setParamValues(self, value):
        for param in self.order:
            if self.params[param].getValue() == "NULL":
                self.params[param].setValue(value)
                break

    def setName(self, name):
        self.name = name
    def getParams(self):
        return self.params

    def getStartPC(self):
        return self.startPC

    def getReturnPC(self):
        return self.returnPC

    def getName(self):
        return self.name

    # def initSymbolTable(self):
    #     self.symTable = SymbolTable(self.name, current_scope, glbl_sym_table)

    def returnPC(self, returnPC): #place in the enviroment above it to return to after completeing.
        self.returnPC = returnPC


    def __repr__(self):
        return "Name: {0} ".format(self.name)

class SymbolTable:

        # set scope hierarchy for current symbol table

    def __init__(self, symName, prevScope):
        self.symName = symName # symbol table name
        self.tbl = {}  # symbol table
        self.prevScope = prevScope # previousScope

    def add(self, varname, variable):
        # add identifier to symbol table
        try:
            if varname in self.tbl:
                raise ValueError("Identifier exists")
            else:
                self.tbl[varname] = variable
        except ValueError:
            print "Compilation Error: Identifier exists"

    def getPrevScope(self):
        return self.prevScope

    # def getScope(self):
    #     return self.scope_hierarchy

    def setPrevScope(self, scope):
        self.prevScope = scope
    def getTable(self):
        return self.tbl

    def lookup(self, symbol):

        if symbol in self.tbl:
            return self.tbl[symbol]
        else:

            if self.prevScope is not None:
                return dict_of_symbolTabs[self.prevScope].lookup(symbol)
            else:
                return None

    def emptyTable(self):
        self.tbl.clear()

    def __repr__(self):
        return "table: {0}, prevScope: {1}".format(self.tbl, self.prevScope)

class Label:

    def __init__(self, name, pc, prevScope):
        self.name = name
        self.lstartpc = pc
        self.lSymbTab = SymbolTable(self.name, prevScope)
        symtab_add(self.lSymbTab)
        label_add(self)

    def getStart(self):
        return self.lstartpc

    def lnext(self):
        for instr in lInstrQueue:
            yield instr
