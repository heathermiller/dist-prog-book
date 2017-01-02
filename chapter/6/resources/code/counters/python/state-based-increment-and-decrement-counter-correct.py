class CvRDT:
    pass

class Counter(CvRDT):

    def __init__(self,
                 increments = None,
                 decrements = None):   # constructor function
        if increments is None:
            self._increments = [0] * length(replicas())
        else:
            self._increments = increments
        if decrements is None:
            self._decrements = [0] * length(replicas())
        else:
            self._decrements = decrements

    def increments(self):               # query function
        return list(self._increments)   # return a clone

    def decrements(self):               # query function
        return list(self._decrements)   # return a clone

    def value(self):                    # query function
        return (sum(self.increments()) -
                sum(self.decrements()))

    def increment(self):                # update function
        self._increments[self.replicaId()] += 1

    def decrement(self):                # update function
        self._decrements[self.replicaId()] += 1

    def compare(self, other):           # comparison function
        return (all(v1 <= v2 for (v1, v2) in
                    zip(self.increments(),
                        other.increments()))
                and
                all(v1 <= v2 for (v1, v2) in
                    zip(self.decrements(),
                        other.decrements())))

    def merge(self, other):             # merge function
        return Counter(increments = map(max, zip(self.increments(),
                                                 other.increments())),
                       decrements = map(max, zip(self.decrements(),
                                                 other.decrements())))
