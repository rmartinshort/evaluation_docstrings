from collections import defaultdict


class FirstUnique(object):
    def __init__(self, nums):
        """
        :type nums: List[int]
        """

        self.Q = nums
        self.first_unique_index = 0
        self.S = self.determineNOccur(self.Q)
        self.lenQ = len(self.Q)
        self.first_unique_index = self.determineFirstUnique()

    def determineNOccur(self, Q):
        H = defaultdict(int)
        for v in self.Q:
            H[v] += 1

        return H

    def determineFirstUnique(self):
        index = self.first_unique_index

        while (index < self.lenQ) and (self.S[self.Q[index]]) > 1:
            index += 1

        return index

    def showFirstUnique(self):
        """
        :rtype: int
        """

        self.first_unique_index = self.determineFirstUnique()

        if self.first_unique_index == self.lenQ:
            return -1
        else:
            return self.Q[self.first_unique_index]

    def add(self, value):
        """
        :type value: int
        :rtype: None
        """

        self.Q.append(value)
        self.S[value] += 1
        self.lenQ += 1
