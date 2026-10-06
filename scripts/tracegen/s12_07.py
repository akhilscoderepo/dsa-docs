from common import *
CH='12-monotonic-stacks'; FILE='07-histogram-rectangles.md'
def fmt(l): return "["+", ".join(map(str,l))+"]"
def run(H,ph,expect):
    n=len(H); st=[]; best=0; steps=[]
    for i in range(n+1):
        cur=0 if i==n else H[i]
        while st and H[st[-1]]>cur:
            t=st.pop(); w=i if not st else i-st[-1]-1; a=H[t]*w; best=max(best,a)
            who="the sentinel of height 0" if i==n else f"height {cur}"
            steps.append({"at":{"i":i},"vars":{"stack":fmt(st),"height":H[t],"width":w,"area":a,"best":best},"note":f"{who.capitalize()} is shorter than bar {t} of height {H[t]}. The width is {w}, so the area is {a}."})
        st.append(i)
        steps.append({"at":{"i":i},"vars":{"stack":fmt(st),"best":best},"note":(f"Index {i} goes on the stack." if i<n else "The scan ends with the sentinel on the stack.")})
    assert best==expect,(best,expect)
    fill(CH,FILE,block(H,["i"],steps),ph)
run([6,2,5,4,5,1,6],"@@TRACE1@@",12)
run([2,3,5,6],"@@TRACE2@@",10)
