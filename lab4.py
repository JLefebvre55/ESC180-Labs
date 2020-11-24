from math import pi
from time import sleep

#Problem 1 - Count even integers in list
def count_evens(L):
    count = 0
    for i in L:
        if i % 2 == 0:
            count+=1
    return count

#Problem 2 - List to string without str(list)
def list_to_str(lis, separator=', '):
    #List start
    s = "["
    #Items 0 to len-1 (with separator)
    for i in range(0,len(lis)-1):
        s += str(lis[i])
        s += separator
    #Final item (no separator)
    s+= str(lis[-1])
    s+= "]"
    return s

#Problem 3 - List comparison without list1 == list2 (instead by element)
def lists_are_the_same(list1, list2):
    if len(list1) != len(list2):
        return False
    for i in range(0, len(list1)):
        if(list1[i] is not list2[i]):
            return False
    return True

#Problem 4 - Sexy recursive GCF
steps = 0
def simplify_fraction(n, m, start=2):
    global steps
    start = min(start,2)
    #Divisor cannot be 1 (short circuit) or larger than the smaller of the denominator or numerator (inclusive)
    for div in range(start, min(n,m)+1):
        if(n % div == 0 and m % div == 0):
            n = int(n/div)
            m = int(m/div)
            # print("{}: {}/{}".format(div,n,m))
            return simplify_fraction(n,m,div)
        steps+=1
    result = (n,m,steps)
    steps = 0
    return result

#Problem 5 - Leibniz formula for π
def leibniz(n):
    total = 0
    for k in range(n):
        total += 4*((-1)**k)/(2*k+1)
        # print("{}: {}".format(k, 4*total))
    return total

#Truncates float i to n digits
def truncate(i, n):
    return int(i*10**n)/10**n

#How many digits of π is a number accurate to?
def accuracy(lpi):
    n = 0
    while(True):
        npi = truncate(pi, n)
        nlpi = truncate(lpi, n)
        if(npi == nlpi):
            n+=1
        else:
            return n

#How many iterations of the Leibniz summation for π does it take for the approximation to be accurate to some number of digits?
def toAccuracy(target):
    k=0
    lpi = 4
    acc = 0
    while(acc < target):
        k+=1
        lpi += 4*((-1)**k)/(2*k+1)
        acc = accuracy(lpi)
    return k

#Same as above, skips the first 10^(n-1) iterations
def toAccuracyFaster(target):
    k=10**(target-1) #Leibniz steps
    lpi = leibniz(k) #Let's get like 10^target-1 out of the way
    acc = accuracy(lpi)
    while(acc < target):
        lpi += 4*((-1)**k)/(2*k+1)
        k+=1
        acc = accuracy(lpi)
    return k
        
        
#Problem 6
esteps = 0
def euclid(a,b):
    global esteps
    if(a%b==0):
        result = (b,esteps)
        esteps = 0
        return result
    esteps += 1
    return euclid(b,a%b)

if __name__ == "__main__":
    #Testing
    lis = [1,2,3,4,5,6]
    print("Problem 1: There are {} even numbers in {}.".format(count_evens(lis), lis))
    print("Problem 2: {}.".format(list_to_str(lis)))
    print("Problem 3 (1): {} == {}? {}".format(lis, lis, lists_are_the_same(lis, lis)))
    lis2 = [2,2,3,9,5,6]
    print("Problem 3 (2): {} == {}? {}".format(lis, lis2, lists_are_the_same(lis, lis2)))

    fraction = (2322,654)
    simp = simplify_fraction(*fraction) #3/13 * [3,3,3,5,17]
    print("Problem 4 (1): {}/{} simplifies to {}/{} in {} steps using a recursive method.".format(*fraction, *simp))
    esimp = euclid(*fraction)
    
    print("Leibniz approx takes {} steps".format(toAccuracy(5)))
    
    print("Problem 6 (2): \na) GCF of {} and {}: {} in {} steps using Euclid's algorithm.".format(*fraction, *esimp))
    print("b) {}/{} simplifies to {}/{}".format(*fraction, *[int(x/esimp[0]) for x in fraction]))

# Uncomment for continuous Leibniz step-accuracy generation
# n=1
# while True:
#     print(toAccuracyFaster(n))
#     n+=1 