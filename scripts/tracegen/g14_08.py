from common import *
CH='14-linked-lists'; F='08-middle-nodes.md'
def run(vals,test):
    n=len(vals); slow=0; fast=0; k=0
    def at(): return {"slow":slow,"fast":-1 if fast>=n else fast}
    st=[{"at":at(),"vars":{"steps":0},"note":f"Start: slow and fast both hold the node {vals[0]}."}]
    def can(f):
        if test=="second": return f<n and f+1<n
        return f+1<n and f+2<n
    while can(fast):
        slow+=1; fast+=2; k+=1
        fd="null" if fast>=n else f"the node {vals[fast]}"
        st.append({"at":at(),"vars":{"steps":k},"note":f"slow moves 1 and fast moves 2. slow holds the node {vals[slow]}, and fast holds {fd}."})
    st.append({"at":at(),"vars":{"steps":k},"note":f"The loop test fails, so the loop stops. slow holds the node {vals[slow]}."})
    return st,slow
v=[10,20,30,40,50]; st,s=run(v,"second"); assert s==2
fill(CH,F,block(v,["slow","fast"],st),"@@TRACE1@@")
v=[1,2,3,4,5,6]; st,s=run(v,"second"); assert s==3 and v[s]==4
fill(CH,F,block(v,["slow","fast"],st),"@@TRACE2@@")
