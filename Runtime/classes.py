#Classes we will need
global dict_of_symbolTabs
dict_of_symbolTabs = {}
global dict_of_labels
dict_of_labels = {}
global current_scope
global dict_of_functions
dict_of_functions = {}


current_scope = "GLBL"


def symtab_add(name):
    if name.symName not in dict_of_symbolTabs:
        dict_of_symbolTabs[name.symName] = name.tbl
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

class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)
         print("Stack: {0}".format(self.items))

     def pop(self):
         print("Stack: {0}".format(self.items))
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
        if value is "NULL":
            self.value = None
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
    def __init__(self, returnType, name):
        self.tbl = {}
        self.name = name
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
    def setParamValues(self, value):
        for param in self.order:
            if self.params[param].getValue() is "NULL":
                self.params[param].setValue(value)
                break


    def getParams(self):
        return self.params
    def getStartPC(self):
        return self.startPC

    def getRetrunPC(self):
        return self.returnPC

    def getName(self):
        return self.name

    # def initSymbolTable(self):
    #     self.symTable = SymbolTable(self.name, current_scope, glbl_sym_table)

    def returnPC(self, returnPC): #place in the enviroment above it to return to after completeing.
        self.returnPC = returnPC

    def __repr__(self):
        return "ReturnType: {0}, params: {1},  startPC: {2}, order: {3}, returnPC: {4}".format(self.returnType, self.params,  self.startPC, self.order, self.returnPC)




class GlblSymTab:
    def __init__(self):
        self.tbl = {}
        self.name = "GLBL"


    def getTable(self):
        return self.tbl

    def add(self, varname, variable):
        # add identifier to symbol table
        try:
            if varname in tbl:
                raise ValueError("Identifier exists")
                # if tbl[varname].getType() == variable.getType():
                #     tbl[varname].setValue(variable.getValue())
                # else:
                #     raise ValueError("DataType mismatch for %r - defined as %r".format(varname, tbl[varname].getType))
            else:
                tbl[varname] = variable
        except ValueError:
            print "Compilation Error: Identifier exists"

    def lookup(self, symbol):
        try:
            if symbol in self.tbl:
                exists =  self.tbl.get(symbol, default=None)
                if exists:
                    return exists.getValue()
                else:
                    raise ValueError("Symbol Not set")
            else:
                raise ValueError("Symbol not found")
        except ValueError:
            print "Compilation Error: Identifier not found"

glbl_sym_table = GlblSymTab()


class SymbolTable:

        # set scope hierarchy for current symbol table

    def __init__(self, symName, prevScope, glblSymtab = glbl_sym_table):
        self.symName = symName # symbol table name
        self.tbl = {}  # symbol table
        self.scope_hierarchy = []  # Scope Hierarchy list contains the list of the preceding scope
        self.prevScope = prevScope # previousScope
        self.scope_hierarchy.insert(0, prevScope)
        list_of_prev_scope = None

        try:
            list_of_prev_scope = dict_of_symbolTabs.get(prevScope, None).getScope()
        except:
            # print("No previous scope")
            list_of_prev_scope = None
        if list_of_prev_scope:
            for scope in list_of_prev_scope:
                self.scope_hierarchy.append(scope)
        self.glblSymTab = glblSymtab # access to global symbol table



    def add(self, varname, variable):
        # add identifier to symbol table
        try:
            if varname in self.tbl:
                raise ValueError("Identifier exists")
                # if tbl[varname].getType() == variable.getType():
                #     tbl[varname].setValue(variable.getValue())
                # else:
                #     raise ValueError("DataType mismatch for %r - defined as %r".format(varname, tbl[varname].getType))
            else:
                self.tbl[varname] = variable
        except ValueError:
            print "Compilation Error: Identifier exists"

    def getScope(self):
        return self.scope_hierarchy

    def getTable(self):
        return self.tbl

    def lookup(self, symbol):
        # lookup symbol table
        try:
            if symbol in self.tbl:
                exists =  self.tbl.get(symbol, None)
                if exists:
                    return exists
                elif not exists:
                    for symTabNames in self.scope_hierarchy:
                        exists = dict_of_symbolTabs.get(symTabNames).getTable().get(symbol, None)
                        if exists:
                            return exists
                            break
                    if not exists:
                        exists = self.glblSymTab.getTable().get(symbol, None)
                        if exists:
                            return exists
                else:
                    raise ValueError("Couldn't find symbol, is it declared?")
        except ValueError:
            print "Compilation Error: Identifier not found"

    def __repr__(self):
        return "table: {0}, prevScope: {1}".format(self.tbl, self.prevScope)
class Label:

    def __init__(self, name, pc):
        self.name = name
        self.lstartpc = pc
        self.lSymbTab = SymbolTable(self.name, current_scope, glbl_sym_table)
        symtab_add(self.lSymbTab)
        label_add(self)

    def getStart(self):
        return self.lstartpc

    def lnext(self):
        for instr in lInstrQueue:
            yield instr
