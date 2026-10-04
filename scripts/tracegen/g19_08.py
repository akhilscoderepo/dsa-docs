from common import *
CH='19-recursion-and-backtracking'; F='08-proof-based-pruning.md'
w=[2,3,5,6]; limit=8; path=[]; steps=[]; calls=[0]
def load(start,room):
    calls[0]+=1
    steps.append({"at":{"start":start,"i":-1},"vars":{"path":str(path),"room":room,"calls":calls[0]},"note":f"The call arrives with the load {path}, and {room} of weight can still be added, so the load fits and is recorded."})
    for i in range(start,len(w)):
        if w[i]>room:
            steps.append({"at":{"start":start,"i":i},"vars":{"path":str(path),"room":room,"calls":calls[0]},"note":f"The crate of weight {w[i]} is more than the {room} left, and every later crate is heavier, so the loop stops here."})
            break
        path.append(w[i])
        steps.append({"at":{"start":start,"i":i},"vars":{"path":str(path),"room":room-w[i],"calls":calls[0]},"note":f"The crate of weight {w[i]} fits, so it goes on the cart and {room-w[i]} of room remains."})
        load(i+1,room-w[i])
        path.pop()
        steps.append({"at":{"start":start,"i":i},"vars":{"path":str(path) if path else "empty","room":room,"calls":calls[0]},"note":f"The crate of weight {w[i]} comes off again, so the path is {path if path else 'empty'} and {room} of room is back."})
load(0,limit)
assert calls[0]==9
fill(CH,F,block([str(x) for x in w],["start","i"],steps),"@@TRACE1@@")
# trace 2: wrong prune with a negative value
v=[5,-5]; target=0; path=[]; steps=[]; found=[0]
def go(start,total):
    if total==target:
        found[0]+=1
        steps.append({"at":{"start":start,"i":-1},"vars":{"path":str(path),"sum":total,"lost":"no"},"note":f"The call arrives with the path {path} summing to {total}, which is the target, so it is counted."})
    else:
        steps.append({"at":{"start":start,"i":-1},"vars":{"path":str(path),"sum":total,"lost":"no"},"note":f"The call arrives with the path {path} summing to {total}, which is not the target."})
    for i in range(start,len(v)):
        path.append(v[i])
        s=total+v[i]
        if s>target:
            steps.append({"at":{"start":start,"i":i},"vars":{"path":str(path),"sum":s,"lost":"yes"},"note":f"The sum {s} is above the target, so the careless rule abandons the branch, but the value -5 is still to come and would bring the sum back to 0, so a real answer is lost."})
            path.pop()
            continue
        steps.append({"at":{"start":start,"i":i},"vars":{"path":str(path),"sum":s,"lost":"no"},"note":f"The value {v[i]} is taken, so the sum is {s}."})
        go(i+1,s)
        path.pop()
        steps.append({"at":{"start":start,"i":i},"vars":{"path":str(path) if path else "empty","sum":total,"lost":"no"},"note":f"The value {v[i]} is removed, so the sum is {total} again."})
go(0,0)
assert found[0]==1
fill(CH,F,block([str(x) for x in v],["start","i"],steps),"@@TRACE2@@")
