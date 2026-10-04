from common import *
CH='23-directed-graphs-and-union-find'
F='03-undirected-parent-state.md'
def adjl(n,es):
    a=[[] for _ in range(n)]
    for x,y in es: a[x].append(y); a[y].append(x)
    return a
# trace 1: parent walk on a tree
n=6; es=[[0,1],[0,2],[1,3],[1,4],[2,5]]
adj=adjl(n,es); seen=[False]*n; steps=[]; reached=[0]; ring=[False]
def walk(v,p):
    seen[v]=True; reached[0]+=1
    steps.append({"at":{"cur":v},"vars":{"parent":p,"reached":reached[0]},
      "note":f"Post {v} is entered"+(f" from post {p}." if p>=0 else " as the start.")})
    for w in adj[v]:
        if w==p:
            steps.append({"at":{"cur":v},"vars":{"parent":p,"reached":reached[0]},"note":f"Post {w} is the parent vertex of post {v}, so that string is skipped."}); continue
        assert not seen[w]; 
        walk(w,v)
        steps.append({"at":{"cur":v},"vars":{"parent":p,"reached":reached[0]},"note":f"The walk returns to post {v} with {reached[0]} posts reached so far."})
walk(0,-1)
assert reached[0]==n
steps.append({"at":{"cur":0},"vars":{"parent":-1,"reached":reached[0]},"note":f"No ring was found and {reached[0]} posts were reached, which equals n = {n}, so the layout is a tree."})
fill(CH,F,block(list(range(n)),["cur"],steps),"@@TRACE1@@")
# trace 2: count passes, plain reach falls short
n=5; es=[[0,1],[1,2],[2,0],[3,4]]
assert len(es)==n-1
adj=adjl(n,es); seen=[False]*n; seen[0]=True; stack=[0]; reached=1; steps=[]
steps.append({"at":{"cur":0},"vars":{"strings":len(es),"reached":1},"note":"The list holds 4 strings and n - 1 is 4, so the count rule passes. Post 0 is marked as reached."})
while stack:
    v=stack.pop(); new=[]
    for w in adj[v]:
        if not seen[w]: seen[w]=True; reached+=1; stack.append(w); new.append(w)
    steps.append({"at":{"cur":v},"vars":{"strings":len(es),"reached":reached},
      "note":f"Post {v} is expanded"+(f" and marks post{'s' if len(new)>1 else ''} {', '.join(map(str,new))}." if new else "; every neighbor is already marked.")})
assert reached==3
steps.append({"at":{"cur":0},"vars":{"strings":len(es),"reached":reached},"note":"The walk is finished with 3 posts reached out of 5, so posts 3 and 4 are cut off and the answer is false."})
fill(CH,F,block(list(range(n)),["cur"],steps),"@@TRACE2@@")
print("ok")
