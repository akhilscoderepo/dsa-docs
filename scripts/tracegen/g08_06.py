from common import *
CH='08-two-pointers'; F='06-k-sum-reduction.md'
def t1():
    a=[-4,-1,-1,0,1,2]; T=0; st=[]; count=0
    for i in range(len(a)-2):
        rem=T-a[i]; l,r=i+1,len(a)-1
        while l<r:
            s=a[l]+a[r]; at={"i":i,"left":l,"right":r}
            vars_={"remaining":str(rem),"sum":str(s),"count":str(count)}
            if s<rem: st.append({"at":at,"vars":vars_,"note":f"The pair sum {s} is below the remaining target {rem}, so left moves right."}); l+=1
            elif s>rem: st.append({"at":at,"vars":vars_,"note":f"The pair sum {s} is above the remaining target {rem}, so right moves left."}); r-=1
            elif a[l]==a[r]:
                m=r-l+1; add=m*(m-1)//2; count+=add
                st.append({"at":at,"vars":{"remaining":str(rem),"sum":str(s),"count":str(count)},"note":f"The ends match and hold equal values, so the block of {m} equal values adds {add} index pairs."}); break
            else:
                x,y=a[l],a[r]; rx=ry=0
                while l<=r and a[l]==x: l+=1; rx+=1
                while r>=l and a[r]==y: r-=1; ry+=1
                count+=rx*ry
                st.append({"at":at,"vars":{"remaining":str(rem),"sum":str(s),"count":str(count)},"note":f"The pair sum matches. The run of {x} has length {rx} and the run of {y} has length {ry}, so the count grows by {rx*ry}."})
    import itertools
    assert count==sum(1 for c in itertools.combinations(a,3) if sum(c)==T)==3
    return block(a,["i","left","right"],st)
def t2():
    a=[-4,-1,1,2]; T=1; st=[]; best=None
    for i in range(len(a)-2):
        l,r=i+1,len(a)-1
        while l<r:
            s=a[i]+a[l]+a[r]
            if best is None or abs(s-T)<abs(best-T) or (abs(s-T)==abs(best-T) and s<best): best=s
            at={"i":i,"left":l,"right":r}
            if s<T: st.append({"at":at,"vars":{"sum":str(s),"best":str(best)},"note":f"The total {s} is below {T}, so left moves right. The best total is {best}."}); l+=1
            elif s>T: st.append({"at":at,"vars":{"sum":str(s),"best":str(best)},"note":f"The total {s} is above {T}, so right moves left. The best total is {best}."}); r-=1
            else: st.append({"at":at,"vars":{"sum":str(s),"best":str(best)},"note":"The total equals the target."}); break
    assert best==2
    return block(a,["i","left","right"],st)
fill(CH,F,t1(),"@@TRACE1@@"); fill(CH,F,t2(),"@@TRACE2@@")
