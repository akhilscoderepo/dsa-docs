from common import *
CH='23-directed-graphs-and-union-find'
F='04-find-compression.md'
def run(parent, queries, cells):
    steps=[]
    for q in queries:
        x=q; root=x; hops=0
        # climb
        path=[]
        while True:
            steps.append({"at":{"x":x},"vars":{"hops":hops,"rewrites":0},
              "note":f"Query {q}: card {x} is read; "+("it names itself, so it is the root." if parent[x]==x else f"it names {parent[x]}, one more hop.")})
            if parent[x]==x: break
            x=parent[x]; hops+=1
        root=x
        rewrites=0; x=q
        if parent[x]==root:
            steps[-1]["note"]+=f" Member {q} already follows the root, so nothing is rewritten."
        while parent[x]!=root:
            nxt=parent[x]; parent[x]=root; rewrites+=1
            steps.append({"at":{"x":x},"vars":{"hops":hops,"rewrites":rewrites},
              "note":f"Query {q}: card {x} now names the root {root} instead of {nxt}."})
            x=nxt
        yield_ = (q,hops,rewrites,root)
        run.res.append(yield_)
    return steps
run.res=[]
# trace 1
p1=[0]+list(range(0,7))
assert p1==[0,0,1,2,3,4,5,6]
s1=run(p1,[7],list(range(8)))
assert run.res[-1]==(7,7,6,0), run.res[-1]
assert p1==[0,0,0,0,0,0,0,0]
assert len(s1)==14
fill(CH,F,block(list(range(8)),["x"],s1),"@@TRACE1@@")
# trace 2
run.res=[]
p2=[0,0,0,1,1,3,4,2,7]
s2=run(p2,[8,6,8],list(range(9)))
assert run.res==[(8,3,2,0),(6,3,2,0),(8,1,0,0)], run.res
print(run.res, p2)
assert p2==[0,0,0,1,0,3,0,0,0], p2
fill(CH,F,block(list(range(9)),["x"],s2),"@@TRACE2@@")
