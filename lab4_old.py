from math import pi

def count_evens(L):
    '''
    Problem 1
    Count even integers in list L.
    '''
    evens = 0
    for i in L:
        if i % 2 == 0:
            evens+=1
    return evens

def list_to_str(L):
    '''
    Problem 2
    Convert a list L to a string representation without str().
    i.e. [1, 2, 3]
    '''
    
    #List start
    s = "["
    #Items 0 to len-1 (with separator)
    for i in range(0,len(L)-1):
        s += str(L[i])
        s += ', '
    #Final item (no separator)
    s+= str(L[-1])
    s+= "]"
    return s

def lists_are_the_same(list1, list2):
    '''
    Problem 3
    Compare two lists list1 and list2 without ==.
    True iff lists contain equivalent elements in the same order.
    '''
    for i in range(0, len(list1)):
        if(list1[i] is not list2[i]):
            return False
    return True

# steps = 0
def simplify_fraction(n, m):
    '''
    Problem 4
    Simplify a fraction n/m. Returns a 2-tuple (n',m')
    '''
    #Divisor cannot be 1 (short circuit) or larger than the smaller of the denominator or numerator (inclusive)
    for div in range(2, max(n,m)):
        if(n % div == 0 and m % div == 0):
            n = int(n/div)
            m = int(m/div)
            print("{}: {}/{}".format(div,n,m))
    return (n,m)

def leibniz(n):
    '''
    Problem 5 a)
    Compute an approximation for π using the Leibniz formula for 'n' steps.
    '''
    total = 0
    for k in range(n):
        total += 4*((-1)**k)/(2*k+1)
        # print("{}: {}".format(k, 4*total))
    return total

#Truncates float 'i' to 'n' digits
def truncate(i, n):
    return int(i*10**n)/10**n

def accuracy(lpi):
    '''
    Problem 5 b)
    Compute the number of digits of accuracy of 'lpi' as an approximation for π.
    '''
    n = 0
    while(True):
        npi = truncate(pi, n)
        nlpi = truncate(lpi, n)
        if(npi == nlpi):
            n+=1
        else:
            return n

def toAccuracy(target):
    '''
    Problem 5 c)
    Iterates the Leibniz summation for π until the approximation is accurate to 'target' digits.
    '''
    k=0
    lpi = 4
    acc = 0
    while(acc < target):
        k+=1
        lpi += 4*((-1)**k)/(2*k+1)
        acc = accuracy(lpi)
    return k

def toAccuracyFaster(target):
    '''
    Same as 5 c), but faster.
    '''
    k=10**(target-1) #Leibniz steps
    lpi = leibniz(k) #Let's get like 10^target-1 out of the way
    acc = accuracy(lpi)
    while(acc < target):
        lpi += 4*((-1)**k)/(2*k+1)
        k+=1
        acc = accuracy(lpi)
    return k
        
        
#Problem 6
# esteps = 0
def euclid(a,b):
    # global esteps
    if(a%b==0):
        # result = (b,esteps)
        # esteps = 0
        # return result
        return b
    # esteps += 1
    return euclid(b,a%b)

#Testing
lis = [1,2,3,4,5,6]
print("P1: There are {} even numbers in {}.".format(count_evens(lis), lis))
print("P2: {}.".format(list_to_str(lis)))
print("P3 (T1): {} == {}? {}".format(lis, lis, lists_are_the_same(lis, lis)))
lis2 = [2,2,3,9,5,6]
print("P3 (T2): {} == {}? {}".format(lis, lis2, lists_are_the_same(lis, lis2)))

fraction = (2322,654)
simp = simplify_fraction(*fraction) #3/13 * [3,3,3,5,17]
print("Problem 4 (1): {}/{} simplifies to {}/{}.".format(*fraction, *simp))
esimp = euclid(*fraction)
print("Problem 4 (2): \na) GCF of {} and {}: {}.".format(*fraction, *esimp))
print("b) {}/{} simplifies to {}/{}".format(*fraction, *[int(x/esimp[0]) for x in fraction]))

# lpi = leibniz(100000)

# Uncomment for continuous Leibniz step-accuracy generation
# n=1
# while True:
#     print(toAccuracyFaster(n))
#     n+=1 