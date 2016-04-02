__author__ = 'Shashank'
import pyparsing as pp

# typeName = pp.Keyword("integer")
# identifier = pp.Word(pp.alphas,pp.alphanums)
#
# assignment = pp.Literal(":=")
# numeric = pp.Word(pp.nums)
# endChar = pp.Literal(".")
#
# declaration = typeName + identifier + pp.Optional(  assignment + numeric) + pp.ZeroOrMore(pp.Literal(",") + identifier + pp.Optional( assignment + numeric )) + endChar
#
#
#
#
#
# print declaration.parseString("integer a := 10, \n b := 15, c:=20, d.")

# functionCallStatement
# assignmentStatement = pp.Or(identifier ^ indentifier + lsqBracs + numericLiteral + rsqBracs) + assign + expr + eol
# nullStatement = pp.Literal("none")
# functionSpecification =
# compoundStatement = pp.Or(ifStatement ^ loopStatement)
# simpleStatement = pp.Or(nullStatement  ^ assignmentStatement ^ functionCallStatement ^ declarativeStatement ^ printStatement ^ returnStatement)
# statement = pp.Or(simpleStatement ^ compoundStatement ^ functionSpecification)
# sequenceOfStatements = pp.OneOrMore(statement)
# program = sequenceOfStatements

