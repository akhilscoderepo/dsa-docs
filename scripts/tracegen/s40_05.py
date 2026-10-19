from common import *
CH='40-composite-indexes-and-allocation'; F='05-validated-priority.md'
def run(calls):
    clock=0; cur={}; heap=[]; cells=[]; st=[]; out=[]
    for o,a in calls: cells.append(f"{o}({','.join(map(str,a))})")
    def view(): return " ".join(f"{p}:{i}@{v}" for p,i,v in sorted(heap,key=lambda e:(-e[0],e[1],e[2]))) or "empty"
    for n,(o,a) in enumerate(calls):
        r="null"
        if o=="set":
            i,p=a; clock+=1; cur[i]=(p,clock); heap.append((p,i,clock)); note=f"Call {n}: the record for job {i} becomes priority {p} with version {clock}, and the heap gains an entry. Older entries for job {i} stay in the heap."
        elif o=="cancel":
            del cur[a[0]]; note=f"Call {n}: job {a[0]} leaves the record. Its heap entries stay and now fail the version check."
        else:
            notes=[]
            r="-1"
            while heap:
                heap.sort(key=lambda e:(-e[0],e[1],e[2])); p,i,v=heap.pop(0)
                if i in cur and cur[i][1]==v:
                    del cur[i]; r=str(i); notes.append(f"entry {p}:{i}@{v} matches the record, so poll returns job {i}"); break
                notes.append(f"entry {p}:{i}@{v} fails the version check, so poll drops it")
            if r=="-1": notes.append("the heap is empty, so poll returns -1")
            note=f"Call {n}: "+"; then ".join(notes)+"."
        st.append({"at":{"call":n},"vars":{"heap":view(),"result":r},"note":note}); out.append(r)
    return cells,st,out
c,s,o=run([("set",(1,5)),("set",(2,9)),("set",(1,12)),("poll",()),("poll",()),("poll",())])
assert o[3:]==["1","2","-1"]
fill(CH,F,block(c,["call"],s),"@@TRACE1@@")
c,s,o=run([("set",(3,7)),("cancel",(3,)),("set",(3,7)),("poll",()),("poll",())])
assert o[3:]==["3","-1"]
fill(CH,F,block(c,["call"],s),"@@TRACE2@@")
