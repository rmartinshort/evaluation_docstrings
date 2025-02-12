class Solution:
    def shortestWay(self, source, target):
        i = 0
        answer = 0
        while i < len(target):
            can_form = False

            # for every char in target, see if its in source
            for ch in source:
                # Can form a minimum subsequence of target
                if ch == target[i]:
                    can_form = True
                    i += 1
                    if i == len(target):
                        return answer + 1

            if can_form:
                answer += 1
            # Couldn't form a subsequence, return early.
            else:
                return -1
