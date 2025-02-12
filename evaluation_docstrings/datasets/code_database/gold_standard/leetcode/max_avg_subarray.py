class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        """
        This is the same as finding the max of a subarray of length k
        we can move along and consider the sum by adding the next element and subtracting the first
        """

        this_sum = sum(nums[:k])
        max_sum = this_sum
        for i in range(len(nums) - k):
            # add the next element
            this_sum += nums[i + k]
            # subtract the first element
            this_sum -= nums[i]
            # compare
            max_sum = max(max_sum, this_sum)

        return max_sum / k
