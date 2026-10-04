from common import *
from tn import *
CH='18-tries'

def search_steps(trie, word, exact=True):
    """walks word through the trie; one step per letter and a verdict step. returns (steps, answer)."""
    steps = []; cur = 0
    for i, ch in enumerate(word):
        if ch not in trie.kids[cur]:
            steps.append({"at": {"i": i}, "vars": {"flag": "-", "found": "no"}, "note": f"The letter {ch} has no edge from the node for {word[:i]}, so the walk fails and the answer is no."})
            return steps, False
        cur = trie.kids[cur][ch]
        steps.append({"at": {"i": i}, "vars": {"flag": "set" if trie.term[cur] else "unset", "found": "yes"}, "note": f"The letter {ch} has an edge, so the cursor moves onto the node for {word[:i+1]}."})
    ans = trie.term[cur] if exact else True
    steps.append({"at": {"i": len(word)}, "vars": {"flag": "set" if trie.term[cur] else "unset", "found": "yes"}, "note": f"Every letter was matched, and the flag of the node for {word} is {'set' if trie.term[cur] else 'unset'}, so an exact question answers {'yes' if ans else 'no'}."})
    return steps, ans

if __name__ == '__main__':
    t=Trie(); t.insert("app")
    s1=t.insert("apple")
    assert t.size()==6 and t.pass_[t.walk("app")]==2
    fill(CH,'02-insert-and-search.md',block(list("apple"),["i"],s1),"@@TRACE1@@")
    s2,ans=search_steps(t,"appl")
    assert ans is False and t.walk("appl") is not None
    fill(CH,'02-insert-and-search.md',block(list("appl"),["i"],s2),"@@TRACE2@@")
