# Java-faithful binary heap simulation (matches java.util.PriorityQueue siftUp/siftDown) for chapter 17 traces.
fmt = lambda l: "[" + ",".join(map(str, l)) + "]"


class Heap:
    def __init__(self, key=lambda x: x):
        self.a = []
        self.key = key

    def less(self, x, y):
        return self.key(x) < self.key(y)

    def offer(self, v):
        a = self.a
        a.append(v)
        k = len(a) - 1
        swaps = []
        while k > 0:
            p = (k - 1) >> 1
            if not self.less(v, a[p]):
                break
            a[k] = a[p]
            swaps.append((k, p))
            k = p
        a[k] = v
        return swaps, k

    def poll(self):
        a = self.a
        top = a[0]
        last = a.pop()
        path = []
        if a:
            n = len(a)
            k = 0
            while True:
                c = 2 * k + 1
                if c >= n:
                    break
                if c + 1 < n and self.less(a[c + 1], a[c]):
                    c += 1
                if not self.less(a[c], last):
                    break
                a[k] = a[c]
                path.append((k, c))
                k = c
            a[k] = last
        return top, last, path

    def peek(self):
        return self.a[0]

    def __len__(self):
        return len(self.a)
