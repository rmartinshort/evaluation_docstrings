class Solution:
    def numWays(self, n: int, k: int) -> int:
        if n == 0:
            return 0

        dp = [0] * (n + 1)

        if len(dp) > 1:
            dp[1] = k
        if len(dp) > 2:
            dp[2] = k**2

        if len(dp) <= 3:
            return dp[-1]

        for i in range(3, len(dp)):
            # value at i = sum of possibilies leading up to i
            dp[i] = (k - 1) * dp[i - 1] + (k - 1) * dp[i - 2]

        return dp[-1]
