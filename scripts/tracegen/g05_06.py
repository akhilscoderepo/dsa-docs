from common import *
CH='05-sorting-and-java-comparators'; N='06-sort-and-sweep.md'
def run(vals,ph,tail):
    s=sorted(vals); fr=None; cost=0
    st=[{"at":{"i":-1},"vars":{"frontier":"none","moves":0},"note":"Start: no slot is taken, so the frontier is below every request."}]
    for i,a in enumerate(s):
        taken=a if fr is None else max(a,fr)
        cost+=taken-a; fr=taken+1
        why="The frontier is not above the request, so the request keeps its slot." if taken==a else "The frontier is above the request, so the request moves up to the frontier."
        st.append({"at":{"i":i},"vars":{"asked":a,"taken":taken,"frontier":fr,"moves":cost},"note":f"{why} The frontier becomes {fr}."})
    st.append({"at":{"i":len(s)},"vars":{"frontier":fr,"moves":cost},"note":tail.format(cost)})
    fill(CH,N,block(s,["i"],st),ph); return cost
assert run([5,2,5,5],"@@TRACE1@@","The pass ends with {} moves in total.")==3
assert run([0,0,0,0,10],"@@TRACE2@@","The pass ends with {} moves in total.")==6
