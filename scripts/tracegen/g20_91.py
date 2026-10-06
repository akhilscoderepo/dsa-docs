from common import *
CH='20-greedy'; F='91-sort-then-commit-greedily.md'
s="abacbdeffed"; last={c:i for i,c in enumerate(s)}
assert last['a']==2 and last['b']==4 and last['c']==3 and last['d']==10 and last['e']==9 and last['f']==8
st=[]; start=0; end=0; sizes=[]
for i,c in enumerate(s):
    end=max(end,last[c]); note=f"The letter {c} ends at {last[c]}, so end is {end}."
    if i==end:
        sizes.append(i-start+1); note+=f" The index equals end, so the scan cuts a part of length {i-start+1}."; start=i+1
    st.append({"at":{"i":i},"vars":{"end":end,"cuts":len(sizes)},"note":note})
assert sizes==[5,6]
fill(CH,F,block(list(s),["i"],st),"@@TRACE1@@")
iv=sorted([(1,3),(2,4),(4,6),(5,8),(7,9)],key=lambda x:x[1]); gap=1; last_end=None; st=[]; acc=0
for i,(a,b) in enumerate(iv):
    if last_end is None or a>=last_end+gap:
        acc+=1; note=f"The start {a} is at least the needed bound, so the scan keeps [{a},{b}) and sets lastEnd to {b}."; last_end=b
    else: note=f"The start {a} is below lastEnd + 1 = {last_end+gap}, so the scan removes [{a},{b})."
    st.append({"at":{"i":i},"vars":{"kept":acc,"removed":i+1-acc},"note":note})
assert acc==3
fill(CH,F,block([f"{a}-{b}" for a,b in iv],["i"],st),"@@TRACE2@@")
