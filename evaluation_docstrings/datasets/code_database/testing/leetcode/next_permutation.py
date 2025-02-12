class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        def swap(nums, p1, p2):
            nums[p1], nums[p2] = nums[p2], nums[p1]

        def reverse(nums, start):
            p0 = len(nums) - 1
            p1 = start
            while p0 > p1:
                swap(nums, p0, p1)
                p0 -= 1
                p1 += 1

        p1 = len(nums) - 2
        # count backwards until we fid that nums[p1] < nums[p1+1]
        # [5,4,3,2,1] -> decreasing order so no next permutation, just sort
        # first we count back until we fnd an element thats smaller than p+1
        # then we count back again until we find the first element thats larger than the above
        # then we swap them
        # then we reverse the remainder of the array
        # [1,5,8,4,7,6,5,3,1] -> [1,5,8,5,7,6,4,3,1] -> [1,5,8,5,1,3,4,6,7]

        while p1 >= 0 and (nums[p1] >= nums[p1 + 1]):
            p1 -= 1

        if p1 >= 0:
            p2 = len(nums) - 1
            # count backwards util we find nums[p2] > nums[p1]
            while nums[p2] <= nums[p1]:
                p2 -= 1
            swap(nums, p1, p2)

        reverse(nums, p1 + 1)
