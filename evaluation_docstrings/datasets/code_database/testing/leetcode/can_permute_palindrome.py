from collections import defaultdict


class Solution(object):
    def canPermutePalindrome(self, s):
        len_s = len(s)

        if len_s == 1:
            return True

        H = defaultdict(int)

        for i in range(len_s):
            H[s[i]] += 1

        even_letters = 0
        for k, v in H.items():
            if v % 2 == 0:
                even_letters += 1

        if even_letters >= len(H) - 1:
            return True
        else:
            return False
