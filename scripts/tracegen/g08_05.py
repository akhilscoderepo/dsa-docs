from common import *
CH='08-two-pointers'; F='05-duplicate-skipping.md'
def t1():
    a=[1,1,2,3,3,4,5]; T=6; l,r=0,6; st=[]; out=[]
    while l<r:
        s=a[l]+a[r]; v={"sum":str(s),"pairs":str(out)}
        at={"left":l,"right":r}
        if s<T: st.append({"at":at,"vars":v,"note":f"The sum {s} is below {T}, so left moves right."}); l+=1
        elif s>T: st.append({"at":at,"vars":v,"note":f"The sum {s} is above {T}, so right moves left."}); r-=1
        else:
            out.append([a[l],a[r]]); x,y=a[l],a[r]
            nl,nr=l,r
            while nl<nr and a[nl]==x: nl+=1
            while nl<nr and a[nr]==y: nr-=1
            st.append({"at":at,"vars":{"sum":str(s),"pairs":str(out)},"note":f"The sum {s} equals {T}, so the pair {out[-1]} is recorded. Then left skips the run of {x} and right skips the run of {y}."}); l,r=nl,nr
    assert out==[[1,5],[2,4],[3,3]]
    return block(a,["left","right"],st)
def t2():
    a=[-2,-1,0,0,1,1,2,2]; T=2; base=0; l,r=1,7; st=[]; out=[]
    # fixed value a[0] = -2, pair target 2
    while l<r:
        s=a[l]+a[r]; at={"left":l,"right":r}
        if s<T: st.append({"at":at,"vars":{"sum":str(s),"fixed":"-2","found":str(out)},"note":f"The sum {s} is below {T}, so left moves right."}); l+=1
        elif s>T: st.append({"at":at,"vars":{"sum":str(s),"fixed":"-2","found":str(out)},"note":f"The sum {s} is above {T}, so right moves left."}); r-=1
        else:
            out.append([-2,a[l],a[r]]); x,y=a[l],a[r]; nl,nr=l,r
            while nl<nr and a[nl]==x: nl+=1
            while nl<nr and a[nr]==y: nr-=1
            st.append({"at":at,"vars":{"sum":str(s),"fixed":"-2","found":str(out)},"note":f"With the fixed value -2, the sum {s} matches the pair target {T}, so the triplet {out[-1]} is recorded. Both pointers skip their runs."}); l,r=nl,nr
    assert out==[[-2,0,2],[-2,1,1]],out
    return block(a,["left","right"],st)
fill(CH,F,t1(),"@@TRACE1@@"); fill(CH,F,t2(),"@@TRACE2@@")
