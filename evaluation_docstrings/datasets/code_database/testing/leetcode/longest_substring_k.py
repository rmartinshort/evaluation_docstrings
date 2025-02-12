from collections import defaultdict


class Solution:
    def lengthOfLongestSubstringKDistinct(self, s: str, k: int) -> int:
        H = defaultdict(int)
        ln = len(s)
        current_len = 0
        # this is the running sum of the values in the dict
        running_sum_len = 0
        l = 0

        for i in range(ln):
            candidate = s[i]
            H[candidate] += 1
            running_sum_len += 1

            while len(H) > k:
                # if too long, start to reduce
                H[s[l]] -= 1
                # if get to zero, remove
                if H[s[l]] == 0:
                    del H[s[l]]
                # subtract from running sum
                running_sum_len -= 1
                l += 1

            # print(H, running_sum_len)
            current_len = max(running_sum_len, current_len)

        return current_len
