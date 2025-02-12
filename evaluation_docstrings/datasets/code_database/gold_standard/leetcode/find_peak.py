class Solution(object):
    def findPeakElement(self, nums):
        """

        Approach
        like a binary search

        peak is where nums[i]>nums[i-1] and nums[i]>nums[i+1]
        if i == 0, its peak if nums[i]<nums[1]
        if i == len(nums)-1, peak if nums[i]>nums[i-1]
        if len(nums) == 1, peak is at nums[0]

        if thats not true, decide which direction we need to move towards the peak
        if nums[i]>nums[i-1] and nums[i]<nums[i+1], then we need to move right
        if nums[i]<nums[i-1] and nums[i]>nums[i+1], then we need to move left

        :type nums: List[int]
        :rtype: int
        """

        max_index = len(nums) - 1
        left = 0
        right = len(nums) - 1

        if right == 0:
            return right

        while left <= right:
            mid = (left + right) // 2
            print(mid)
            # handle edge cases
            if mid == 0:
                # we're at the beginning
                if nums[mid] > nums[mid + 1]:
                    return mid
                else:
                    left = mid + 1

            elif mid == max_index:
                # we're at the end
                if nums[mid] > nums[mid - 1]:
                    return mid
                else:
                    right = mid - 1
            # normal case
            else:
                # not an edge case
                if (nums[mid] > nums[mid - 1]) and (nums[mid] > nums[mid + 1]):
                    return mid

                elif nums[mid] > nums[mid - 1]:
                    # we need to go up the slope
                    left = mid + 1
                else:
                    # we need to go down the slope
                    right = mid - 1
