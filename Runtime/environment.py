#Classes we will need
class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)

class Queue:
    def __init__(self, values):
        self.items = values

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def peek(self):
        return self.items[-1]

#Globals

#highlevel code looks like:
    #integer a, b := 10.
tokens = Queue(["TYP", "VAR", "a", "b", "EQL", "10", "EOL"][::-1])#reverse for the queue
varDict = {}#this contains all our variables and their values
stack = Stack()

def TYP():
    stack.push(tokens.dequeue()) #pushes "VAR" onto stack
    while tokens.peek() is not "EQL": #push all the identifiers onto the stack
        stack.push(tokens.dequeue())
    tokens.dequeue()#remove "EQL"
    value = tokens.dequeue() #this is "10" in our sample case.

    while stack.peek() is not "VAR": #pop off all the variable identifiers and assign their value.
        varDict[stack.pop()] = value
    stack.pop() #pop off "VAR"
    tokens.dequeue() #dequeue "EOL"

def main():
    nextToken = tokens.dequeue()
    if nextToken is "TYP":
        TYP()
    print(varDict)

#Call the main method. Starts runtime.
main()
