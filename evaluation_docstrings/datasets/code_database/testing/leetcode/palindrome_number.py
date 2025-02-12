class Solution:
    def isPalindrome(self, x):
        str_x = str(x)
        p0 = 0
        p1 = len(str_x) - 1

        while p0 < p1:
            if str_x[p0] != str_x[p1]:
                return False
            p0 += 1
            p1 -= 1

        return True
