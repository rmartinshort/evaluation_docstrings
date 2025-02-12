class Solution:
    def minCost(self, costs: List[List[int]]) -> int:
        dp = costs
        N = len(dp)

        # go from 1 to N
        for i in range(1, N):
            dp[i][0] += min(dp[i - 1][1], dp[i - 1][2])
            dp[i][2] += min(dp[i - 1][1], dp[i - 1][0])
            dp[i][1] += min(dp[i - 1][2], dp[i - 1][0])

        return min(dp[-1])
