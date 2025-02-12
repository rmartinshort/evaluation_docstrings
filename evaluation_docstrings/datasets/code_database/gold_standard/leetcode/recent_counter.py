from collections import deque


class RecentCounter(object):
    def __init__(self):
        self.recent_requests = deque([])

    def ping(self, t):
        """
        :type t: int
        :rtype: int
        """

        # remove old values if they don't meet the criteria
        # note that popleft will remove the first value in the queue, pop will remove the last one
        while self.recent_requests and self.recent_requests[0] < (t - 3000):
            removed_value = self.recent_requests.popleft()

        self.recent_requests.append(t)
        return len(self.recent_requests)
