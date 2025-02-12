class Solution(object):
    def removeElement(self, nums, val):
        """
        :type nums: List[int]
        :type val: int
        :rtype: int
        """

        ln = len(nums)

        new_length = ln
        i = 0

        while i < new_length:
            if nums[i] == val:
                # Don't advance i if this is the case!
                nums[i] = nums[new_length - 1]
                new_length -= 1
            else:
                i += 1

        return new_length
