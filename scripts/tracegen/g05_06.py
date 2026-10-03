from common import *
CH='05-sorting-and-java-comparators'
F='06-sort-and-sweep.md'
req=sorted([3,2,1,2,1,7]); st=[]; fr=None; tot=0
for i,x in enumerate(req):
    placed=x if fr is None else max(x,fr+1)
    tot+=placed-x; fr=placed
    why="It is the first request, so it keeps its value." if i==0 else (f"It is not above the previous frontier, so it moves up to {placed}." if placed>x else f"It is above the previous frontier, so it keeps {x}.")
    st.append({"at":{"i":i},"vars":{"request":x,"placed":placed,"frontier":fr,"totalMoves":tot},"note":f"Request {x}. {why} The frontier is {fr} and the total moves so far are {tot}."})
assert tot==6 and "keeps 7" in st[-1]["note"]
fill(CH,F,block(req,["i"],st),"@@TRACE1@@")
people=[[7,0],[4,4],[7,1],[5,0],[6,1],[5,2]]
people=[[2,4],[6,0],[3,2],[3,0],[4,2],[5,0]]
o=sorted(people,key=lambda p:(p[0],-p[1])); line=[None]*len(o); st=[]
for i,p in enumerate(o):
    empty=-1
    for at in range(len(line)):
        if line[at] is None:
            empty+=1
            if empty==p[1]: line[at]=p; break
    s=" ".join("_" if x is None else f"{x[0]}/{x[1]}" for x in line)
    st.append({"at":{"i":i},"vars":{"person":f"{p[0]}/{p[1]}","slot":at,"line":s},"note":f"Place {p[0]}/{p[1]} in the empty position that has {p[1]} empty positions before it, which is position {at}. The line is now {s}."})
assert line==[[3,0],[5,0],[3,2],[6,0],[2,4],[4,2]]
fill(CH,F,block([f"{h}/{k}" for h,k in o],["i"],st),"@@TRACE2@@")
