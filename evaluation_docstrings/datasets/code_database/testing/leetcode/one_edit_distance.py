class Solution(object):
    def isOneEditDistance(self, s, t):
        len_t = len(t)
        len_s = len(s)

        if len_s > len_t:
            return self.isOneEditDistance(t, s)

        if len_t > len_s + 1:
            return False

        for i in range(len_s):
            # if the chars are not the same
            if s[i] != t[i]:
                # if the strings are the same length
                if len_s == len_t:
                    # check of everything beyond that is the same
                    return s[i + 1 :] == t[i + 1 :]
                # if the strings are not the same length
                else:
                    # check of everything after that char in t (the longer one) is the same
                    return s[i:] == t[i + 1 :]

        # if we're here, then the strings are only one edit away if t has one more char than s
        return len_s + 1 == len_t
