__author__ = 'Digant'
import pyparsing as pp
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
    actualParameter = pp.ZeroOrMore(pp.Optional(",") + pp.Or(numericLiteral ^ identifier ^ expr))
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


# Check DataTypes
def checkInt(l):
    return int(l)


def checkFloat(l):
    return float(l)


def checkBool(l):
    return bool(l)


def returnIntermediateOperator(sdkOperator):
    # Function to return Operator's Intermediate Codes
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
    elif sdkOperator == ">":
        return 'GT'
    elif sdkOperator == "<":
        return 'LT'
    elif sdkOperator == ">=":
        return 'GE'
    elif sdkOperator == "<=":
        return 'LE'
    elif sdkOperator == "==":
        return 'EEQL'
    elif sdkOperator == "!=":
        return 'NEQL'
    elif sdkOperator == "!":
        return 'NOT'


def typeNameIntermediateConvert(typeNames):
    if typeNames == "integer":
        return "INT"
    elif typeNames == "boolean":
        return "BOOL"
    elif typeNames == "floating":
        return "FLT"


def callFunctionIntermediate(callStatement):
    # Function Call to Intermediate Code
    intermediateString = callStatement.split("(")
    returnString = 'CALL ' + intermediateString[0] + '\n'
    intermediateStr = intermediateString[1].replace(")", "")
    searchObj = re.search(r',', intermediateString[1])
    if searchObj:
        rightSide = intermediateStr.split(",")
        for parameter in rightSide:
            returnString += 'PAR ' + parameter + '\n'
    elif intermediateString[1] != ')':
        # Case when only 1 parameter exist
        returnString += 'PAR ' + intermediateStr + '\n'
    return returnString


def assignStatement(assStatement):
    # Function for Assigning Statement
    # Input is an assignment statement like  a = b + c
    intermediateAssign = 'STRTEXP\n'
    searchObj = re.search(r'[a-zA-Z]+\([0-9,]*[True]*[False]*\)', assStatement)
    assStatement = re.sub(r'[a-zA-Z]+\([0-9,]*[True]*[False]*\)', '@', assStatement)
    intermediateString = assStatement.split("=")
    postfixExpr = infixToPostfixConv(removeWhiteSpace(intermediateString[1]))
    for s in postfixExpr.split():
        if isOperator(s):
            intermediateAssign += returnIntermediateOperator(s) + "\n"
        elif s == '@':
            intermediateAssign += callFunctionIntermediate(searchObj.group())
        else:
            intermediateAssign += 'PUSH ' + s + "\n"
    intermediateAssign += "EQL " + intermediateString[0] + "\n"
    intermediateAssign += 'ENDEXP'
    return intermediateAssign


# Variable Declaration Translator
def varDeclaration(tokenizedInput, value):
    # Eg : integer a, b := 10, c := 20.
    # Input : ['integer', 'a', ',', 'b', ':=', '10', ',', 'c', ':=', '20', '.']
    # Output :
    # TYP INT a
    # TYP INT b
    # STRTEXP
    # PUSH 10
    # EQL b
    # ENDEXP
    # TYP INT c
    # STRTEXP
    # PUSH 20
    # EQL c
    # ENDEXP
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
                    if checkInt(nextValue):
                        assStatement = prevValue + "=" + nextValue
                        intermediateOutput.append(assignStatement(assStatement))
                        nextValue = next(tokenizedInput)
                        # Commented section for if not initialized variable
                        # elif nextValue == commaLit or nextValue == eol:
                        # intermediateOutput.append("EQL NULL")
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
                    if checkFloat(nextValue):
                        assStatement = prevValue + "=" + nextValue
                        intermediateOutput.append(assignStatement(assStatement))
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
                    if checkBool(nextValue):
                        assStatement = prevValue + "=" + nextValue
                        intermediateOutput.append(assignStatement(assStatement))
                        nextValue = next(tokenizedInput)
            else:
                nextValue = next(tokenizedInput)
    # Return Error
    if nextValue != ".":
        intermediateOutput.append("SDK ERROR : Next Value = " + nextValue)
    return intermediateOutput


# Handling Variable or Expressions Declaration inside a Block
def blockDeclaration(tokenizedInput, value):
    intermediateOutput = ''
    nextValue = value
    if value in typeName:
        nextValue = next(tokenizedInput)
    commaFlag = 0
    # Variable Declaration or assignment
    if value in typeName:
        while nextValue != "." and nextValue != "}" and nextValue != "{":
            if commaFlag == 1:
                intermediateOutput += "\n"
            intermediateOutput += "TYP " + typeNameIntermediateConvert(value) + " " + nextValue
            prevValue = nextValue
            nextValue = next(tokenizedInput)
            # Handling Declaration
            if nextValue == ":=":
                commaFlag = 0
                rightSide = ''
                nextValue = next(tokenizedInput)
                while nextValue != "." and commaFlag == 0:
                    rightSide += nextValue
                    nextValue = next(tokenizedInput)
                    if nextValue == commaLit:
                        commaFlag = 1
                        nextValue = next(tokenizedInput)
                # Assignment Declaration
                assStatement = prevValue + "=" + rightSide
                intermediateOutput += "\n" + assignStatement(assStatement)
    elif nextValue == ":=":
        # Normal Assignment without declaration
        rightSide = ''
        nextValue = next(tokenizedInput)
        while nextValue != eol:
            rightSide += nextValue
            nextValue = next(tokenizedInput)
        assStatement = value + '=' + rightSide
        intermediateOutput += assignStatement(assStatement)
    elif nextValue == "break":
        nextValue = next(tokenizedInput)
        intermediateOutput += 'BREAK'

    # Return Error
    # if nextValue != ".":
    #   intermediateOutput = "SDK ERROR : Next Value = " + rightSide
    return intermediateOutput


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
    # STRTFUN
    # TYP INT x
    # STRTEXP
    # PUSH 10
    # EQL x
    # ENDEXP
    # TYP INT y
    # STRTEXP
    # PUSH 20
    # EQL y
    # ENDEXP
    # TYP INT z
    # STRTEXP
    # PUSH x
    # PUSH y
    # ADD
    # EQL z
    # ENDEXP
    # ENDFUN
    # RTRN z
    # END
    intermediateOutput = list()
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
    intermediateOutput.append("STRTFUN")
    nextValue = next(tokenizedInput)
    while nextValue != 'return':
        # Handles Assignment Operations
        if nextValue in typeName or nextValue != '.':
            intermediateOutput.append(blockDeclaration(tokenizedInput, nextValue))
            # else:
            # print nextValue
        nextValue = next(tokenizedInput)
    intermediateOutput.append("RTRN " + next(tokenizedInput))
    intermediateOutput.append("ENDFUN")

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
    intermediateAssign += "STRTEXP" + "\n"
    for s in postfixExpr.split():
        if isOperator(s):
            intermediateAssign += returnIntermediateOperator(s) + "\n"
        else:
            intermediateAssign += 'PUSH ' + s + "\n"
    intermediateAssign += "ENDEXP"
    return intermediateAssign

def whenBody(tokenizedInput, value):
    intermediateAssign = ''
    nextValue = value
    while nextValue != '}':
        # Handles Assignment Operations
        if nextValue in typeName and nextValue != '.':
            intermediateAssign += blockDeclaration(tokenizedInput, nextValue)
        nextValue = next(tokenizedInput)
    return intermediateAssign

# When Statement Intermediate Generator
def whenStatement(tokenizedInput, value):
    # Eg: when((a > 20) && ((a < 30) || (a <= 25))){ integer a. } elseWhen (a == b){  integer f. } else{ integer g. }
    # ['when', '(', '(', 'a', '>', '20', ')', '&&', '(', '(', 'a', '<', '30', ')', '||', '(', 'a', '<', '25', ')', ')',
    # ')', '{', 'integer', 'a', '.', '}', 'elseWhen', '(', 'a', '==', 'b', ')', '{', 'integer', 'f', '.', '}', 'else',
    # '{', 'integer', 'g', '.', '}']
    # Output :
    # WHEN
    # STRTEXP
    # PUSH a
    # PUSH 2
    # PUSH a
    # PUSH 30
    # LT
    # PUSH a
    # PUSH 25
    # OR
    # AND
    # ENDEXP
    # JEQ LABEL1
    # .LABEL1
    # TYPE INT a
    # WLEND1
    # STRTEXP
    # PUSH a
    # PUSH b
    # EEQL
    # ENDEXP
    # JEQ LABEL2
    # .LABEL2
    # TYP INT f
    # WLEND2
    # TYP INT g
    # ENDW
    global labelCounter
    intermediateOutput = list()

    # When statement declaration
    intermediateOutput.append("WHEN")
    nextValue = next(tokenizedInput)
    # When Condition Check
    intermediateOutput.append(whenCondition(tokenizedInput, nextValue))
    labelCounter += 1
    intermediateOutput.append("JEQ LABEL" + str(labelCounter))

    # When Body - Label Declaration
    intermediateOutput.append(".LABEL" + str(labelCounter))
    intermediateOutput.append(whenBody(tokenizedInput, nextValue))
    intermediateOutput.append("WLEND" + str(labelCounter))

    # elseWhen Declaration
    nextValue = next(tokenizedInput)
    while nextValue == 'elseWhen':
        intermediateOutput.append(whenCondition(tokenizedInput, nextValue))
        labelCounter += 1
        intermediateOutput.append("JEQ LABEL" + str(labelCounter))
        intermediateOutput.append(".LABEL" + str(labelCounter))
        nextValue = next(tokenizedInput)
        intermediateOutput.append(whenBody(tokenizedInput, nextValue))
        intermediateOutput.append("WLEND" + str(labelCounter))

    # else Declaration
    # Run statements till ENDW
    nextValue = next(tokenizedInput)
    intermediateOutput.append(whenBody(tokenizedInput, nextValue))
    intermediateOutput.append("ENDW")

    # print intermediateOutput
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
    # STRTEXP
    # PUSH a
    # PUSH 50
    # LT
    # PUSH b
    # PUSH 10
    # GT
    # OR
    # ENDEXP
    # JEQ LABEL1
    # .LABEL1
    # TYP INT a
    # BREAK
    # LLEND1
    # LOOP END
    global labelCounter
    intermediateOutput = list()
    buildExpr = ''
    # Loop statement declaration
    intermediateOutput.append("LOOP")
    nextValue = next(tokenizedInput)

    # Loop Condition Check
    intermediateOutput.append(whenCondition(tokenizedInput, nextValue))
    labelCounter += 1
    intermediateOutput.append("JEQ LABEL" + str(labelCounter))

    # Loop Body Begin
    intermediateOutput.append(".LABEL" + str(labelCounter))
    nextValue = next(tokenizedInput)
    while nextValue != '}':
        intermediateOutput.append(blockDeclaration(tokenizedInput,nextValue))
        nextValue = next(tokenizedInput)
    intermediateOutput.append("LLEND" + str(labelCounter))

    # Loop End
    intermediateOutput.append("LOOP END")
    return intermediateOutput


# Process : Tokenized Parsed String to Assembly Conversion
def convertTokens(tokenizedInput):
    # Building an Iterator on "result" variable
    numItems = len(tokenizedInput)
    tokenizedInputIter = iter(tokenizedInput)
    tokenizedOutput = list()
    for value in tokenizedInputIter:
        if value != '.':
            # Scenario 1 : Variable Declaration
            if value in typeName:
                tokenizedOutput.append(varDeclaration(tokenizedInputIter, value))
            # Scenario 2 : Function Declaration
            elif value == "function":
                tokenizedOutput.append(functionDeclaration(tokenizedInputIter, value))
            # Scenario 3 : When Statement
            elif value == "when":
                tokenizedOutput.append(whenStatement(tokenizedInputIter, value))
            # Scenario 4 : Loop Statement
            elif value == "loop":
                tokenizedOutput.append(loopStatement(tokenizedInputIter, value))
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
    labelCounter = 0
    # Parse Input
    tokenizedInput = parseSDK("loop ((a < 50) || (b >10)){ integer a. break. }")


    # when(a < 10){ integer a. } else when (a == b){  integer f. } else{ integer g. } ")

    # Input's been tokenized based on Grammar Rules
    # result = program.parseString("function factorial -> integer ( integer fact ) { \n integer factVal . \n factVal := fact * factorial ( fact - 1 ) . \n  return factVal .}")
    # print result
    # ['function', 'sampleFunction', '->', 'integer', '(', 'integer', 'fact', ')', '{', 'integer', 'factVal', '.', 'factVal', ':=', 'fact', '*', 'factorial', '(', 'fact', '-', '1', ')', '.', 'return', 'factVal', '.', '}']
    print tokenizedInput

    # Sample Exception handling
    # raise Exception('Incorrect data')
    # print tokenizedInput
    # Writing TokenizedOutput to file
    writeFile(convertTokens(tokenizedInput))


if __name__ == "__main__":
    main()
