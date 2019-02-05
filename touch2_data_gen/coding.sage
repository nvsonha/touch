load('scalar_sol.sage')


def get_occurrence(rank, v, ind):
    print 'Running...'
    g3 = []
    b3 = []
    g_occurrence = {}     # This set counts #_occurrence of elements in good cases
    b_occurrence = {}     # This set counts #_occurrence of elements in failed cases
    C = []

    # Cannot use python dict because mutable matrix is no hashable
    for i in range(len(v)):
        g_occurrence.update({i:0})
        b_occurrence.update({i: 0})

    comb = Combinations(len(v), 3).list()
    for a in comb:
        # 1-row 3-col block: where all 3 possible messages stack together
        im = identity_matrix(2)
        c = block_matrix(3, 2, [ [im,v[a[0]]], [im,v[a[1]]], [im,v[a[2]]] ])

        if c.rank() < rank:
            b3.append(a)
            b_occurrence[a[0]] += 1
            b_occurrence[a[1]] += 1
            b_occurrence[a[2]] += 1
        else:
            g3.append(a)
            g_occurrence[a[0]] += 1
            g_occurrence[a[1]] += 1
            g_occurrence[a[2]] += 1
            C.append(c)
    return g3, b3, g_occurrence, b_occurrence, C


def get_vector(q, n, m):
    """

    :param n: number of rows
    :param m: number of cols
    :return: list of all vector of size [n x m] over F(q)
    """

    print 'q=', q, 'n=', n, 'm=', m, '\n'
    code_size = q**m

    S = ScalarSol(m, q)  # Create a Scalar object
    r = S.generate_possible_messages()  # List all codewords by vectorizing elements over GF(q)

    if len(r) == code_size:                      # Double-check my generate_possible_messages()
        print 'Number of basics: ', len(r)
    else:
        return False                        # All of my functions return Result/False
    rr = []
    for i in range(2 * code_size):               # e.g [0, 1, 2, 3] of size 4, I make [0,1,2,3,4,5,6,7]
        rr.append(i % code_size)                   # then modulo for the size, to get [0,1,2,3,0,1,2,3]

    #a = Arrangements(range(code_size), n)
    a = Arrangements(rr, n)
    print 'Permutations: ', str(len(a.list()))
    c = []
    for i in range(len(a.list())):
        temp = r[a[i][0]]
        for j in range(n-1):
            temp = block_matrix(1, 2, [temp, r[a[i][j+1]]])
        c.append(temp.transpose())          # Column Vector is transposed to Row Vector
    return c