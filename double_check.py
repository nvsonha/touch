c = load('touch2_data/matrix_2x4_q2')
g62 = load('g64_res2_23.sobj')
check = Combinations(g62,3)

print('Checking...')
for ch in check:
    im = identity_matrix(2)
    matrix = block_matrix(3,2, [ [im,c[ch[0]]], [im,c[ch[1]]], [im,c[ch[2]]] ])
    if matrix.rank() < 4:
        print('wrong somewhere')
print('Done check!')