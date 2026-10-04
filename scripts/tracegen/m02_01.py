from common import *
CH='02-matrices-and-2d-arrays'; F='01-shape-contracts.md'
def run(g):
    tot=0; st=[{"at":{"r":-1},"vars":{"total":0},"note":"Start: no row has been read, so total is 0."}]
    for r,row in enumerate(g):
        s=sum(row); tot+=s
        n=f"Row {r} holds {len(row)} cell(s)"+(f" and adds {s}." if row else ", so the inner loop runs zero times.")
        st.append({"at":{"r":r},"vars":{"rowLength":len(row),"total":tot},"note":n+f" The total is {tot}."})
    st.append({"at":{"r":len(g)},"vars":{"total":tot},"note":f"The row index equals grid.length, so the loop ends with total {tot}."})
    return st,tot
cells=lambda g:[str(x).replace(' ','') for x in g]
g=[[1,2],[3,4]]; st,t=run(g); assert t==10
fill(CH,F,block(cells(g),["r"],st),"@@TRACE1@@")
g=[[1,2],[],[3]]; st,t=run(g); assert t==6
fill(CH,F,block(cells(g),["r"],st),"@@TRACE2@@")
