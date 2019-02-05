gmt = load('touch2_data/gmt.sobj')

gmt_freq = [0] * 256
for g in gmt:
    gmt_freq[g[0]] += 1
    gmt_freq[g[1]] += 1
    gmt_freq[g[2]] += 1

graph = list_plot([(i,gmt_freq[i]) for i in range(len(gmt_freq))])
graph.show()
