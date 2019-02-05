load('coding.sage')

rank = 4

file = 'm16Jan_fix'
folder = 'touch2_data/m16Jan_fix/'
f = folder+file
filename = 'matrix_2x4_q2.sobj'


def wr(t):
    o = open(f+'.txt', 'a')
    o.write(t)
    o.close()


def collect():
    vector_list = load(filename)

    ind = 0
    max_occurrence = -1
    # Continue loop until no bad3 left
    while max_occurrence != 0:
        wr('Loop %s' % ind)
        size = len(vector_list)
        wr('len(vector_list) = %s' % size)

        g3, b3, g_occurrence, b_occurrence, C = get_occurrence(rank, vector_list, ind=ind)
        max_occurrence = max(b_occurrence.values())
        save(C, f+'_good_matrix_%s' % ind)
        save(g_occurrence, f+'_good_occurrence_%s' % ind)
        save(b_occurrence, f+'_bad_occurrence_%s' % ind)
        save(g3, f+'_g3_%s' % ind)
        save(b3, f+'_b3_%s' % ind)

        s1 = set([x for x in b_occurrence if b_occurrence[x] != max_occurrence])
        s = set(range(size)).intersection(s1)
        vector_list_processed = [vector_list[i] for i in s]        # Reset message_
        wr('Reduced to: %s' % len(vector_list_processed))

        if len(vector_list_processed) == 0 and max_occurrence != 0:
            vector_list_processed = vector_list[1:]
            wr('Empty %s' % len(vector_list_processed))
        vector_list = vector_list_processed[:]
        save(vector_list_processed, f+'_processed_%s' % ind)
        ind += 1


collect()