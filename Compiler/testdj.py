__author__ = 'Digant'
import pyparsing as pp
import os
import re
from pprint import pprint
from InfixToPostfix import infixToPostfixConv, isOperator


# Function to remove WhiteSpaces
def removeWhiteSpace(expression):
    return expression.replace(" ", "")


# Writing to Intermediate Intermediate.sdk file
def writeFile(my_list):
    with open("Intermediate.sdk", 'w') as f:
        f.write("SDKSTRT" + '\n')
        index = 0
        while index <= len(my_list) - 1:
            for s in my_list[index]:
                f.write(s + '\n')
            index += 1
        f.write("SDKEND" + '\n')


# Process : Scanner/Parser to generate Tokenized Output
def parseSDK(input):
    # Global Variable Setting
    global eol
    global commaLit
    global assign
    global lsqBracs
    global lcrBracs
    global rsqBracs
    global rcrBracs
    global numeric
    global plus
    global minus
    global when
    global elsevar
    global typeName
    global prevElement
    global nextElement
    prevElement = ''
    nextElement = ''

    eol = pp.Literal(".")
    commaLit = pp.Literal(",")
    assign = pp.Literal(":=")
    lsqBracs = pp.Literal("[")
    rsqBracs = pp.Literal("]")
    numeric = pp.Word(pp.nums)
    plus = pp.Literal("+")
    minus = pp.Literal("-")
    when = pp.Keyword("when")
    elsevar = pp.Keyword("else")
    elseWhen = pp.Keyword("elseWhen")
    loop = pp.Keyword("loop")
    lBracs = pp.Literal("(")
    rBracs = pp.Literal(")")
    lcrBracs = pp.Literal("{")
    rcrBracs = pp.Literal("}")
    andExpr = pp.Keyword("&&")
    orExpr = pp.Keyword("||")
    notExpr = pp.Keyword("!")
    breakStatement = pp.Keyword("break") + eol
    numericLiteral = numeric
    stringLiteral = pp.Word(pp.alphas, pp.alphanums)
    identifier = stringLiteral
    size = numericLiteral
    unaryAddingOperator = pp.Or(plus ^ minus)
    binaryAddingOperator = pp.Or(plus ^ minus)
    relationalOperator = pp.Or(
        pp.Literal("==") ^ pp.Literal("!=") ^ pp.Literal("<") ^ pp.Literal(">") ^ pp.Literal("<=") ^ pp.Literal(">="))
    multiplyingOperator = pp.Or(pp.Literal("*") ^ pp.Literal("/"))
    # Made Change here
    simpleStatement = pp.Forward()
    compoundStatement = pp.Forward()
    expr = pp.Forward()
    actualParameter = pp.Or(numericLiteral ^ identifier ^ expr)
    functionCallExpression = identifier + lBracs + actualParameter + rBracs
    functionCallStatement = functionCallExpression + eol
    primary = pp.Or(numericLiteral ^ stringLiteral ^ pp.Literal("true") ^ pp.Literal("false") ^ functionCallExpression)
    # Made Change here
    factor = pp.Or((primary + pp.Optional(pp.Literal("^") + primary)) ^ (notExpr + primary))
    term = factor + pp.ZeroOrMore(multiplyingOperator + factor)
    simpleExpression = pp.Optional(unaryAddingOperator) + term + pp.ZeroOrMore(binaryAddingOperator + term)
    relation = pp.ZeroOrMore(lBracs) + simpleExpression + pp.ZeroOrMore(relationalOperator + simpleExpression) + pp.ZeroOrMore(rBracs)
    # Changed this part due to error scenario : + pp.ZeroOrMore(pp.Or((pp.Literal(",") + simpleExpression) ^ (relationalOperator + simpleExpression)))
    expr << relation + pp.ZeroOrMore(pp.Or((andExpr + relation)) ^ (orExpr + relation))
    indexedComponent = pp.Literal("[") + (expr + pp.ZeroOrMore("," + expr)) + pp.Literal("]")
    name = pp.Or(identifier ^ indexedComponent)
    condition = expr
    typeName = pp.Or(pp.Literal("integer") ^ pp.Literal("floating") ^ pp.Literal("boolean"))
    ArrayTypeDefinition = pp.Literal("Array") + typeName + pp.Literal("[") + (
        size + pp.ZeroOrMore(pp.Literal(",") + size)) + pp.Literal("]")
    typeDefinition = pp.Or(typeName ^ ArrayTypeDefinition)

    formalParameters = typeDefinition + identifier + pp.ZeroOrMore(commaLit + typeDefinition + identifier)

    returnStatement = pp.Literal("return") + relation + eol

    printStatement = pp.Literal("print") + expr + eol

    declarativeStatement = typeDefinition + identifier + pp.Optional(assign + expr) \
                           + pp.ZeroOrMore(pp.Literal(",") + identifier + pp.Optional(assign + relation)) + eol
    # + pp.ZeroOrMore(pp.Literal(",") + identifier + pp.Optional(assign + expr))

    assignmentStatement = identifier + pp.Optional(lsqBracs + numericLiteral + rsqBracs) + assign + expr + eol

    nullStatement = pp.Literal("none")

    functionSpecification = pp.Keyword("function") + identifier + pp.Literal(
        "->") + typeDefinition + lBracs + pp.Optional(formalParameters) \
                            + rBracs + lcrBracs + pp.ZeroOrMore(pp.Or(simpleStatement ^ compoundStatement)) + rcrBracs

    sequenceOfStatements = pp.Forward()
    ifStatement = when + condition + lcrBracs + pp.ZeroOrMore(simpleStatement) + rcrBracs + \
                  pp.ZeroOrMore(elseWhen + condition + lcrBracs + simpleStatement + rcrBracs) + \
                  pp.Optional(elsevar + lcrBracs + pp.ZeroOrMore(simpleStatement) + rcrBracs)
    loopStatement = loop + condition + lcrBracs + pp.ZeroOrMore(pp.Or(simpleStatement ^ compoundStatement ^ breakStatement)) + rcrBracs
    compoundStatement << pp.Or(loopStatement ^ ifStatement)
    simpleStatement << pp.Or(nullStatement ^ assignmentStatement ^ functionCallStatement ^ declarativeStatement ^
                             printStatement ^ returnStatement)
    statement = pp.Or(simpleStatement ^ functionSpecification ^ compoundStatement)
    sequenceOfStatements << pp.OneOrMore(statement)
    program = sequenceOfStatements

    return program.parseString(input)


def returnIntermediateOperator(sdkOperator):
    # Return Operator's Intermediate Symbol
    if sdkOperator == "+":
        return 'ADD'
    elif sdkOperator == "-":
        return 'SUB'
    elif sdkOperator == "*":
        return 'MUL'
    elif sdkOperator == "/":
        return 'DIV'
    elif sdkOperator == "=":
        return 'EQL'
    elif sdkOperator == "&&":
        return 'AND'
    elif sdkOperator == "||":
        return 'OR'
    elif sdkOperator == "<":
        return 'LT'
    elif sdkOperator == ">":
        return 'GT'
    elif sdkOperator == "<=":
        return 'LTE'
    elif sdkOperator == ">=":
        return 'GTE'
    elif sdkOperator == "==":
        return 'EEQL'
    elif sdkOperator == "!=":
        return 'NEQL'
    elif sdkOperator == "!":
        return 'NOT'


def typeNameIntermediateConvert(typeNames):
    # Return Intermediate Code for TypeNames
    if typeNames == "integer":
        return "INT"
    elif typeNames == "boolean":
        return "BOOL"
    elif typeNames == "floating":
        return "FLT"


def assignStatement(preValue, assStatement):
    # Input is an assignment statement like  a = b + c

    intermediateAssign = 'STRTEX\n'
    rightSide = assStatement.split("=")[1]
    m = re.search(r"[a-zA-Z]*\([a-zA-Z0-9*+-/]*\)", rightSide)
    if m is not None:
        funcName = m.group()
    rightSide = re.sub(r"[a-zA-Z]*\([a-zA-Z0-9*+-/]*\)", '@', rightSide)
    postfixExpr = infixToPostfixConv(removeWhiteSpace(rightSide)).split()
    for s in postfixExpr:
        if isOperator(s):
            if s == "@" and funcName is not None:
                intermediateAssign += "CALL " + funcName.split("(")[0] + "\n"
                for arg in funcName.split("(")[1].split(","):
                    arg = re.sub(r"\)", '', arg)
                    intermediateAssign += 'PAR ' + arg + '\n'
            else:
                intermediateAssign += returnIntermediateOperator(s) + "\n"
        else:
            intermediateAssign += 'PUSH ' + s + "\n"
    intermediateAssign += 'EQL ' + preValue + '\n'
    intermediateAssign += 'ENDEX'
    return intermediateAssign


# Variable Declaration Translator
def varDeclaration(tokenizedInput, value):
    # Eg : integer a, b := 10, c := 20.
    # Input : ['integer', 'a', ',', 'b', ':=', '10', ',', 'c', ':=', '20', '.']
    # Output :
    # TYP INT a
    # EQL NULL
    # TYP INT b
    # STRTEX
    # PUSH 10
    # EQL b
    # ENDEX
    # TYP INT c
    # STRTEX
    # PUSH 20
    # EQL c
    # ENDEX
    # EOL
    intermediateOutput = list()
    if value == "integer":
        nextValue = next(tokenizedInput)
        while nextValue != ".":
            if nextValue != ",":
                intermediateOutput.append("TYP INT " + nextValue)
                prevValue = nextValue
                nextValue = next(tokenizedInput)
                if nextValue == assign:
                    nextValue = next(tokenizedInput)
                    assStatement = prevValue + "=" + nextValue
                    intermediateOutput.append(assignStatement(prevValue, assStatement))
                    nextValue = next(tokenizedInput)
            else:
                nextValue = next(tokenizedInput)

    elif value == "floating":
        nextValue = next(tokenizedInput)
        while nextValue != ".":
            if nextValue != ",":
                intermediateOutput.append("TYP FLT " + nextValue)
                prevValue = nextValue
                nextValue = next(tokenizedInput)
                if nextValue == assign:
                    nextValue = next(tokenizedInput)
                    assStatement = prevValue + "=" + nextValue
                    intermediateOutput.append(assignStatement(prevValue, assStatement))
                    nextValue = next(tokenizedInput)
            else:
                nextValue = next(tokenizedInput)

    else:
        nextValue = next(tokenizedInput)
        while nextValue != ".":
            if nextValue != ",":
                intermediateOutput.append("TYP BOOL " + nextValue)
                prevValue = nextValue
                nextValue = next(tokenizedInput)
                if nextValue == assign:
                    nextValue = next(tokenizedInput)
                    assStatement = prevValue + "=" + nextValue
                    intermediateOutput.append(assignStatement(prevValue, assStatement))
                    nextValue = next(tokenizedInput)
            else:
                nextValue = next(tokenizedInput)
    # Return Error
    if nextValue != ".":
        intermediateOutput.append("SDK ERROR : Next Value = " + nextValue)
    return intermediateOutput


# Handling Variable or Expressions Declaration inside a Block
def blockDeclaration(tokenizedInput, value):
    global prevElement
    intermediateOutput = ''
    prevValue = value
    commaFlag = 0
    rightSide = ''
    # Variable Declaration or assignment
    if value in typeName:
        nextValue = next(tokenizedInput)
        while nextValue != ".":
            if nextValue != ",":
                intermediateOutput += "TYP " + typeNameIntermediateConvert(value) + " " + nextValue + "\n"
                prevValue = nextValue
                nextValue = next(tokenizedInput)
                if nextValue == assign:
                    nextValue = next(tokenizedInput)
                    while nextValue != '.':
                        rightSide += nextValue
                        nextValue = next(tokenizedInput)
                    assStatement = prevValue + "=" + rightSide
                    intermediateOutput += assignStatement(prevValue, assStatement)
            else:
                nextValue = next(tokenizedInput)
    elif value == "print":
        nextValue = next(tokenizedInput)
        rightSide = nextValue
        intermediateOutput += printStatement(tokenizedInput, nextValue)
        nextValue = next(tokenizedInput)
    elif value == "when":
        intermediateOutput += whenStatement(tokenizedInput,value)
    elif value == "return":
        nextValue = next(tokenizedInput)
        intermediateOutput += returnStatement(tokenizedInput, nextValue)
        nextValue = next(tokenizedInput)
    else:
        nextValue = next(tokenizedInput)
        if nextValue == ":=":
            # Normal Assignment without declaration
            rightSide = ''
            nextValue = next(tokenizedInput)
            while nextValue != eol:
                rightSide += nextValue
                nextValue = next(tokenizedInput)
            assStatement = value + '=' + rightSide
            intermediateOutput += assignStatement(value, assStatement)
        elif nextValue == "break":
            nextValue = next(tokenizedInput)
            rightSide = nextValue
            intermediateOutput += 'BREAK'
    # Return Error
    if prevElement != '}' and nextElement == '':
        if nextValue != "." and nextValue != '}':
        # print intermediateOutput
        #print next(tokenizedInput)
            intermediateOutput = "SDK ERROR : Next Value = " + rightSide

    return intermediateOutput

def returnStatement(tokenizedInput, value):
    # Function for return Intermediate
    intermediateStr = ''
    intermediateStr = 'RTRN ' + value
    return intermediateStr

# Function Declaration Translator
def functionDeclaration(tokenizedInput, value):
    # Eg :
    # function sampleFunction -> integer (integer param1, boolean param2){
    #       integer x:= 10, y:= 20.
    #       integer z:= x + y.
    #       return z.
    #   }
    # Input : ['function', 'sampleFunction', '->', 'integer', '(', 'integer', 'param1', ',', 'boolean', 'param2', ')', '{', 'integer', 'x', ':=', '10', ',', 'y', ':=', '20', '.', 'integer', 'z', ':=', 'x', '+', 'y', '.', 'return', 'z', '.', '}']
    # Output :
    # FUN sampleFunction INT
    # PAR INT param1
    # PAR BOOL param2
    # STRT
    # TYP INT x
    # STRTEX
    # PUSH 10
    # EQL x
    # ENDEX
    # TYP INT y
    # STRTEX
    # PUSH 20
    # EQL y
    # ENDEX
    # TYP INT z
    # STRTEX
    # PUSH x
    # PUSH y
    # ADD
    # EQL z
    # ENDEX
    # ENDFUN
    # RTRN z
    # END
    intermediateOutput = list()
    global nextElement
    global prevElement
    # Function declaration statement
    functionName = next(tokenizedInput)
    next(tokenizedInput)
    functionReturnType = next(tokenizedInput)
    intermediateOutput.append("FUN " + functionName + " " + typeNameIntermediateConvert(functionReturnType))

    # Checking Parameters
    next(tokenizedInput)
    nextValue = next(tokenizedInput)
    while nextValue in typeName and nextValue != lcrBracs:
        intermediateOutput.append("PAR " + typeNameIntermediateConvert(nextValue) + " " + next(tokenizedInput))
        next(tokenizedInput)
        nextValue = next(tokenizedInput)

    # Function Body
    intermediateOutput.append("STRT")
    nextValue = next(tokenizedInput)
    while nextValue != 'return':
        intermediateOutput.append(blockDeclaration(tokenizedInput, nextValue))
        if prevElement == '}':
            nextValue = nextElement
            prevElement = ''
            nextElement = ''
        else :
            nextValue = next(tokenizedInput)

    intermediateOutput.append("RTRN " + next(tokenizedInput))
    intermediateOutput.append("FUNEND")

    # Return Error
    nextValue = next(tokenizedInput)
    if nextValue != ".":
        intermediateOutput.append("SDK ERROR : Next Value = " + nextValue)
    return intermediateOutput

def whenCondition(tokenizedInput, value):
    intermediateAssign = ''
    nextValue = value
    condition = ''
    if value == "elseWhen":
        nextValue = next(tokenizedInput)
    while nextValue != '{':
        condition += nextValue
        nextValue = next(tokenizedInput)
    # print condition
    condition = re.sub(r'==', '@', condition)

    postfixExpr = infixToPostfixConv(removeWhiteSpace(condition))
    postfixExpr = re.sub(r'@', '==', postfixExpr)
    intermediateAssign += "STRTEX" + "\n"
    for s in postfixExpr.split():
        if isOperator(s):
            intermediateAssign += returnIntermediateOperator(s) + "\n"
        else:
            intermediateAssign += 'PUSH ' + s + "\n"
    intermediateAssign += "ENDEX"
    return intermediateAssign

# Function to translate When statement's body
def whenBody(tokenizedInput, value):
    intermediateAssign = ''
    global prevElement
    nextValue = value
    while nextValue != '}':
        # Handles Assignment Operations
        intermediateAssign += blockDeclaration(tokenizedInput, nextValue)
        nextValue = next(tokenizedInput)
    prevElement = '}'
    return intermediateAssign

# When Statement Intermediate Generator
def whenStatement(tokenizedInput, value):
    # Eg: when((a > 20) && ((a < 30) || (a <= 25))){ integer a. } elseWhen (a == b){  integer f. } else{ integer g. }
    # ['when', '(', '(', 'a', '>', '20', ')', '&&', '(', '(', 'a', '<', '30', ')', '||', '(', 'a', '<', '25', ')', ')',
    # ')', '{', 'integer', 'a', '.', '}', 'elseWhen', '(', 'a', '==', 'b', ')', '{', 'integer', 'f', '.', '}', 'else',
    # '{', 'integer', 'g', '.', '}']
    # Output :
    # WHEN
    # STRTEX
    # PUSH a
    # PUSH 2
    # PUSH a
    # PUSH 30
    # LT
    # PUSH a
    # PUSH 25
    # OR
    # AND
    # ENDEX
    # JEQ LABEL1
    # .LABEL1
    # TYPE INT a
    # WLEND1
    # STRTEX
    # PUSH a
    # PUSH b
    # EEQL
    # ENDEX
    # JEQ LABEL2
    # .LABEL2
    # TYP INT f
    # WLEND2
    # TYP INT g
    # ENDW
    global labelCounter
    global prevElement
    global nextElement
    intermediateOutput = ''
    prevElement = ''
    # When statement declaration
    intermediateOutput += "WHEN" + "\n"
    nextValue = next(tokenizedInput)
    # When Condition Check
    intermediateOutput += whenCondition(tokenizedInput, nextValue) + "\n"
    labelCounter += 1
    intermediateOutput += "JEQ LABEL" + str(labelCounter) + "\n"
    nextValue = next(tokenizedInput)
    # When Body - Label Declaration
    intermediateOutput += ".LABEL" + str(labelCounter) + "\n"
    intermediateOutput += whenBody(tokenizedInput, nextValue) + "\n"
    intermediateOutput += "LEND" + str(labelCounter) + "\n"

    # elseWhen Declaration
    nextElement = next(tokenizedInput)
    if nextElement == 'elseWhen' or nextElement == 'else':
        while nextElement == 'elseWhen':
            intermediateOutput += whenCondition(tokenizedInput, nextValue) + "\n"
            labelCounter += 1
            intermediateOutput += "JEQ LABEL" + str(labelCounter) + "\n"
            intermediateOutput += ".LABEL" + str(labelCounter) + "\n"
            nextElement = next(tokenizedInput)
            intermediateOutput += whenBody(tokenizedInput, nextValue) + "\n"
            intermediateOutput += "LEND" + str(labelCounter) + "\n"

        # else Declaration
        # Run statements till ENDW
        if nextElement == 'else':
            intermediateOutput += whenBody(tokenizedInput, nextValue) + "\n"
            nextElement = next(tokenizedInput)

    intermediateOutput += "ENDW"
    # if nextValue != "}":
    #   intermediateOutput.append("SDK ERROR : Next Value = " + nextValue)
    return intermediateOutput

# Loop Sequence Statements
def loopStatement(tokenizedInput, value):
    # Eg: loop ((a < 50) || (b >10)){ integer a. break. }
    # Input :
    # ['loop', '(', '(', 'a', '<', '50', ')', '||', '(', 'b', '>', '10', ')', ')', '{', 'integer', 'a', '.', 'break', '.', '}']
    # Output :
    # LOOP
    # STRTEX
    # PUSH a
    # PUSH 50
    # LT
    # PUSH b
    # PUSH 10
    # GT
    # OR
    # ENDEX
    # JEQ LABEL1
    # .LABEL1
    # TYP INT a
    # BREAK
    # LEND1
    # LOOP END
    global labelCounter
    intermediateOutput = list()
    buildExpr = ''
    # Loop statement declaration
    labelCounter += 1
    intermediateOutput.append(".LABEL" + str(labelCounter))
    intermediateOutput.append("LOOP")
    nextValue = next(tokenizedInput)

    # Loop Condition Check
    intermediateOutput.append(whenCondition(tokenizedInput, nextValue))
    intermediateOutput.append("CMP")

    # Loop Body Begin
    nextValue = next(tokenizedInput)
    while nextValue != '}':
        intermediateOutput.append(blockDeclaration(tokenizedInput,nextValue))
        nextValue = next(tokenizedInput)
    intermediateOutput.append("JMP LABEL" + str(labelCounter))
    intermediateOutput.append("LEND" + str(labelCounter))

    # Loop End
    intermediateOutput.append("LOOPLEND" + str(labelCounter))
    return intermediateOutput

# Function to convert Print statments
def printStatement(tokenizedInput, value):
    # Eg: print a .
    # Input :
    # ['print', 'a', '.']
    # Output :
    # STRTPRNT
    # STRTEX
    # PUSH a
    # ENDEX
    # ENDPRNT
    if value == 'print':
        value = next(tokenizedInput)
    intermediateOutput = ''
    # Print statement declaration
    intermediateOutput += "STRTPRNT\nSTRTEX\n"
    intermediateOutput += "PUSH " + value
    intermediateOutput += "\nENDEX"
    # Print end
    intermediateOutput += "\nENDPRNT"
    return intermediateOutput

# Process : Tokenized Parsed String to Assembly Conversion
def convertTokens(tokenizedInput):
    # Building an Iterator on "result" variable
    numItems = len(tokenizedInput)
    tokenizedInputIter = iter(tokenizedInput)
    tokenizedOutput = list()
    for value in tokenizedInputIter:
        if value != '.' and value != "}":
            # Scenario 1 : Variable Declaration
            if value in typeName:
                tokenizedOutput.append(varDeclaration(tokenizedInputIter, value))
            # Scenario 2 : Function Declaration
            elif value == "function":
                tokenizedOutput.append(functionDeclaration(tokenizedInputIter, value))
            # Scenario 3 : When Statement
            elif value == "when":
                tokenizedOutput.append(whenStatement(tokenizedInputIter, value).split("\n"))
            # Scenario 4 : Loop Statement
            elif value == "loop":
                tokenizedOutput.append(loopStatement(tokenizedInputIter, value))
            # Scenario 5 : Print Statement
            elif value == "print":
                tokenizedOutput.append(printStatement(tokenizedInputIter,value).split("\n"))
            else:
                nextVal = value
                rightSide = ''
                if next(tokenizedInputIter) == ':=':
                    nextVal = next(tokenizedInputIter)
                    while nextVal != eol:
                        rightSide += nextVal
                        nextVal = next(tokenizedInputIter)
                assStatement = value + " = " + rightSide
                tokenizedOutput.append(assignStatement(value, assStatement).split("\n"))
    return tokenizedOutput


def main():
    global eol
    global commaLit
    global assign
    global lsqBracs
    global rsqBracs
    global numeric
    global plus
    global minus
    global when
    global elsevar
    global typeName
    global lcrBracs
    global labelCounter
    global nextElement
    global prevElement
    labelCounter = 0

    # Parse Input
    file = open('input.txt', 'r')
    tokenizedInput = parseSDK(file.read())
    # tokenizedInput = parseSDK("integer n . function fact -> integer( integer param ) { when(param == 1) { return param. } integer parMinOne := param - 1. integer result := param * fact(parMinOne). return result. } n := fact(4).")

    # Shashank Fibo Program : integer a := 1, b := 1, counter := 0. loop (counter < 5){ integer temp := a . a := b . b := temp + b . print a . counter := counter + 1 .}
    # ['integer', 'a', ':=', '1', ',', 'b', ':=', '1', ',', 'counter', ':=', '0', '.', 'loop', '(', 'counter', '<', '5', ')', '{', 'integer', 'temp', ':=', 'a', '.', 'a', ':=', 'b', '.', 'b', ':=', 'temp', '+', 'b', '.', 'print', 'a', '.', 'counter', ':=', 'counter', '+', '1', '.', '}']

    # Kevin's Factorial Program : int n . function fact -> integer( integer param ) { when(param == 1) { return param. } integer parMinOne := param - 1. integer result := param * fact(parMinOne). return result. } n := fact(4).
    # ['integer', 'n', '.', 'function', 'fact', '->', 'integer', '(', 'integer', 'param', ')', '{', 'when', '(', 'param', '==', '1', ')', '{', 'return', 'param', '.', '}', 'integer', 'parMinOne', ':=', 'param', '-', '1', '.', 'integer', 'result', ':=', 'param', '*', 'fact', '(', 'parMinOne', ')', '.', 'return', 'result', '.', '}', 'n', ':=', 'fact', '(', '4', ')', '.']


    # when(a < 10){ integer a. } else when (a == b){  integer f. } else{ integer g. } ")
    # Input's been tokenized based on Grammar Rules
    # result = program.parseString("function factorial -> integer ( integer fact ) { \n integer factVal . \n factVal := fact * factorial ( fact - 1 ) . \n  return factVal .}")
    print tokenizedInput
    # ['function', 'sampleFunction', '->', 'integer', '(', 'integer', 'fact', ')', '{', 'integer', 'factVal', '.', 'factVal', ':=', 'fact', '*', 'factorial', '(', 'fact', '-', '1', ')', '.', 'return', 'factVal', '.', '}']
    # Sample Exception handling
    # raise Exception('Incorrect data')
    # print tokenizedInput
    # Writing TokenizedOutput to file
    writeFile(convertTokens(tokenizedInput))


if __name__ == "__main__":
    main()
    os.system('python ../Runtime/environment.py')
