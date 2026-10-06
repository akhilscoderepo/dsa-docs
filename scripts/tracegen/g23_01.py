from common import *
CH='23-directed-graphs-and-union-find'
J=lambda xs:"-".join(map(str,xs)) if xs else "empty"
def run(n,edges,ph):
    adj=[[] for _ in range(n)]; indeg=[0]*n
    for a,b in edges: adj[a].append(b); indeg[b]+=1
    q=[v for v in range(n) if indeg[v]==0]; order=[]; st=[]
    while q:
        cur=q.pop(0); order.append(cur)
        for w in adj[cur]:
            indeg[w]-=1
            if indeg[w]==0: q.append(w)
        st.append({"at":{"cur":cur},"vars":{"indeg":J(indeg).replace("-",","),"queue":J(q),"order":J(order)},"note":f"The loop removes vertex {cur}, lowers its followers' counters and queues those that reach 0."})
    if len(order)==n: st.append({"at":{"cur":-1},"vars":{"indeg":J(indeg).replace("-",","),"queue":"empty","order":J(order)},"note":f"The queue is empty and count equals n = {n}, so the method returns the order."})
    else: st.append({"at":{"cur":-1},"vars":{"indeg":J(indeg).replace("-",","),"queue":"empty","order":J(order)},"note":f"The queue is empty and count is {len(order)} while n is {n}, so a cycle blocks the other vertices and the method returns an empty array."})
    fill(CH,'01-kahn-topological-order.md',block(list(range(n)),["cur"],st),ph); return order
assert run(6,[(0,2),(1,2),(2,3),(1,4),(4,3)],"@@TRACE1@@")==[0,1,5,2,4,3]
assert run(5,[(0,1),(1,2),(2,1),(2,3),(4,3)],"@@TRACE2@@")==[0,4]
