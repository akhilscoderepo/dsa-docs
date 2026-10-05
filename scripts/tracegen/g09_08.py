from common import *
CH='09-sliding-window'; F='08-count-every-valid-subarray.md'
def run(a,K):
    l=0; s=0; tot=0; st=[]
    for r,v in enumerate(a):
        s+=v; n=f"The value {v} enters, so the sum is {s}."
        while l<=r and s>=K:
            n+=f" The sum {s} is not below {K}, so the value {a[l]} leaves."; s-=a[l]; l+=1
        add=r-l+1; tot+=add
        n+=f" The starts {l} to {r} are valid, so add is {add} and the count is {tot}." if add else f" The window is empty, so add is 0 and the count is {tot}."
        st.append({"at":{"left":l,"right":r},"vars":{"sum":str(s),"add":str(add),"count":str(tot)},"note":n})
    return st,tot
a=[2,1,3,1,2]; st,t=run(a,5); assert t==9
fill(CH,F,block(a,["left","right"],st),"@@TRACE1@@")
a=[2,3,1]; st,t=run(a,1); assert t==0
fill(CH,F,block(a,["left","right"],st),"@@TRACE2@@")
