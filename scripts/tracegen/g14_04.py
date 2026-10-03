from common import *
CH='14-linked-lists'
F='04-merge.md'
A=[2,5,9];B=[1,5,7,8]
cells=A+B
out=[];i=0;j=0
def idx_a(i): return i if i<len(A) else -1
def idx_b(j): return len(A)+j if j<len(B) else -1
steps=[]
while i<len(A) and j<len(B):
    if B[j]<A[i]:
        v=B[j];src="second";j+=1
    else:
        v=A[i];src="first";i+=1
    out.append(v)
    steps.append({"at":{"a":idx_a(i),"b":idx_b(j)},"vars":{"result":"["+",".join(map(str,out))+"]"},"note":f"The node holding {v} from the {src} list is attached to the result tail, and that list's head moves forward."})
rest=A[i:] if i<len(A) else B[j:]
out+=rest
steps.append({"at":{"a":idx_a(i),"b":-1},"vars":{"result":"["+",".join(map(str,out))+"]"},"note":"The second list is exhausted, so the whole remaining first list, a single node holding 9, is attached in one assignment."})
assert out==[1,2,5,5,7,8,9]
fill(CH,F,block(cells,["a","b"],steps),"@@TRACE1@@")
A2=[1,2];B2=[5,6];c2=A2+B2
i=j=0;out=[];s2=[];comp=0
while i<2 and j<2:
    comp+=1
    if B2[j]<A2[i]: v=B2[j];j+=1;src="second"
    else: v=A2[i];i+=1;src="first"
    out.append(v)
    s2.append({"at":{"a":i if i<2 else -1,"b":2+j if j<2 else -1},"vars":{"result":"["+",".join(map(str,out))+"]","comparisons":comp},"note":f"The node holding {v} from the {src} list is attached after one comparison."})
out+=B2[j:]
s2.append({"at":{"a":-1,"b":2},"vars":{"result":"["+",".join(map(str,out))+"]","comparisons":comp},"note":"The first list is exhausted after two comparisons, and the second list, still headed by the node holding 5, is attached as a whole without any further comparison."})
assert out==[1,2,5,6] and comp==2
fill(CH,F,block(c2,["a","b"],s2),"@@TRACE2@@")
