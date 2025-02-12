class Solution:
    def largestAltitude(self, gain: List[int]) -> int:
        """
        This can be done with a prefix sum
        """

        pfs = 0
        max_alt = 0
        for i in range(1, len(gain) + 1):
            pfs = gain[i - 1] + pfs
            max_alt = max(max_alt, pfs)

        return max_alt
