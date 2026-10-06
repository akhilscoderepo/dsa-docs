from common import *
CH='16-trees-bfs-and-bsts'; F='07-iterator-foundations.md'
cells=[40,20,60,10,30,50,70]; kids={0:(1,2),1:(3,4),2:(5,6),3:(None,None),4:(None,None),5:(None,None),6:(None,None)}
stack=[]; work=0
def spine(i):
    global work
    while i is not None:
        stack.append(i); work+=1; i=kids[i][0]
spine(0)
assert [cells[j] for j in stack]==[40,20,10]
st=[]; calls=[]
for c in range(1,8):
    before=work
    p=stack.pop(); work+=1
    spine(kids[p][1])
    calls.append((p,work-before,work,[cells[j] for j in stack]))
for c,(p,w,tot,sk) in enumerate(calls[:3],1):
    st.append({"at":{"node":p},"vars":{"stack":str(sk)},"note":f"Call {c} pops {cells[p]} and returns it. The stack now holds {sk}."})
fill(CH,F,block(cells,["node"],st),"@@TRACE1@@")
st=[]
# total includes constructor loading (3 pushes) -> recompute cumulative
cum=0; base=3; assert calls[-1][2]==14
for c,(p,w,tot,sk) in enumerate(calls,1):
    st.append({"at":{"node":p},"vars":{"call work":w,"total":tot},"note":f"Call {c} returns {cells[p]} and spends {w} unit(s) on its pop and pushes."})
fill(CH,F,block(cells,["node"],st),"@@TRACE2@@")
print([ (cells[p],w,t) for p,w,t,_ in calls])
