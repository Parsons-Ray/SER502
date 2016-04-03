__author__ = 'Shashank'
import pyparsing as pp

# typeName = pp.Keyword("integer")
# identifier = pp.Word(pp.alphas,pp.alphanums)
#
# assignment = pp.Literal(":=")
# numeric = pp.Word(pp.nums)
# endChar = pp.Literal(".")
#
# declaration = typeName + identifier + pp.Optional( assignment + numeric) + pp.ZeroOrMore(pp.Literal(",") + identifier + pp.Optional( assignment + numeric )) + endChar
#
#
#
#
#
# print declaration.parseString("integer a := 10, \n b := 15, c:=20, d.")
#


eol = pp.Literal(".")
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

numericLiteral = pp.Optional(numeric) + pp.Optional(eol + numeric)
stringLiteral = pp.Word(pp.alphas, pp.alphanums)
identifier = stringLiteral
size = numericLiteral
unaryAddingOperator = pp.Or(plus ^ minus)
binaryAddingOperator = pp.Or(plus ^ minus)
multiplyingOperator = pp.Or(pp.Literal("*") ^ pp.Literal("/"))
relationalOperator = pp.Or(pp.Literal("==") ^ pp.Literal("!=") ^ pp.Literal( "<" ) ^ pp.Literal(">") ^ pp.Literal("<=") ^ pp.Literal(">="))
indexedComponent = pp.Literal("[") + (numericLiteral + pp.ZeroOrMore("," + numericLiteral) )+ pp.Literal("]")
name = pp.Or(identifier ^ indexedComponent)
primary = pp.Or(numericLiteral ^ name  ^ pp.Literal("true") ^ pp.Literal("false"))
factor = pp.Or((primary + pp.Optional(pp.Literal("^") + primary)) ^ (pp.Literal("NOT") + primary))
term = factor + pp.ZeroOrMore(multiplyingOperator + factor)
simpleExpression = pp.Optional(unaryAddingOperator) + term + pp.ZeroOrMore(binaryAddingOperator + term)
relation = simpleExpression + pp.ZeroOrMore(pp.Or(pp.Literal(",") + simpleExpression) ^ (relationalOperator + simpleExpression))
expr = relation + pp.ZeroOrMore(pp.Or((pp.Literal("AND") + relation) ^ (pp.Literal("OR") + relation)))
printStatement = pp.Literal("print") + expr
returnStatement = pp.Literal("return") + expr
typeName = pp.Or(pp.Literal("integer") ^ pp.Literal("floating") ^ pp.Literal("boolean"))
ArrayTypeDefinition = pp.Literal("Array") + typeName + pp.Literal("[") + (size + pp.ZeroOrMore(pp.Literal(",") + size))+ pp.Literal("]")
typeDefinition = pp.Or(typeName ^ ArrayTypeDefinition)
declarativeStatement = typeDefinition + identifier + pp.Optional( assign + expr) + pp.ZeroOrMore(pp.Literal(",") + identifier + pp.Optional( assign + expr)) + eol
# functionCallStatement =
assignmentStatement = identifier + pp.Optional(lsqBracs + numericLiteral + rsqBracs) + assign + expr + eol
nullStatement = pp.Literal("none")
# compoundStatement =
# DOUBT : expression = pp.Optional(lsqBracs) +  + pp.Optional(rcrBracs) + pp.Or(pp.ZeroOrMore(andExpr + relation) ^ pp.ZeroOrMore(orExpr + relation))
# Changed expression from relation ({ "AND" relation } | { "OR" relation }) | "[" relation "]" to ["["] + relation + ["]"] {"AND" relation } | { "OR" relation }
condition = expr
# DOUBT : how to refer sequenceOfStatements if defined below?
loopStatement = loop + lBracs + condition + rBracs + lcrBracs + sequenceOfStatements + rcrBracs
ifStatement = when + lBracs + condition + rBracs + lcrBracs + sequenceOfStatements + rcrBracs + pp.ZeroOrMore(elseWhen + lBracs + condition + rBracs + lcrBracs + sequenceOfStatements + rcrBracs) + pp.Optional(elsevar + lcrBracs + sequenceOfStatements + rcrBracs)
compoundStatement = pp.Or(ifStatement ^ loopStatement)
simpleStatement = pp.Or(nullStatement  ^ assignmentStatement ^ functionCallStatement ^ declarativeStatement ^ printStatement ^ returnStatement)
statement = pp.Or(simpleStatement ^ compoundStatement ^ functionSpecification)
sequenceOfStatements = pp.OneOrMore(statement)
program = sequenceOfStatements
