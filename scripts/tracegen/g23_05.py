from common import *
CH='23-directed-graphs-and-union-find'; N='05-union-by-size.md'
def run(n,ops,ph,expect_parent):
    parent=list(range(n)); size=[1]*n; comps=n; st=[]
    def find(x):
        while parent[x]!=x: x=parent[x]
        return x
    for a,b in ops:
        big=find(a); small=find(b)
        if big==small:
            note=f"The call ({a},{b}) finds the single root {big} for both arguments, so it changes nothing."
        else:
            if size[big]<size[small]: big,small=small,big
            parent[small]=big; size[big]+=size[small]; comps-=1
            note=f"The call ({a},{b}) joins the roots {big} and {small}. The root {small} becomes a child of {big}, and size[{big}] becomes {size[big]}."
        st.append({"at":{"big":big,"small":small},"vars":{"call":f"{a},{b}","parent":" ".join(map(str,parent)),"size":" ".join(map(str,size)),"components":comps},"note":note})
    assert parent==expect_parent,(parent,expect_parent)
    fill(CH,N,block(list(range(n)),["big","small"],st),ph)
run(6,[[0,1],[2,1],[3,4],[4,2]],"@@TRACE1@@",[0,0,0,0,3,5])
run(5,[[0,1],[1,0],[2,2],[2,3],[3,1]],"@@TRACE2@@",[2,0,2,2,4])
