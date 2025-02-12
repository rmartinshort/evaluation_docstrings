from collections import defaultdict


class Solution:
    def twoSum(self, nums, target):
        H = defaultdict(int)
        for i, n in enumerate(nums):
            H[target - n] = i

        for i, n in enumerate(nums):
            if n in H and H[n] != i:
                return [i, H[n]]
