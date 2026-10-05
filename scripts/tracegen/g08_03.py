from common import *
CH='08-two-pointers'; F='03-two-way-partition.md'
def t1():
    a=[3,8,5,2,6,7]; l,r=0,len(a)-1; st=[]
    while l<r:
        v={"array":str(a)}
        if a[l]%2==0: st.append({"at":{"left":l,"right":r},"vars":v,"note":f"The value {a[l]} at left is even, so left moves right."}); l+=1
        elif a[r]%2!=0: st.append({"at":{"left":l,"right":r},"vars":v,"note":f"The value {a[r]} at right is odd, so right moves left."}); r-=1
        else:
            x,y=a[l],a[r]; a[l],a[r]=y,x
            st.append({"at":{"left":l,"right":r},"vars":{"array":str(a)},"note":f"The values {x} and {y} are both misplaced, so the scan swaps them and moves both pointers."}); l+=1; r-=1
    st.append({"at":{"left":l,"right":r},"vars":{"array":str(a)},"note":"The pointers have met. Every even value stands before every odd value."})
    assert all(x%2==0 for x in a[:3]) and all(x%2 for x in a[3:])
    return block([3,8,5,2,6,7],["left","right"],st)
def t2():
    a=[7,2,9,3,5,1]; P=5; s=0; st=[]
    for i in range(len(a)):
        if a[i]<P:
            if i!=s:
                x,y=a[s],a[i]; a[s],a[i]=y,x
                st.append({"at":{"i":i,"store":s},"vars":{"array":str(a)},"note":f"The value {y} is below {P}, so it swaps with {x} at store and store advances."})
            else: st.append({"at":{"i":i,"store":s},"vars":{"array":str(a)},"note":f"The value {a[i]} is below {P} and already sits at store, so store advances."})
            s+=1
        else: st.append({"at":{"i":i,"store":s},"vars":{"array":str(a)},"note":f"The value {a[i]} is not below {P}, so only i moves."})
    st.append({"at":{"i":len(a),"store":s},"vars":{"array":str(a)},"note":f"The scan ends with store = {s}. The first {s} slots hold the values below {P}."})
    assert all(x<P for x in a[:s]) and all(x>=P for x in a[s:]) and s==3
    return block([7,2,9,3,5,1],["i","store"],st)
fill(CH,F,t1(),"@@TRACE1@@"); fill(CH,F,t2(),"@@TRACE2@@")
