from common import *
CH='17-heaps-and-priority-queues'; F='01-priorityqueue-mechanics.md'
# Trace 1: offers
vals=[5,3,8,1,4]; h=[]; st=[]
for i,v in enumerate(vals):
    h.append(v); j=len(h)-1; sw=0
    while j>0 and h[(j-1)//2]>h[j]:
        h[(j-1)//2],h[j]=h[j],h[(j-1)//2]; j=(j-1)//2; sw+=1
    st.append({"at":{"next":i},"vars":{"array":str(h)},"note":f"The value {v} enters at the end and swaps {sw} time(s) during sift up. The array is now {h}."})
st.append({"at":{"next":len(vals)},"vars":{"array":str(h)},"note":f"All values are in. The root is {h[0]}, and the array {h} is not in sorted order."})
assert h==[1,3,8,5,4]
fill(CH,F,block(vals,["next"],st),"@@TRACE1@@")
# Trace 2: polls
h=[1,3,8,5,4]; cells=list(h); st=[]; outs=[]
st.append({"at":{"hole":-1,"child":-1},"vars":{"array":str(h),"returned":"[]"},"note":"The queue holds [1, 3, 8, 5, 4] and no poll has run."})
for _ in range(2):
    top=h[0]; last=h.pop()
    outs.append(top)
    if h:
        h[0]=last; j=0
        st.append({"at":{"hole":0,"child":-1},"vars":{"array":str(h),"returned":str(outs)},"note":f"The poll takes {top} from the root. The last item {last} moves to the root, so the array is {h}."})
        while True:
            c=2*j+1
            if c>=len(h): break
            if c+1<len(h) and h[c+1]<h[c]: c+=1
            if h[c]>=h[j]:
                st.append({"at":{"hole":j,"child":c},"vars":{"array":str(h),"returned":str(outs)},"note":f"The smaller child {h[c]} is not smaller than {h[j]}, so sift down stops."}); break
            h[c],h[j]=h[j],h[c]
            st.append({"at":{"hole":c,"child":-1},"vars":{"array":str(h),"returned":str(outs)},"note":f"The item swaps with its smaller child. The moving item now sits at position {c}, and the array is {h}."}); j=c
        else: pass
assert outs==[1,3] and h==[4,5,8]
fill(CH,F,block(cells,["hole","child"],st),"@@TRACE2@@")
