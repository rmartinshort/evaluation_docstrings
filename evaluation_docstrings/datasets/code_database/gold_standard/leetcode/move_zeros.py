class Solution(object):
    def moveZeroes(self, nums):
        """
        :type nums: List[int]
        :rtype: None Do not return anything, modify nums in-place instead.
        """

        # [1,4,0,3,0,2,0,0,4,7,0,9]

        ln = len(nums)
        last_non_zero_position = 0
        # A better approach where we don't need to save elements in
        # another array. This is just the realization that the non-zero elements need to be next
        # to each other
        # for i in range(ln):
        #     if nums[i] != 0:
        #         nums[last_non_zero_position] = nums[i]
        #         last_non_zero_position += 1

        # for i in range(last_non_zero_position,ln):
        #     nums[i] = 0

        # or, if we realize that all the elements between i and last_non_zero_position will be zero, we can do
        for i in range(ln):
            if nums[i] != 0:
                nums[i], nums[last_non_zero_position] = (
                    nums[last_non_zero_position],
                    nums[i],
                )
                last_non_zero_position += 1
