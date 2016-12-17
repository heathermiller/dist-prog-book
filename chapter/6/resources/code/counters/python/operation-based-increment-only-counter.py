class CmRDT:
    pass

class Counter(CmRDT):

    def __init__(self):         # constructor function
        self._count = 0

    def value(self):            # query function
        return self._count

    def increment(self):        # update function
        self._count += 1
        for replica in self.replicas():
            self.transmit("increment", replica)
