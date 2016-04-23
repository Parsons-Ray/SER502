__author__ = 'Digant'
# File for InfixToPostfix Conversion


def isOperand(sdkOperand):
    # Function to check if the sdkOperand is an Operand
    if not (isOperator(sdkOperand)) and (sdkOperand != "(") and (sdkOperand != ")"):
        return 1
    return 0


def isOperator(sdkOperator):
    # Function to check if the sdkOperator is an Operator
    if sdkOperator == "+" or sdkOperator == "-" or sdkOperator == "*" or sdkOperator == "/" or sdkOperator == "^" or \
                    sdkOperator == "=" or sdkOperator == "&&" or sdkOperator == "||":
        return 1
    return 0


def isStackEmpty(stack):
    # Function to check if the Stack is empty
    if len(stack) == 0:
        return 1
    return 0

def strToTokens(inputString):
    # Function to convert String to Tokens
    strArr = inputString
    temporaryString = ''
    tokens = []
    tokensIndex = 0
    counter = 0
    for val in strArr:
        counter += 1
        if isOperand(val):
            temporaryString += val
        if isOperator(val) or val == ")" or val == "(":
            if temporaryString != "":
                tokens.append(temporaryString)
                tokensIndex += 1
            temporaryString = ''
            tokens.append(val)
            tokensIndex += 1
        if counter == len(strArr):
            if temporaryString != '':
                tokens.append(temporaryString)
    return (tokens)


def pushStack(stack, element):
    # Function to push element into Stack
    stack.append(element)


def popStack(stack):
    # Function to pop element out of Stack
    return stack.pop()


def topStack(stack):
    # Function to return top element from Stack
    return stack[len(stack) - 1]


def precedence(operator):
    # Function to decide Precedence of the Operator
    if operator == "&&":
        return (8)
    if operator == "||":
        return (7)
    if operator == "^":
        return (6)
    if (operator == "*") or (operator == "/"):
        return (5)
    if (operator == "+") or (operator == "-"):
        return (4)
    if operator == "(":
        return (3)
    if operator == ")":
        return (2)
    if operator == "=":
        return (1)


def infixToPostfixConv(infixStr, postfixStr=[], retType=0):
    # Function to convert infixToPostfix
    postfixStr = []
    stack = []
    postfixPtr = 0
    returnVal = ''
    temporaryString = infixStr
    infixStr = []
    infixStr = strToTokens(temporaryString)
    for value in infixStr:
        if isOperand(value):
            postfixStr.append(value)
            postfixPtr += 1
        if isOperator(value):
            if value != "^":
                while (not (isStackEmpty(stack))) and (precedence(value) <= precedence(topStack(stack))):
                    postfixStr.append(topStack(stack))
                    popStack(stack)
                    postfixPtr += 1
            else:
                while (not (isStackEmpty(stack))) and (precedence(value) < precedence(topStack(stack))):
                    postfixStr.append(topStack(stack))
                    popStack(stack)
                    postfixPtr += 1
            pushStack(stack, value)
        if value == "(":
            pushStack(stack, value)
        if value == ")":
            while topStack(stack) != "(":
                postfixStr.append(popStack(stack))
                postfixPtr += 1
            popStack(stack)

    while not (isStackEmpty(stack)):
        if topStack(stack) == "(":
            popStack(stack)
        else:
            postfixStr.append(popStack(stack))

    for value in postfixStr:
        # Added space to easily split later the operands & arguments
        returnVal += " " + value

    if retType == 0:
        return returnVal
    else:
        return postfixStr
