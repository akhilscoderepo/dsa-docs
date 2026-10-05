from common import *
CH='08-two-pointers'; F='91-sums-in-sorted-arrays.md'
def t1():
    a=[8,3,12,5]; T=13; ks=sorted((v,i) for i,v in enumerate(a)); vals=[v for v,_ in ks]; st=[]; l,r=0,3
    while l<r:
        s=vals[l]+vals[r]; at={"left":l,"right":r}; v={"sum":str(s),"rows":f"{ks[l][1]} and {ks[r][1]}"}
        if s==T: st.append({"at":at,"vars":v,"note":f"The sum {s} equals {T}. The keys hold the original rows {ks[l][1]} and {ks[r][1]}, so the answer is {sorted([ks[l][1],ks[r][1]])}."}); break
        if s<T: st.append({"at":at,"vars":v,"note":f"The sum {s} is below {T}, so left moves right."}); l+=1
        else: st.append({"at":at,"vars":v,"note":f"The sum {s} is above {T}, so right moves left."}); r-=1
    assert sorted([ks[l][1],ks[r][1]])==[0,3]
    return block(vals,["left","right"],st)
def t2():
    a=[9,2,-5,3,1]; T=0; ks=sorted((v,i) for i,v in enumerate(a)); vals=[v for v,_ in ks]; st=[]; found=None
    for i in range(3):
        rem=T-vals[i]; l,r=i+1,4
        while l<r:
            s=vals[l]+vals[r]; at={"i":i,"left":l,"right":r}; v={"remaining":str(rem),"sum":str(s)}
            if s==rem:
                rows=sorted([ks[i][1],ks[l][1],ks[r][1]]); st.append({"at":at,"vars":v,"note":f"The pair sum {s} equals the remaining target {rem}. The three keys hold the original rows {rows}."}); found=rows; break
            if s<rem: st.append({"at":at,"vars":v,"note":f"The pair sum {s} is below the remaining target {rem}, so left moves right."}); l+=1
            else: st.append({"at":at,"vars":v,"note":f"The pair sum {s} is above the remaining target {rem}, so right moves left."}); r-=1
        if found: break
    assert found==[1,2,3]
    return block(vals,["i","left","right"],st)
fill(CH,F,t1(),"@@TRACE1@@"); fill(CH,F,t2(),"@@TRACE2@@")
