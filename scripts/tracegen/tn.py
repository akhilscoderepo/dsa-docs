# helpers for trie traces: a tiny character trie that records pass counts and flags
class Trie:
    def __init__(self):
        self.kids = [{}]; self.pass_ = [0]; self.term = [False]
    def size(self): return len(self.kids)
    def insert(self, word, narrate=True):
        """inserts word, returns the list of trace steps (one per letter plus the ending step)."""
        steps = []; cur = 0; self.pass_[0] += 1
        for i, ch in enumerate(word):
            if ch in self.kids[cur]:
                cur = self.kids[cur][ch]; made = False
            else:
                self.kids.append({}); self.pass_.append(0); self.term.append(False)
                self.kids[cur][ch] = len(self.kids) - 1; cur = self.kids[cur][ch]; made = True
            self.pass_[cur] += 1
            note = (f"The letter {ch} has no edge yet, so a new node is made for the beginning {word[:i+1]} and the walk moves onto it." if made
                    else f"The letter {ch} already has an edge, so the walk moves onto the existing node for {word[:i+1]} and its pass count rises to {self.pass_[cur]}.")
            steps.append({"at": {"i": i}, "vars": {"nodes": self.size(), "pass": self.pass_[cur], "made": "yes" if made else "no"}, "note": note})
        self.term[cur] = True
        steps.append({"at": {"i": len(word)}, "vars": {"nodes": self.size(), "pass": self.pass_[cur], "made": "no"}, "note": f"The word {word} ends here, so the flag of this node is set and the trie holds {self.size()} nodes with the root."})
        return steps
    def walk(self, s):
        cur = 0
        for ch in s:
            if ch not in self.kids[cur]: return None
            cur = self.kids[cur][ch]
        return cur
