from common import *
CH='06-binary-search'
T=[2,5,9,14,20]
def run(q,ph,expect):
    lo,hi=0,len(T)
    st=[{"at":{"lo":0,"hi":5,"mid":-1},"vars":{"query":str(q)},"note":f"Start with the whole list. The query is {q}."}]
    while lo<hi:
        mid=lo+(hi-lo)//2
        if T[mid]<=q: lo=mid+1; note=f"Time {T[mid]} does not pass {q}, so lo becomes {lo}."
        else: hi=mid; note=f"Time {T[mid]} passes {q}, so hi becomes {hi}."
        st.append({"at":{"lo":lo,"hi":hi,"mid":mid},"vars":{"time[mid]":str(T[mid])},"note":note})
    ans=lo-1
    assert ans==expect
    st.append({"at":{"lo":lo,"hi":hi,"mid":-1},"vars":{"p":str(lo),"answer":str(ans)},"note":(f"The interval is empty with p = {lo}, so the answer is position {ans}, the entry at time {T[ans]}." if ans>=0 else "The interval is empty with p = 0, so no entry applies and the lookup returns the empty answer.")})
    fill(CH,'91-time-lookup.md',block(T,["lo","hi","mid"],st),ph)
run(12,"@@TRACE1@@",2)
run(1,"@@TRACE2@@",-1)
