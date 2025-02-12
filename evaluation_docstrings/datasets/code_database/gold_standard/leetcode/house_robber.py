from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        """
        Need to decide which to rob
        i.e. we rob the current house and the i+2 house OR we rob the i+1 house
        will be based on max(money[current] + rob[i+2], rob[i+1])
        """

        N = len(nums)
        robbed_amount = [None for _ in range(N + 1)]

        # base case where we have 0 and nums[-1] in the robbed amount list
        # go from the end and then apply the recurrence relation
        robbed_amount[N] = 0
        robbed_amount[N - 1] = nums[-1]

        # count backwards and fill from the end
        for i in range(N - 2, -1, -1):
            robbed_amount[i] = max(nums[i] + robbed_amount[i + 2], robbed_amount[i + 1])

        return robbed_amount[0]
