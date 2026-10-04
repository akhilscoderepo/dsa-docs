from common import *
CH='18-tries'
F='05-binary-tries.md'
W = 5

class BT:
    def __init__(self):
        self.kid = [[None, None]]
    def size(self): return len(self.kid)
    def bits(self, v): return [(v >> b) & 1 for b in range(W - 1, -1, -1)]
    def insert(self, v, steps=None):
        cur = 0; bs = self.bits(v)
        for i, bit in enumerate(bs):
            made = self.kid[cur][bit] is None
            if made:
                self.kid.append([None, None]); self.kid[cur][bit] = len(self.kid) - 1
            cur = self.kid[cur][bit]
            if steps is not None:
                pre = "".join(map(str, bs[:i + 1]))
                note = (f"The bit {bit} has no edge below the node for {pre[:-1] or 'the root'}, so a new node is created for {pre}." if made
                        else f"The bit {bit} already has an edge, so the walk moves onto the existing node for {pre}.")
                steps.append({"at": {"b": i}, "vars": {"nodes": self.size(), "made": "yes" if made else "no"}, "note": note})
        if steps is not None:
            steps.append({"at": {"b": W}, "vars": {"nodes": self.size(), "made": "no"}, "note": f"All {W} bits are placed, so this value ends at its own leaf and the trie holds {self.size()} nodes with the root."})
    def best(self, x, steps):
        cur = 0; score = 0; bs = self.bits(x); partner = []
        for i, bit in enumerate(bs):
            want = 1 - bit
            if self.kid[cur][want] is not None:
                score |= 1 << (W - 1 - i); cur = self.kid[cur][want]; partner.append(want)
                note = f"The query bit is {bit}, so the wanted bit is {want}. That branch exists, so it is taken and the result gains {1 << (W - 1 - i)}."
            else:
                cur = self.kid[cur][bit]; partner.append(bit)
                note = f"The query bit is {bit}, so the wanted bit is {want}. That branch is missing, so the walk takes {bit} and the result gains nothing here."
            steps.append({"at": {"b": i}, "vars": {"want": want, "score": score}, "note": note})
        return score, int("".join(map(str, partner)), 2)

t = BT()
t.insert(6); t.insert(12)
assert t.size() == 10
s1 = []
t.insert(9, s1)
assert t.size() == 13
fill(CH, F, block(list("01001"), ["b"], s1), "@@TRACE1@@")
t2 = BT()
for v in (6, 12, 30, 17): t2.insert(v)
s2 = []
sc, partner = t2.best(9, s2)
assert sc == 24 == (9 ^ partner) and partner == 17
fill(CH, F, block(list("01001"), ["b"], s2), "@@TRACE2@@")
