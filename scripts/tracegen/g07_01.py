from common import *
CH='07-prefix-sums-and-difference-arrays'
F='01-prefix-construction.md'
a=[4,-2,5,3,-6,1]; tot=0; st=[]
for i,x in enumerate(a):
    tot+=x
    st.append({"at":{"i":i},"vars":{"amount":x,"total":tot},"note":f"Add {x} to the total, which becomes {tot}, and write it into slot {i+1}."})
assert st[4]["vars"]["total"]==4 and a[4]<0
fill(CH,F,block([str(x) for x in a],["i"],st),"@@TRACE1@@")
a=[2,-1,8,4,2,2,5]; T=sum(a); assert T==22
left=0; st=[]
for i,x in enumerate(a):
    right=T-left-x
    if left==right:
        st.append({"at":{"i":i},"vars":{"left":left,"amount":x,"right":right},"note":f"The left sum is {left}, the amount is {x}, and the right sum is {T} - {left} - {x} = {right}, so position {i} is a pivot."}); break
    st.append({"at":{"i":i},"vars":{"left":left,"amount":x,"right":right},"note":f"The left sum is {left} and the right sum is {right}, which differ, so add {x} to the left sum and move on."}); left+=x
assert i==3 and left==9 and len(st)==4
fill(CH,F,block([str(x) for x in a],["i"],st),"@@TRACE2@@")
