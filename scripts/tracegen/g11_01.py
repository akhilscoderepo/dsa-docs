from common import *
CH='11-stacks-and-queues'
F='01-arraydeque-contracts.md'
ops=["addLast 4","addLast 7","addLast 1","removeLast","removeLast"]
dq=[]; st=[]; out=[]
for i,o in enumerate(ops):
    if o.startswith("addLast"):
        v=int(o.split()[1]); dq.append(v); note=f"The value {v} goes to the last position, so it becomes the top of the stack."
    else:
        v=dq.pop(); out.append(v); note=f"The removal takes from the last position and returns {v}, the value that arrived most recently."
    st.append({"at":{"op":i},"vars":{"deque":str(dq).replace(' ',''),"out":str(out).replace(' ','')},"note":note})
assert out==[1,7]
fill(CH,F,block(ops,["op"],st),"@@TRACE1@@")
ops2=["pollFirst","peekFirst","removeFirst","addLast null","addLast 5","addLast null"]
res=["null","null","NoSuchElementException","NullPointerException","stored 5","NullPointerException"]
notes=["The deque is empty, so pollFirst returns null instead of throwing.",
"The deque is empty, so peekFirst returns null too, and the null can only mean empty.",
"The deque is still empty, but removeFirst belongs to the throwing family, so it raises NoSuchElementException.",
"Adding null is refused with NullPointerException even though the deque is empty, so nothing is stored.",
"The value 5 is added at the last position, and the deque now holds one element.",
"Adding null is refused again, and the deque still holds only 5."]
dqs=["[]","[]","[]","[]","[5]","[5]"]
st=[{"at":{"op":i},"vars":{"result":res[i],"deque":dqs[i]},"note":notes[i]} for i in range(6)]
fill(CH,F,block(ops2,["op"],st),"@@TRACE2@@")
