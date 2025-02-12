class Solution:
    def findMaxConsecutiveOnes(self, nums: List[int]) -> int:
        max_len = 0
        p1, p2 = 0, 0
        ln = len(nums)
        count_zero = 0
        while (p2 < ln) and (p1 <= p2):
            if nums[p2] == 0:
                count_zero += 1

            while count_zero == 2:
                if nums[p1] == 0:
                    count_zero -= 1
                p1 += 1

            max_len = max(max_len, p2 - p1 + 1)
            p2 += 1

        return max_len
