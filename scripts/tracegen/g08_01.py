from common import *
CH='08-two-pointers'; F='01-opposite-ends.md'
def t1():
    a=[1,3,4,6,8,11]; T=10; l,r=0,len(a)-1; st=[]
    while l<r:
        s=a[l]+a[r]; v={"sum":str(s)}
        if s==T: st.append({"at":{"left":l,"right":r},"vars":v,"note":f"The sum {s} equals the target {T}, so the pair at indexes {l} and {r} is the answer."}); break
        if s<T: st.append({"at":{"left":l,"right":r},"vars":v,"note":f"The sum {s} is below {T}, so index {l} cannot help and left moves right."}); l+=1
        else: st.append({"at":{"left":l,"right":r},"vars":v,"note":f"The sum {s} is above {T}, so index {r} cannot help and right moves left."}); r-=1
    assert (l,r)==(2,3)
    return block(a,["left","right"],st)
def t2():
    h=[4,2,5,3,6,1]; l,r=0,5; best=0; st=[]
    while l<r:
        ar=min(h[l],h[r])*(r-l); best=max(best,ar)
        if h[l]<=h[r]: mv=f"The wall at index {l} is not taller, so left moves right."; nl,nr=l+1,r
        else: mv=f"The wall at index {r} is shorter, so right moves left."; nl,nr=l,r-1
        st.append({"at":{"left":l,"right":r},"vars":{"area":str(ar),"best":str(best)},"note":f"The area is min({h[l]}, {h[r]}) * {r-l} = {ar}. "+mv})
        l,r=nl,nr
    assert best==max(min(h[i],h[j])*(j-i) for i in range(6) for j in range(i+1,6))
    return block(h,["left","right"],st)
fill(CH,F,t2(),"@@TRACE2@@")
