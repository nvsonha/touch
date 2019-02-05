rel_wid_1 = load('touch2_data/RelOfPair_wid_1.sobj')

graph1 = list_plot([(i,len(rel_wid_1[x])) for i,x in zip(range(len(rel_wid_1)), rel_wid_1.keys())])
graph1.show()
