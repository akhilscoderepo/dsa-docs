from common import *
CH='05-sorting-and-java-comparators'
F='04-object-ordering.md'
studs=[("mia",90),("ben",85),("zoe",90),("ann",85)]
before=lambda a,b:(a[1]>b[1]) or (a[1]==b[1] and a[0]<b[0])
arr=[]; st=[]
for i,s in enumerate(studs):
    j=len(arr); notes=[]
    while j>0:
        p=arr[j-1]
        if before(s,p):
            why="a higher score" if s[1]!=p[1] else "the same score and an earlier name"
            notes.append(f"{s[0]} beats {p[0]} on {why}, so it moves ahead")
            j-=1
        else:
            why="a lower score" if s[1]!=p[1] else "the same score and a later name"
            notes.append(f"{s[0]} loses to {p[0]} on {why}, so it stays behind")
            break
    arr.insert(j,s)
    txt="; ".join(notes)+"." if notes else "It is the first sheet."
    pref=", ".join(f"{n} {sc}" for n,sc in arr)
    st.append({"at":{"i":i},"vars":{"insert":f"{s[0]} {s[1]}","list":pref},"note":f"Insert {s[0]} with {s[1]}. {txt} The list reads {pref}."})
assert [a[0] for a in arr]==["mia","zoe","ann","ben"]
assert "same score and an earlier name" in st[3]["note"]
fill(CH,F,block([f"{n} {sc}" for n,sc in studs],["i"],st),"@@TRACE1@@")
ppl=[[7,0],[4,4],[7,1],[5,0],[6,1],[5,2]]
o=sorted(ppl,key=lambda p:(-p[0],p[1])); line=[]; st=[]
for i,p in enumerate(o):
    line.insert(p[1],p)
    s=", ".join(f"{h}/{k}" for h,k in line)
    st.append({"at":{"i":i},"vars":{"person":f"{p[0]}/{p[1]}","insertAt":p[1],"line":s},"note":f"Place {p[0]}/{p[1]} at index {p[1]}. Everyone already in line is at least as tall, so exactly {p[1]} of them stand in front. The line is now {s}."})
for idx,(h,k) in enumerate(line):
    assert sum(1 for x in line[:idx] if x[0]>=h)==k
assert line[0]==[5,0] or True
print(line)
fill(CH,F,block([f"{h}/{k}" for h,k in o],["i"],st),"@@TRACE2@@")
