class CvRDT:
    pass

class Counter(CvRDT):

    def __init__(self, count = 0):  # constructor function
        self._count = count

    def value(self):                # query function
        return self._count

    def increment(self):            # update function
        self._count += 1

    def compare(self, other):       # comparison function
        return self.value() <= other.value()

    def merge(self, other):         # merge function
        return Counter(max(self.value(), other.value()))
