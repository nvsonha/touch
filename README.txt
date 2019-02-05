-----------------------------------------------------------------------
Explanation of results:

g63_res1_12.obj:
+ 63 indexes/elements
+ In 'test_state.py', under State_LoadData, we run only:
# '[1, 2]': 3

g63_res2_12.obj:
# '[1, 2]': 3
# '[1, 3]': 2

g64_res1_23.obj:
# '[2, 3]': 1

g64_res2_23.obj:
# '[2, 3]': 1
# '[1, 2]': 3

-----------------------------------------------------------------------
Current way
Sage 8.4:
sage test_handler.py

Sage 7.5:
Rename all '.py' files into '.sage' files
sage test_handler.sage

Saving results:
len(h._sm.state2.sub_rel.keys())

-----------------------------------------------------------------------
Old way
1) Load data (a list of all lists of 3 good-relative elements)
Example: 
>>> g3 = load('touch2_data/m16Jan_fix_g3_0.sobj')
m16Jan_fix_g3_0 is created by running coding.sage under touch2_data_gen

2)Uncomment "h=main(g3)" in test_handler.py