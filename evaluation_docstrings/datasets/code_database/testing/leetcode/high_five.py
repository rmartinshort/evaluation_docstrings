from collections import defaultdict
import heapq


class Solution(object):
    def highFive(self, items):
        H = defaultdict(list)
        for element in items:
            H[element[0]].append(-element[1])

        op = []
        for k, v in H.items():
            heapq.heapify(v)
            count = 0
            sum_max = 0
            while v and count < 5:
                max_val = -heapq.heappop(v)
                sum_max += max_val
                count += 1
            op.append([k, sum_max // count])

        return op
