import os
from time import sleep
history = [0]
currentValue = lambda : history[-1]
memory = 0

#Increments the current value by some number
def add(to_add):
    global history
    history.append(currentValue() + to_add)
    
#Decrements the current value by some number
def subtract(to_sub):
    add(-to_sub)

#Multiplies the current value by some factor
def multiply(factor):
    global history
    history.append(currentValue() * factor)

#Divides the current value by some divisor
def divide(divisor):
    global history
    if divisor == 0:
        print("Error: The divisor cannot be 0.")
    else:
        history.append(currentValue() / divisor)
        
def exponent(ex):
    global history
    history.append(currentValue() ** ex)

def setvalue(val):
    global history
    history.append(val)
    
operators = {
    '+' : add,
    '-' : subtract,
    '/' : divide,
    '*' : multiply,
    '=' : setvalue,
    '^' : exponent
}

#Saves the current value to memory
def memory():
    global memory
    memory = currentValue()
    print("{} saved to memory!".format(memory))

#Recalls the value stored in memory to the current value
def recall():
    global history
    global memory
    history.append(memory)
    print("{} recalled from memory!".format(currentValue()))

def undo():
    global history
    history.pop()

def clear():
    setvalue(0)
    
#Operand-less
special = {
    'm' : memory,
    'r' : recall,
    'u' : undo,
    'c' : clear
}

if __name__ == "__main__":
    print("Welcome to the calculator program.")
    while(True):
        os.system('clear')
        print('>>{}\n'.format(currentValue()))
        operation = input('>').replace(" ", "").lower()
        operator = operation[0:1]
        if(operator in special.keys()):
            special[operator]()
        elif(operator in operators.keys()):
            #No operand defaults to zero
            operand = float(operation[1:]) if (operation.__len__() > 1) else 0
            operators[operator](operand)
        else:
            print('Invalid operator: {}'.format(operator))
            sleep(2)