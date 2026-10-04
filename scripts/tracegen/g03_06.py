from common import *
CH='03-strings'; F='06-run-construction.md'
def run(s):
    n=len(s); start=0; best=0
    st=[{"at":{"i":0},"vars":{"start":0,"best":0},"note":"Start: the open run begins at index 0 and best is 0."}]
    for i in range(1,n+1):
        if i==n or s[i]!=s[start]:
            L=i-start; best=max(best,L)
            why="the index equals the length, so the end of the string closes the final run" if i==n else f"'{s[i]}' differs from '{s[start]}', so the run closes"
            st.append({"at":{"i":i},"vars":{"start":i,"best":best},"note":f"At index {i}, {why}, with length {L}. The best length is {best}."})
            start=i
        else:
            st.append({"at":{"i":i},"vars":{"start":start,"best":best},"note":f"Index {i} holds '{s[i]}', which matches the open run, so the run grows."})
    return st,best
import itertools
for ph,s,exp in (("@@TRACE1@@","aabbbc",3),("@@TRACE2@@","xyyy",3)):
    st,b=run(s); assert b==exp==max(len(list(g)) for _,g in itertools.groupby(s))
    fill(CH,F,block(list(s),["i"],st),ph)
