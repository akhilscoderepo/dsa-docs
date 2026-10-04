from common import *
CH='04-hash-maps-and-sets'
def run(cells, ph, expect):
    al=set(cells); best=(0,0); st=[]
    for i,x in enumerate(cells):
        if x-1 in al:
            st.append({"at":{"i":i},"vars":{"value":x,"start":"no","best":str(list(best))},"note":f"Value {x}: {x-1} is in the set, so {x} lies inside a run. Skip it."})
        else:
            ln=1
            while x+ln in al: ln+=1
            if ln>best[1] or (ln==best[1] and x<best[0]): best=(x,ln)
            st.append({"at":{"i":i},"vars":{"value":x,"start":"yes","best":str(list(best))},"note":f"Value {x}: {x-1} is missing, so {x} starts a run. The walk upward finds length {ln}. Best so far: start {best[0]}, length {best[1]}."})
    assert best==expect
    fill(CH,'05-set-sequences.md',block(cells,["i"],st),ph)
run([50,12,13,49,11,51,52,14],"@@TRACE1@@",(11,4))
distinct=list(dict.fromkeys([3,3,2,1,1,9]))
run(distinct,"@@TRACE2@@",(1,3))
