__author__ = 'Digant'
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
relation = simpleExpression + pp.ZeroOrMore(
    pp.Or(pp.Literal(",") + simpleExpression ^ relationalOperator + simpleExpression))
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

declarativeStatement = typeDefinition + identifier + pp.Optional(assign + expr) + pp.ZeroOrMore(
    pp.Literal(",") + identifier + pp.Optional(assign + expr)) + eol

assignmentStatement = identifier + pp.Optional(lsqBracs + numericLiteral + rsqBracs) + assign + expr + eol

nullStatement = pp.Literal("none")

functionSpecification = pp.Keyword("function") + identifier + pp.Literal("->") + typeDefinition + lBracs + pp.Optional(
    formalParameters) + rBracs + lcrBracs + pp.ZeroOrMore(pp.Or(simpleStatement ^ compoundStatement)) + rcrBracs

sequenceOfStatements = pp.Forward()
ifStatement = when + lBracs + condition + rBracs + lcrBracs + pp.ZeroOrMore(simpleStatement) + rcrBracs + pp.ZeroOrMore(
    elseWhen + lBracs + condition + rBracs + lcrBracs + simpleStatement + rcrBracs) + pp.Optional(
    elsevar + lcrBracs + pp.ZeroOrMore(simpleStatement) + rcrBracs)
loopStatement = loop + lBracs + condition + rBracs + lcrBracs + pp.ZeroOrMore(simpleStatement) + rcrBracs
compoundStatement << pp.Or(loopStatement ^ ifStatement)
simpleStatement << pp.Or(nullStatement ^ assignmentStatement ^ functionCallStatement ^ declarativeStatement ^
                         printStatement ^ returnStatement)
statement = pp.Or(simpleStatement ^ functionSpecification ^ compoundStatement)
sequenceOfStatements << pp.OneOrMore(statement)
program = sequenceOfStatements

result = program.parseString("function factorial -> integer ( integer fact ) { \n integer factVal . \n factVal := fact * factorial ( fact - 1 ) . \n  return factVal .}")
print result
