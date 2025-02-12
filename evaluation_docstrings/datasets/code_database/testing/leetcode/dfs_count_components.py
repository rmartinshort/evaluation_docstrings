from collections import defaultdict


class Solution(object):
    def countComponents(self, n, edges):
        """
        :type n: int
        :type edges: List[List[int]]
        :rtype: int
        """

        self.H = defaultdict(list)
        self.seen = set()

        for edge in edges:
            self.H[edge[0]].append(edge[1])
            self.H[edge[1]].append(edge[0])

        connected_components = 0

        def dfs(node):
            self.seen.add(node)
            for connected in self.H[node]:
                if connected not in self.seen:
                    dfs(connected)

        for node in range(n):
            if node not in self.seen:
                dfs(node)
                connected_components += 1

        return connected_components
