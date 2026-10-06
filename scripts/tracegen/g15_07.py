from common import *
CH='15-trees-dfs'; F='07-traversal-reconstruction.md'
def run(pre,inn):
    where={v:i for i,v in enumerate(inn)}; steps=[]; n=len(inn)
    def rec(pl,pr,il,ir):
        if pl>pr: return
        r=pre[pl]; k=where[r]; ls=k-il; rs=ir-k
        steps.append({"at":{"lo":il,"root":k,"hi":ir},"vars":{"preorder window":f"{pl} to {pr}","left size":ls,"right size":rs},"note":f"The first value of the preorder window is {r}. It sits at inorder position {k}, so {ls} values go to the left subtree and {rs} go to the right subtree."})
        rec(pl+1,pl+ls,il,k-1); rec(pl+ls+1,pr,k+1,ir)
    rec(0,len(pre)-1,0,n-1); return steps
pre=[8,5,2,9,4,7]; inn=[2,5,9,8,7,4]; s=run(pre,inn); assert len(s)==6
fill(CH,F,block([str(x) for x in inn],["lo","root","hi"],s),"@@TRACE1@@")
pre=[5,4,3]; inn=[3,4,5]; s=run(pre,inn); assert len(s)==3
fill(CH,F,block([str(x) for x in inn],["lo","root","hi"],s),"@@TRACE2@@")
