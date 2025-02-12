class Solution(object):
    def find_pivot_index(self, nums):
        ln = len(nums)
        left = 0
        right = ln - 1

        if nums[left] < nums[right]:
            # the array has not been pivoted
            return 0

        while left <= right:
            mid = (left + right) // 2
            # we have found the pivot point
            if nums[mid] > nums[mid + 1]:
                return mid + 1
            else:
                # implies pivot is to the left of mid
                # since otherwise mid > left
                if nums[mid] < nums[left]:
                    right = mid - 1
                # implies pivot is to the right of mid
                else:
                    left = mid + 1

    def search(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """

        # Approach
        # find the rotation index (the smallest element in the array)
        # binary search in the correct part of the sorted array

        def _bin_search(left, right):
            while left <= right:
                mid = (left + right) // 2
                if nums[mid] == target:
                    return mid
                elif nums[mid] > target:
                    # target lies in the left part
                    right = mid - 1
                else:
                    # target lies in the right part
                    left = mid + 1

            return -1

        ln = len(nums)
        if ln == 1:
            return 0 if nums[0] == target else -1

        piv_index = self.find_pivot_index(nums)

        if nums[piv_index] == target:
            return piv_index
        elif piv_index == 0:
            # pivot is 0, search entire array
            return _bin_search(0, ln - 1)
        elif nums[0] > target:
            # implies value is to the right of the pivot
            return _bin_search(piv_index, ln - 1)
        else:
            # implies value is to the left of the pivot
            return _bin_search(0, piv_index)
