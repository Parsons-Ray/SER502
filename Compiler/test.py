__author__ = 'Shashank'
import pyparsing as pp

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
numericLiteral = pp.Optional(numeric) + pp.Optional(eol + numeric)
stringLiteral = pp.Word(pp.alphas, pp.alphanums)
identifier = stringLiteral
size = numericLiteral
unaryAddingOperator = pp.Or(plus ^ minus)
binaryAddingOperator = pp.Or(plus ^ minus)
relationalOperator = pp.Or(pp.Literal("==") ^ pp.Literal("!=") ^ pp.Literal( "<" ) ^ pp.Literal(">") ^ pp.Literal("<=") ^ pp.Literal(">="))
multiplyingOperator = pp.Or(pp.Literal("*") ^ pp.Literal("/"))

def primary():
    return pp.Or(numericLiteral ^ stringLiteral ^ pp.Literal("true") ^ pp.Literal("false"))

def factor():
    return pp.Or((primary() + pp.Optional(pp.Literal("^") + primary())) ^ (notExpr + primary()))

def term():
    return factor() + pp.ZeroOrMore(multiplyingOperator + factor())

def simpleExpression():
    return pp.Optional(unaryAddingOperator) + term() + pp.ZeroOrMore(binaryAddingOperator + term())

def relation():
    return simpleExpression() + pp.ZeroOrMore(pp.Or(pp.Literal(",") + simpleExpression()) ^ (relationalOperator + simpleExpression()))


def expr():
    return relation() + pp.ZeroOrMore(pp.Or((pp.Literal("AND") + relation()) ^ (pp.Literal("OR") + relation())))

def indexedComponent():
    return pp.Literal("[") + (expr() + pp.ZeroOrMore("," + expr()) )+ pp.Literal("]")


def name():
    return pp.Or(identifier ^ indexedComponent())




condition = expr()
typeName = pp.Or(pp.Literal("integer") ^ pp.Literal("floating") ^ pp.Literal("boolean"))
ArrayTypeDefinition = pp.Literal("Array") + typeName + pp.Literal("[") + (size + pp.ZeroOrMore(pp.Literal(",") + size))+ pp.Literal("]")
typeDefinition = pp.Or(typeName ^ ArrayTypeDefinition)
actualParameter =  pp.Or(numericLiteral ^ identifier)
formalParameters = typeDefinition + identifier + pp.ZeroOrMore(commaLit + typeDefinition + identifier)
returnStatement = pp.Literal("return") + expr()

printStatement = pp.Literal("print") + expr()

declarativeStatement = typeDefinition + identifier + pp.Optional( assign + expr()) + pp.ZeroOrMore(pp.Literal(",") + identifier + pp.Optional( assign + expr())) + eol

functionCallStatement = identifier + rBracs + actualParameter + lBracs + eol

assignmentStatement = identifier + pp.Optional(lsqBracs + numericLiteral + rsqBracs) + assign + expr() + eol

nullStatement = pp.Literal("none")

def simpleStatement():
    return pp.Or(nullStatement  ^ assignmentStatement ^ functionCallStatement ^ declarativeStatement ^ printStatement ^ returnStatement)

def functionSpecification():
    return pp.Keyword("function") +  identifier + pp.Literal("->") + typeDefinition + lBracs + pp.Optional(formalParameters) + rBracs + lcrBracs + pp.ZeroOrMore(pp.Or(simpleStatement() ^ compoundStatement()
    )) + rcrBracs


def loopStatement():
    return loop + lBracs + condition + rBracs + lcrBracs + pp.ZeroOrMore(simpleStatement()) + rcrBracs


def ifStatement():
   return when + lBracs + condition + rBracs + lcrBracs + pp.ZeroOrMore(simpleStatement()) + rcrBracs + pp.ZeroOrMore(elseWhen + lBracs + condition + rBracs + lcrBracs + simpleStatement() + rcrBracs) + pp.Optional(elsevar + lcrBracs + pp.ZeroOrMore(simpleStatement()) + rcrBracs)



def compoundStatement():
    return pp.Or(loopStatement() ^ ifStatement())


def statement():
    return pp.Or(simpleStatement()  ^ functionSpecification() ^ compoundStatement())


def sequenceOfStatements():
    return pp.ZeroOrMore(statement())

def program():
    return pp.ZeroOrMore(statement())











def main():
    # x = program().validate()
    x = program().parseString("function factorial -> integer ( integer fact ) { \n	integer factVal . \n factVal := fact * factorial ( fact -1 ). \n return factVal.}")
    print x
if __name__ == "__main__":
    main()