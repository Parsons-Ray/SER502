__author__ = 'Digant'
# File for InfixToPostfix Conversion
def isOperand(sdkOperator):
    if not (isOperator(sdkOperator)) and (sdkOperator != "(") and (sdkOperator != ")"):
        return 1
    return 0


def isOperator(sdkOperator):
    if sdkOperator == "+" or sdkOperator == "-" or sdkOperator == "*" or sdkOperator == "/" or sdkOperator == "^":
        return 1
    return 0


def isEmpty(stackArr):
    if len(stackArr) == 0:
        return 1
    return 0


def strToTokens(inputString):
    # Function to convert String to Tokens
    strArr = inputString
    temporaryString = ''
    tokens = []
    tokensIndex = 0
    count = 0
    for val in strArr:
        count += 1
        if isOperand(val):
            temporaryString += val
        if isOperator(val) or val == ")" or val == "(":
            if temporaryString != "":
                tokens.append(temporaryString)
                tokensIndex += 1
            temporaryString = ''
            tokens.append(val)
            tokensIndex += 1
        if count == len(strArr):
            if temporaryString != '':
                tokens.append(temporaryString)
    return (tokens)


def pushStack(stack, element):
    stack.append(element)


def popStack(stack):
    return stack.pop()


def topStack(stack):
    return (stack[len(stack) - 1])


def precedence(operator):
    if operator == "^":
        return (5)
    if (operator == "*") or (operator == "/"):
        return (4)
    if (operator == "+") or (operator == "-"):
        return (3)
    if operator == "(":
        return (2)
    if operator == ")":
        return (1)


def infixToPostfixConv(infixStr, postfixStr=[], retType=0):
    postfixStr = []
    stack = []
    postfixPtr = 0
    temporaryString = infixStr
    infixStr = []
    infixStr = strToTokens(temporaryString)
    for value in infixStr:
        if isOperand(value):
            postfixStr.append(value)
            postfixPtr = postfixPtr + 1
        if isOperator(value):
            if value != "^":
                while (not (isEmpty(stack))) and (precedence(value) <= precedence(topStack(stack))):
                    postfixStr.append(topStack(stack))
                    popStack(stack)
                    postfixPtr += 1
            else:
                while (not (isEmpty(stack))) and (precedence(value) < precedence(topStack(stack))):
                    postfixStr.append(topStack(stack))
                    popStack(stack)
                    postfixPtr += 1
            pushStack(stack, value)
        if value == "(":
            pushStack(stack, value)
        if value == ")":
            while (topStack(stack) != "("):
                postfixStr.append(popStack(stack))
                postfixPtr = postfixPtr + 1
            popStack(stack)

    while not (isEmpty(stack)):
        if topStack(stack) == "(":
            popStack(stack)
        else:
            postfixStr.append(popStack(stack))

    returnVal = ''
    for value in postfixStr:
        returnVal += value

    if retType == 0:
        return returnVal
    else:
        return postfixStr
