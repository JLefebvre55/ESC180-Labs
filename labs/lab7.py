import numpy

def get_lead_ind(row):
    for entry in range(len(row)):
        if row[entry] != 0:
            return entry
    return len(row)

def get_row_to_swap(M, start_i):
    leftmost = start_i
    howleft = get_lead_ind(M[start_i])
    for row in range(start_i+1, len(M)):
        if(get_lead_ind(M[row])<howleft):
            howleft = get_lead_ind(M[row])
            leftmost = row
    return leftmost

def add_rows_coefs(r1, c1, r2, c2):
    result = [0]*len(r1)
    #r1*c1 + r2*c2
    for i in range(len(result)):
        # if(i < len(r1)):
            result[i] += c1*r1[i]
        # if(i < len(r2)):
            result[i] += c2*r2[i]
    return result

def eliminate(M, row_to_sub, best_lead_ind):
    for row in range(row_to_sub+1, len(M)):
        if(M[row][best_lead_ind] != 0):
            coeff = M[row][get_lead_ind(M[row])] / M[row_to_sub][get_lead_ind(M[row_to_sub])]
            for item in range(best_lead_ind, len(M[row])):
                M[row][item] -= coeff*M[row_to_sub][item]

def forward_step(M):
    for row in range(len(M)):
        swap = get_row_to_swap(M, row)
        r = M[row]
        M[row] = M[swap]
        M[swap] = r
        eliminate(M, row, get_lead_ind(M[row]))

M = [[5, 6, 7, 8],
[0,0, 1, 1],
[0, 0, 5, 2],
[0, 0, 7, 0]]

# M = [[5, 6, 7, 8],
# [0, 0, 0, 1],
# [0, 0, 5, 2],
# [0, 1, 0, 0]]

forward_step(M)

print(numpy.array(M))