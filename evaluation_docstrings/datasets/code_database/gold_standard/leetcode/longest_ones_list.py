class Solution(object):
    def longestOnes(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        # Approach
        # find the maximum subarray that has k zeros only
        # we can do this by counting the budget of zeros that we have

        zeros_budget = k
        p0 = 0

        for p1 in range(len(nums)):
            if nums[p1] == 0:
                zeros_budget -= 1

            if zeros_budget < 0:
                # start advancing p0 until zeros budget goes above 0
                # if we see a 0 in nums p0, then we can append to the zeros budget
                # since we will be moving the p0 up
                if nums[p0] == 0:
                    zeros_budget += 1
                p0 += 1

        return p1 - p0 + 1
