from common import *
CH='08-two-pointers'
F='10-index-state-and-floyd.md'

def run(nums):
    st=[]
    walker=runner=0; r=0
    while True:
        walker=nums[walker]; runner=nums[nums[runner]]; r+=1
        if walker==runner:
            note=f"Meeting round {r}: the walker is on index {walker} and the runner, after two links, is on index {runner}. They coincide, so the meeting phase ends after {r} rounds."
        else:
            note=f"Meeting round {r}: the walker moves to index {walker} and the runner moves two links to index {runner}. They are apart."
        st.append({"at":{"walker":walker,"runner":runner,"returner":-1},"vars":{"phase":"meeting","rounds":r},"note":note})
        if walker==runner: break
    meet_rounds=r
    st.append({"at":{"walker":walker,"runner":-1,"returner":0},"vars":{"phase":"entry","tail":0},"note":f"The entry phase starts. The walker stays on index {walker}, and the returner starts at index 0. Both will move one link per round."})
    returner=0; tail=0
    while returner!=walker:
        returner=nums[returner]; walker=nums[walker]; tail+=1
        if returner==walker:
            note=f"Entry round {tail}: both land on index {returner}. This is the shared value, and the tail is {tail}."
        else:
            note=f"Entry round {tail}: the returner moves to index {returner} and the walker to index {walker}. They are apart."
        st.append({"at":{"walker":walker,"runner":-1,"returner":returner},"vars":{"phase":"entry","tail":tail},"note":note})
    entry=walker
    cyc=0; probe=entry
    st.append({"at":{"walker":entry,"runner":-1,"returner":-1},"vars":{"phase":"lap","cycle":0},"note":f"The lap starts on the entry, index {entry}. The walker will count links until it is back here."})
    while True:
        probe=nums[probe]; cyc+=1
        note=f"Lap link {cyc}: the walker reaches index {probe}." + (" That is the entry again, so the ring size is " + str(cyc) + "." if probe==entry else "")
        st.append({"at":{"walker":probe,"runner":-1,"returner":-1},"vars":{"phase":"lap","cycle":cyc},"note":note})
        if probe==entry: break
    return st,(entry,tail,cyc),meet_rounds

def oracle(nums):
    first={}; i=0; s=0
    while i not in first:
        first[i]=s; i=nums[i]; s+=1
    return (i,first[i],s-first[i])

a=[2,5,1,1,4,3]
s,tri,mr=run(a); assert tri==oracle(a)==(1,2,3) and mr==3
fill(CH,F,block(a,["walker","runner","returner"],s),"@@TRACE1@@")
b=[3,1,3,2]
s,tri,mr=run(b); assert tri==oracle(b)==(3,1,2) and mr==2
fill(CH,F,block(b,["walker","runner","returner"],s),"@@TRACE2@@")
