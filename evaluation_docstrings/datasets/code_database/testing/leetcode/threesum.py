class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        """
        For each value, we can do a check to see which of the subsequent
        values add up to 0

        if we sort the array, we can skip any duplicates
        """

        res = []
        nums.sort()

        for i in range(len(nums)):
            candidate = nums[i]
            if i > 0 and candidate == nums[i - 1]:
                continue

            # pointers for left and right
            left = i + 1
            right = len(nums) - 1
            while left < right:
                candidate_sum = candidate + nums[left] + nums[right]
                if candidate_sum == 0:
                    res.append([candidate, nums[left], nums[right]])
                    # advance the left pointer
                    left += 1
                    # avoid duplicates and keep going left if we find one
                    while (nums[left] == nums[left - 1]) and (left < right):
                        left += 1

                # we need to move right
                elif candidate_sum < 0:
                    left += 1
                # if we need to move left
                else:
                    right -= 1

        return res
