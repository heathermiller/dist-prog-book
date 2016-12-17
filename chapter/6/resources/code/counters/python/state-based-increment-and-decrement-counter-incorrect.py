class CvRDT:
    pass

class Counter(CvRDT):

    def __init__(self, counts = None):  # constructor function
        if counts is None:
            self._counts = [0] * length(self.replicas())
        else:
            self._counts = counts

    def value(self):                    # query function
        return sum(self._counts)

    def counts(self):                   # query function
        return list(self._counts)       # return a clone

    def increment(self):                # update function
        self._counts[self.replicaId()] += 1

    def decrement(self):                # update function
        self._counts[self.replicaId()] -= 1

    def compare(self, other):           # comparison function
        return all(v1 <= v2 for (v1, v2) in
                   zip(self.counts(),
                       other.counts()))

    def merge(self, other):             # merge function
        return Counter(map(max, zip(self.counts(),
                                    other.counts())))
