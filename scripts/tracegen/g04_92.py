from common import *
CH='04-hash-maps-and-sets'
def run(cells, ph, expect):
    rows=[set() for _ in range(9)];cols=[set() for _ in range(9)];bx=[set() for _ in range(9)]
    S=lambda s:"{"+",".join(map(str,sorted(s)))+"}"
    st=[{"at":{"i":-1},"vars":{},"note":"Start: all 27 sets are empty."}]; ok=True
    for i,(r,c,d) in enumerate(cells):
        b=r//3*3+c//3
        v={"cell":f"({r},{c})={d}","row":S(rows[r]),"col":S(cols[c]),"box":f"{b}:{S(bx[b])}"}
        bad=[n for n,s in (("row",rows[r]),("column",cols[c]),("block",bx[b])) if d in s]
        if bad:
            st.append({"at":{"i":i},"vars":v,"note":f"Digit {d} is already in the {bad[0]} set of this cell, so the board is illegal."}); ok=False; break
        rows[r].add(d);cols[c].add(d);bx[b].add(d)
        st.append({"at":{"i":i},"vars":v,"note":f"Digit {d} is new in row {r}, column {c} and block {b}. Add it to all three sets."})
    if ok: st.append({"at":{"i":len(cells)},"vars":{},"note":"Every filled cell passed, so the board is legal."})
    assert ok==expect
    fill(CH,'92-matrices-and-sets.md',block([f"({r},{c})={d}" for r,c,d in cells],["i"],st),ph)
run([(0,0,5),(0,3,7),(1,0,6),(2,5,9),(4,4,5)],"@@TRACE1@@",True)
run([(0,0,5),(1,4,3),(2,2,5)],"@@TRACE2@@",False)
