from ll import *
CH='14-linked-lists'
F='01-node-invariants.md'
vals=[4,7,1,9]
steps=[];cnt=0;tot=0
for i,v in enumerate(vals):
    steps.append({"at":{"head":0,"cur":i},"vars":{"count":cnt,"sum":tot},"note":f"The reference cur names the node holding {v}, which has not been counted yet. It is counted, then cur follows its next reference."})
    cnt+=1;tot+=v
steps.append({"at":{"head":0,"cur":4},"vars":{"count":cnt,"sum":tot},"note":"The reference cur is null, so the loop ends. The list was only read, and the head still names the first node."})
assert cnt==4 and tot==21
fill(CH,F,block(vals,["head","cur"],steps),"@@TRACE1@@")
vals2=[4,7,1,9,5]
nxt=[1,2,3,None,None]
s=[]
s.append({"at":{"node":1,"fresh":4},"vars":{"main_chain":chain(vals2,nxt,0),"fresh_chain":chain(vals2,nxt,4)},"note":"A new node holding 5 exists but nothing points to it, and its next reference is null. The chain still reads 4, 7, 1, 9."})
s.append({"at":{"node":1,"fresh":4},"vars":{"saved":"1","main_chain":chain(vals2,nxt,0),"fresh_chain":chain(vals2,nxt,4)},"note":"The old successor of the node holding 7, which holds 1, is saved in a local reference before any link changes."})
nxt[4]=nxt[1]
s.append({"at":{"node":1,"fresh":4},"vars":{"saved":"1","main_chain":chain(vals2,nxt,0),"fresh_chain":chain(vals2,nxt,4)},"note":"The new node now points to the saved successor, so it can reach 1 and 9 without help from the main chain."})
nxt[1]=4
s.append({"at":{"node":1,"fresh":4},"vars":{"saved":"1","main_chain":chain(vals2,nxt,0),"fresh_chain":chain(vals2,nxt,4)},"note":"The node holding 7 now points to the new node. The chain reads 4, 7, 5, 1, 9 and every node is still reachable from the head."})
assert chain(vals2,nxt,0)=="4>7>5>1>9"
fill(CH,F,block(vals2,["node","fresh"],s),"@@TRACE2@@")
