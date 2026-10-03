from common import *
CH='06-binary-search'
F='10-time-indexed-lookup.md'
def run(times,when):
    lo,hi=0,len(times); st=[]
    while lo<hi:
        mid=(lo+hi)//2
        if times[mid]<=when:
            st.append({"at":{"lo":lo,"hi":hi,"mid":mid},"vars":{"time":times[mid],"query":when},"note":f"Time {times[mid]} is not after {when}, so the boundary is to its right and lo moves to {mid+1}."}); lo=mid+1
        else:
            st.append({"at":{"lo":lo,"hi":hi,"mid":mid},"vars":{"time":times[mid],"query":when},"note":f"Time {times[mid]} is after {when}, so the boundary is here or to the left and hi moves to {mid}."}); hi=mid
    return lo,st
times=[2,5,9,14,20,27]
lo,st=run(times,15)
assert lo==4 and times[lo-1]==14
st.append({"at":{"lo":lo,"hi":lo,"mid":-1},"vars":{"upperBound":lo,"answerPosition":lo-1,"answerTime":times[lo-1]},"note":f"The upper bound is position {lo}, so the answer is position {lo-1}, the change at time {times[lo-1]}."})
fill(CH,F,block([str(t) for t in times],["lo","hi","mid"],st),"@@TRACE1@@")
times=[2,5,9]
lo,st=run(times,1)
assert lo==0
st.append({"at":{"lo":0,"hi":0,"mid":-1},"vars":{"upperBound":0,"answer":"blank"},"note":"The upper bound is position 0, so no change is at or before time 1 and the answer is the blank value."})
fill(CH,F,block([str(t) for t in times],["lo","hi","mid"],st),"@@TRACE2@@")
