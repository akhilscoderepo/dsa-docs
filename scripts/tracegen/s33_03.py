from common import *
CH='33-design-data-structure-problems'; F='03-constant-time-composition.md'
def run(vals, v):
    vals=list(vals); pos={x:i for i,x in enumerate(vals)}
    n=len(vals)
    def st(slot,last,vars_,note): return {"at":{"slot":slot,"last":last},"vars":vars_,"note":note}
    s=[]
    def snap(extra=None):
        d={"values":str(vals).replace(" ",""),"slotOf":",".join(f"{k}:{pos[k]}" for k in vals)}
        if extra: d.update(extra)
        return d
    slot=pos[v]; lastslot=n-1; last=vals[-1]
    s.append(st(-1,-1,snap(),f"Start. The list holds {vals} and slotOf maps each value to its position. The call is remove({v})."))
    s.append(st(slot,lastslot,snap({"slot":slot,"last":last}),f"slotOf.get({v}) gives slot {slot}. The final value is {last}, stored at position {lastslot}."))
    vals[slot]=last
    s.append(st(slot,lastslot,snap({"slot":slot,"last":last}),f"Copy {last} into slot {slot}. The list now reads {vals}, so a value is stored twice for a moment."))
    pos[last]=slot
    s.append(st(slot,lastslot,snap({"slot":slot,"last":last}),f"Repair: slotOf.put({last}, {slot}). The entry for {last} now names slot {slot}."))
    del pos[v]
    # note: if v == last the entry for v is gone now
    s.append(st(slot,lastslot,{"values":str(vals).replace(" ",""),"slotOf":",".join(f"{k}:{pos[k]}" for k in sorted(pos,key=lambda k:pos[k]))},f"Delete the entry for {v}. "+("It was also the final value, so the repair write disappears with it." if v==last else f"Only the entry for {v} is removed.")))
    vals.pop()
    moved=-1 if v==last else last
    s.append(st(slot if slot<len(vals) else len(vals),len(vals)-1 if vals else -1,{"values":str(vals).replace(" ",""),"slotOf":",".join(f"{k}:{pos[k]}" for k in sorted(pos,key=lambda k:pos[k])),"moved":moved},f"Drop the final position. The list reads {vals} and the call returns {moved}."))
    assert sorted(pos)==sorted(vals) and all(vals[pos[k]]==k for k in pos)
    return s,vals,moved
a=[40,17,93,52,8]
s,v,m=run(a,17); assert v==[40,8,93,52] and m==8
fill(CH,F,block(a,["slot","last"],s),"@@TRACE1@@")
s,v,m=run(a,8); assert v==[40,17,93,52] and m==-1
fill(CH,F,block(a,["slot","last"],s),"@@TRACE2@@")
