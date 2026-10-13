from common import *
CH='35-advanced-search-sampling-and-geometric-state'; N='04-weighted-selection.md'
def run(w,ticket,ph,expect):
    P=[];s=0
    for x in w: s+=x; P.append(s)
    lo,hi=0,len(P)-1; st=[{"at":{"lo":lo,"mid":-1,"hi":hi},"vars":{"ticket":ticket},"note":f"Start: ticket {ticket}, search the whole range of indexes 0 to {hi}."}]
    while lo<hi:
        m=(lo+hi)//2
        if P[m]>=ticket: hi=m; n=f"The prefix total {P[m]} at index {m} is at least {ticket}, so hi moves to {m}."
        else: lo=m+1; n=f"The prefix total {P[m]} at index {m} is below {ticket}, so lo moves to {lo}."
        st.append({"at":{"lo":lo,"mid":m,"hi":hi},"vars":{"ticket":ticket,"value":P[m]},"note":n})
    st.append({"at":{"lo":lo,"mid":lo,"hi":hi},"vars":{"ticket":ticket,"owner":lo},"note":f"The search ends with lo equal to hi at index {lo}, so index {lo} owns ticket {ticket}."})
    assert lo==expect; fill(CH,N,block(P,["lo","mid","hi"],st),ph)
run([3,1,4,2],5,"@@TRACE1@@",2); run([3,1,4,2],4,"@@TRACE2@@",1)
