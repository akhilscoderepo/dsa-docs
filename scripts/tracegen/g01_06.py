from common import *
CH='01-arrays-core-operations'
arr=[3,1,3,0,3,1]; D=5
count=[0]*D; st=[]
for i,x in enumerate(arr):
    count[x]+=1
    st.append({"at":{"i":i},"vars":{"count":str(count)},"note":f"Read {x} at index {i}. Slot {x} rises to {count[x]}. The counts are now {count}."})
assert count==[1,2,0,3,0]
fill(CH,'06-frequency-arrays.md',block(arr,["i"],st),"@@TRACE1@@")
before=[]; running=0; st=[]
for v in range(D):
    before.append(running)
    note=f"Slot {v} holds {count[v]} readings. The number of readings below {v} is {running}, so the total is stored for slot {v}."
    running+=count[v]
    note+=f" The running total becomes {running}."
    st.append({"at":{"i":v},"vars":{"count":str(count),"before":str(before)},"note":note})
assert before==[0,1,3,3,6]
fill(CH,'06-frequency-arrays.md',block(count,["i"],st),"@@TRACE2@@")
