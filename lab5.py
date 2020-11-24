def list1_start_with_list2(list1, list2):
    '''
    Problem 1
    Does list1 start with list2?
    '''
    if(len(list1) < len(list2)):
        return False
    else:
        for c in range(len(list2)):
            if(list1[c]!=list2[c]):
                return False
        return True

def match_pattern(list1, list2):
    '''
    Problem 2
    Are there any matched patterns of list2 in list1?
    '''
    if(len(list2)>len(list1)):
        return False
    for i in range(0,len(list1)-len(list2)):
        if list1_start_with_list2(list1[i:len(list2)+i],list2):
            return True
    return False

def repeats(list0):
    '''
    Problem 3
    Are there any repeats in list list0?
    '''
    for i in range(len(list0)-1):
        if(list0[i] == list0[i+1]):
            return True
    return False

def dimensions(M):
    '''
    Problem 4a
    Get a dimension-string of any 2D matrix M.
    '''
    if isinstance(M, list) and isinstance(M[0], list):
        return [len(M),len(M[0])]
    else:
        return None

def dimensions_better(M):
    '''
    Problem 4a - Extended
    Get a dimension-string of any matrix M.
    '''
    if isinstance(M, list):
        # print(len(M))
        rest = dimensions_better(M[0])
        # print(rest)
        if(rest == None):
            return [len(M),]
        else:
            return [len(M),]+rest
    else:
        return None
        
def print_matrix_dim(M):
    l = []
    for d in dimensions(M):
        l.append(str(d))
    print('x'.join(l))
    
def print_matrix_dim_better(M):
    l = []
    for d in dimensions_better(M):
        l.append(str(d))
    print('x'.join(l))
    
def mult_M_v(M, v):
    '''
    Problem 4b
    Multiply a matrix by a vector
    '''
    if(len(v) != len(M[0])):
        return
    product = []
    for row in M:
        s = 0
        for i in range(len(row)):
            s += row[i]*v[i]
        product.append(s)
    return product

def mult_M_M(M1,M2):
    '''
    Problem 4c
    Multiply a matrix M1 by a matrix M2
    '''
    if(len(M1) != len(M2[0])):
        return
    result = []
    for row in range(len(M1)):
        for col in range(len(M2[0])):
            for i in range(len(M1[0])):
                result[row][i] += M1[row][col]*M2[col][row]
        result.append(l)
    return result



#len(A[0]) == len(B)
#a in range(len(A))
#b in range(len(B[0]))
'''
def matrix_mult(A, B):
    # input: list of numerial A, list of numerical B
    # output: list of numericals L
    # note: takes matrix A and multiples matrix B, returning produt L,
    #       returns error string if not possible
    # ASSUMES non empty arrays provided
    

    if len(A[0])!=len(B):
        return "cannot complete"
    L = [] # return list L
    
    for i in range(len(A)):
        L.append([]) #adding empty rows
        for j in range(len(B[0])):
            L[i].append(0) #adding zeros for columns
            
            
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(A[0])): #index k to iterate for elements
                L[i][j] += A[i][k]*B[k][j]
    return L
'''

#Testing
list1 = [1,2,3]
list2 = [1,2]
list3 = [0,5,2,1,2,6]
list4 = [1,7,5,9,2,2]

matrix4d = [[[[1,7,5,9,2,2],[1,7,5,9,2,2]],
            [[1,7,5,9,2,2],[1,7,5,9,2,2]],
            [[1,7,5,9,2,2],[1,7,5,9,2,2]]],
            [[[1,7,5,9,2,2],[1,7,5,9,2,2]],
            [[1,7,5,9,2,2],[1,7,5,9,2,2]],
            [[1,7,5,9,2,2],[1,7,5,9,2,2]]],
            [[[1,7,5,9,2,2],[1,7,5,9,2,2]],
            [[1,7,5,9,2,2],[1,7,5,9,2,2]],
            [[1,7,5,9,2,2],[1,7,5,9,2,2]]]]

matrix2d = [[1,2,3,4],
            [5,6,7,8]]

vector = [4,5,7,3]

MA = [[1,2],[3,4],[5,6]]
MB = [[2,6,8],[2,3,7]]

if __name__ == "__main__":
    print("\nProblem 1-1: {} starts with {}? {}.".format(list1,list2,list1_start_with_list2(list1, list2)))
    print("Problem 1-2: {} starts with {}? {}.\n".format(list4,list2,list1_start_with_list2(list4, list2)))
    print("Problem 2-1: {} pattern exists in {}? {}.".format(list2, list3, match_pattern(list3,list2)))
    print("Problem 2-2: {} pattern exists in {}? {}.\n".format(list1, list3, match_pattern(list3,list1)))
    print("Problem 3-1: {} contains a repeat? {}.".format(list4,repeats(list4)))
    print("Problem 3-2: {} contains a repeat? {}.\n".format(list3,repeats(list3)))
    print("Problem 4a-1: {} or ".format(dimensions(matrix2d)), end='')
    print_matrix_dim(matrix2d)
    print("Problem 4a-2: {} or ".format(dimensions_better(matrix4d)), end='')
    print_matrix_dim_better(matrix4d)
    print("Problem 4b: {} * {} = {}.\n".format(matrix2d, vector, mult_M_v(matrix2d, vector)))
    print("Problem 4c: {} * {} = {}.".format(MB, MA, mult_M_M(MB, MA)))