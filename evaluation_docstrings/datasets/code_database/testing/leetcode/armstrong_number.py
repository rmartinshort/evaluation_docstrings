class Solution(object):
    def isArmstrong(self, n):
        ndigits = [int(c) for c in str(n)]
        k = len(ndigits)
        n_sum = sum([float(d) ** k for d in str(n)])
        return n_sum == n
