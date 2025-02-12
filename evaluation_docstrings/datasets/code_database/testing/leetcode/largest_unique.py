from collections import defaultdict


class Solution(object):
    def largestUniqueNumber(self, nums):
        largest_non_repeat = -float("inf")
        H = defaultdict(int)

        # count the number of times each element appears
        for element in nums:
            H[element] += 1

        # pass again and consider only the elements that occured once
        for k, v in H.items():
            if (v == 1) and (k > largest_non_repeat):
                largest_non_repeat = k

        if largest_non_repeat == -float("inf"):
            return -1
        else:
            return largest_non_repeat
