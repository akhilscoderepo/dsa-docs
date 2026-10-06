from common import *
CH='20-greedy'; F='01-local-choice.md'
def run(jobs,servers,ph):
    st=[]; i=0; jobs=sorted(jobs); servers=sorted(servers); disc=0
    for j,s in enumerate(servers):
        if i>=len(jobs): break
        if s>=jobs[i]:
            note=f"The server of size {s} fits the job of size {jobs[i]}, so the pass places the job and moves to the next job."; i+=1
        else:
            note=f"The server of size {s} is smaller than the job of size {jobs[i]}, so the pass discards it and moves on."; disc+=1
        st.append({"at":{"j":j},"vars":{"i":i,"placed":i},"note":note})
    fill(CH,F,block(servers,["j"],st),ph); return i
assert run([3,8,5],[9,4,6],"@@TRACE1@@")==3
assert run([5,6],[1,2,5,7],"@@TRACE2@@")==2
