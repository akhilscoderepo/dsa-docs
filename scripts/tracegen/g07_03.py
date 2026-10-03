from common import *
CH='07-prefix-sums-and-difference-arrays'
F='03-exclusion-state.md'
a=[2,3,4,5]; n=4; out=[0]*n; left=1; st=[]
for i in range(n):
    out[i]=left
    note=f"Store {left} at position {i}, the product of everything before it" + (", which is the empty product." if i==0 else ".")
    st.append({"at":{"i":i},"vars":{"stored":left,"factor":a[i]},"note":note}); left*=a[i]
assert out==[1,2,6,24] and "empty product" in st[0]["note"]
right=1; st=[]
for i in range(n-1,-1,-1):
    out[i]*=right
    st.append({"at":{"i":i},"vars":{"suffix":right,"answer":out[i]},"note":f"The rolling suffix is {right}, so position {i} becomes {out[i]}. Then the suffix absorbs {a[i]}."}); right*=a[i]
assert out==[60,40,30,24] and st[2]["vars"]["suffix"]==20 and out[1]==40
fill(CH,F,block([str(x) for x in a],["i"],st),"@@TRACE2@@")
