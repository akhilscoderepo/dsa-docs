from common import *
CH='09-sliding-window'; F='06-exactly-k-by-subtraction.md'
def run(a,lim):
    l=0; odd=0; tot=0; st=[]
    for r,v in enumerate(a):
        n=f"The value {v} enters."
        if v%2: odd+=1; n+=f" It is odd, so the odd count is {odd}."
        while odd>lim:
            g=a[l]
            if g%2: odd-=1; n+=f" The odd value {g} leaves, so the odd count is {odd}."
            else: n+=f" The even value {g} leaves."
            l+=1
        add=r-l+1; tot+=add; n+=f" The starts {l} to {r} are valid, so add is {add} and the total is {tot}."
        st.append({"at":{"left":l,"right":r},"vars":{"odd":str(odd),"add":str(add),"total":str(tot)},"note":n})
    return st,tot
def brute(a,k): return sum(1 for i in range(len(a)) for j in range(i,len(a)) if sum(x%2 for x in a[i:j+1])<=k)
a=[2,1,3,4,1]; st,t2=run(a,2); assert t2==brute(a,2)==13
fill(CH,F,block(a,["left","right"],st),"@@TRACE1@@")
st,t1=run(a,1); assert t1==brute(a,1)==8 and t2-t1==5
fill(CH,F,block(a,["left","right"],st),"@@TRACE2@@")
