from common import *
CH='10-intervals'
F='01-endpoint-ordering-contracts.md'
def lab(iv): return [f"{s}-{e}" for s,e in iv]
iv=[[1,3],[2,6],[8,10],[15,18]]; st=[]; reach=iv[0][1]; blocks=1
st.append({"at":{"i":0},"vars":{"reach":reach,"blocks":blocks},"note":f"The first card 1 to 3 opens a block, so the reach is {reach} and there is 1 block."})
for i in range(1,len(iv)):
    s,e=iv[i]
    if s<=reach:
        reach=max(reach,e); st.append({"at":{"i":i},"vars":{"reach":reach,"blocks":blocks},"note":f"The card starts at {s}, not past the reach, so it joins the block and the reach becomes {reach}."})
    else:
        blocks+=1; reach=e; st.append({"at":{"i":i},"vars":{"reach":reach,"blocks":blocks},"note":f"The card starts at {s}, past the reach, so a new block opens and the count is {blocks}."})
assert blocks==3 and "reach becomes 6" in st[1]["note"]
fill(CH,F,block(lab(iv),["i"],st),"@@TRACE1@@")
iv=[[1,2],[5,6],[0,10]]; st=[]; out=[[1,2]]; blocks=1; reach=2
st.append({"at":{"i":0},"vars":{"reach":reach,"blocks":blocks},"note":"The first card 1 to 2 opens a block, so the reach is 2 and there is 1 block."})
s,e=iv[1]; blocks+=1; reach=e
st.append({"at":{"i":1},"vars":{"reach":reach,"blocks":blocks},"note":f"The card starts at {s}, past the reach of 2, so a new block opens and the count is {blocks}."})
s,e=iv[2]; reach=max(reach,e)
st.append({"at":{"i":2},"vars":{"reach":reach,"blocks":blocks},"note":f"The card starts at {s}, not past the reach of 6, so it merges with the last block only. The count stays {blocks}, but the true answer is 1."})
assert blocks==2
fill(CH,F,block(lab(iv),["i"],st),"@@TRACE2@@")
