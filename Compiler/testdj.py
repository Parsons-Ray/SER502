__author__ = 'Digant'
import pyparsing as pp


def parseSDK(input):
    # Global Variable Setting
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

    # Process : Scanner/Parser to generate Tokenized Output
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
    andExpr = pp.Keyword("AND")
    orExpr = pp.Keyword("OR")
    notExpr = pp.Keyword("NOT")
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
    relation = simpleExpression + pp.ZeroOrMore(relationalOperator + simpleExpression)
    # Changed this part due to error scenario : + pp.ZeroOrMore(pp.Or((pp.Literal(",") + simpleExpression) ^ (relationalOperator + simpleExpression)))
    expr << relation + pp.ZeroOrMore(pp.Or((pp.Literal("AND") + relation) ^ (pp.Literal("OR") + relation)))
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
        "->") + typeDefinition + lBracs + pp.Optional(
        formalParameters) + rBracs + lcrBracs + pp.ZeroOrMore(pp.Or(simpleStatement ^ compoundStatement)) + rcrBracs

    sequenceOfStatements = pp.Forward()
    ifStatement = when + lBracs + condition + rBracs + lcrBracs + pp.ZeroOrMore(
        simpleStatement) + rcrBracs + pp.ZeroOrMore(
        elseWhen + lBracs + condition + rBracs + lcrBracs + simpleStatement + rcrBracs) + pp.Optional(
        elsevar + lcrBracs + pp.ZeroOrMore(simpleStatement) + rcrBracs)
    loopStatement = loop + lBracs + condition + rBracs + lcrBracs + pp.ZeroOrMore(simpleStatement) + rcrBracs
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


# Declaration Translator
def declaration(tokenizedInput, value):
    print "Decalaration Statement \n"
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
                        intermediateOutput.append(prevValue + " EQL " + nextValue)
                        nextValue = next(tokenizedInput)
                elif nextValue == commaLit:
                    intermediateOutput.append(prevValue + " EQL NULL")
            else:
                nextValue = next(tokenizedInput)

    elif value == "floating":
        nextValue = next(tokenizedInput)
        while nextValue != ".":
            if nextValue != ",":
                intermediateOutput.append("TYP FLOAT " + nextValue)
                prevValue = nextValue
                nextValue = next(tokenizedInput)
                if nextValue == assign:
                    nextValue = next(tokenizedInput)
                    if checkFloat(nextValue):
                        intermediateOutput.append(prevValue + " EQL " + nextValue)
                        nextValue = next(tokenizedInput)
                elif nextValue == commaLit:
                    intermediateOutput.append(prevValue + " EQL NULL")
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
                        intermediateOutput.append(prevValue + " EQL " + nextValue)
                        nextValue = next(tokenizedInput)
                elif nextValue == commaLit:
                    intermediateOutput.append(prevValue + " EQL NULL")
            else:
                nextValue = next(tokenizedInput)

    # Return Error
    if nextValue != ".":
        intermediateOutput.append("SDK ERROR : Next Value = " + nextValue)
    return intermediateOutput


def convertTokens(tokenizedInput):
    # Process : Tokenized Parsed String to Assembly Conversion

    # Building an Iterator on "result" variable
    numItems = len(tokenizedInput)
    tokenizedInputIter = iter(tokenizedInput)
    tokenizedOutput = list()
    for value in tokenizedInputIter:
        # Scenario 1 : Variable Declaration
        # Eg : integer a, b := 10, c := 20.
        # Input : ['integer', 'a', ',', 'b', ':=', '10', ',', 'c', ':=', '20', '.']
        # Output :
        # TYP INT a
        # a EQL NULL
        # TYP INT b
        # b EQL 10
        # TYP INT c
        # c EQL 20
        # EOL
        if value != '.':
            if value in typeName:
                tokenizedOutput.append(declaration(tokenizedInputIter, value))

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
    # Parse Input
    tokenizedInput = parseSDK("integer a, b := 10, c := 20.")
    # Input's been tokenized based on Grammar Rules
    # result = program.parseString("function factorial -> integer ( integer fact ) { \n integer factVal . \n factVal := fact * factorial ( fact - 1 ) . \n  return factVal .}")
    # print result
    # ['function', 'factorial', '->', 'integer', '(', 'integer', 'fact', ')', '{', 'integer', 'factVal', '.', 'factVal', ':=', 'fact', '*', 'factorial', '(', 'fact', '-', '1', ')', '.', 'return', 'factVal', '.', '}']


    # Writing TokenizedOutput to file
    print convertTokens(tokenizedInput)


if __name__ == "__main__":
    main()
