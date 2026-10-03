from common import *
def chain(vals,nxt,head,limit=40):
    out=[];i=head;n=0
    while i is not None and i!=-1 and n<limit:
        out.append(str(vals[i]));i=nxt[i];n+=1
    return ">".join(out) if out else "empty"
