from common import *
from tn import *
CH='18-tries'
F='18-tries/01-prefix-nodes.md'
t=Trie()
s1=t.insert("car")
assert t.size()==4
fill(CH,'01-prefix-nodes.md',block(list("car"),["i"],s1),"@@TRACE1@@")
s2=t.insert("cat")
assert t.size()==5 and t.pass_[t.walk("ca")]==2 and t.term[t.walk("cat")] and not t.term[t.walk("ca")]
fill(CH,'01-prefix-nodes.md',block(list("cat"),["i"],s2),"@@TRACE2@@")
