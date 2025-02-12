class Solution:
    def myPow(self, x: float, n: int) -> float:
        """
        binary exponentiation

        x^n = (x^2)^(n//2)
        so we can take advantage of this to make it faster than just keep multiplying by x

        while n != 0
            if n is odd, multiply result by x and reduce n by 1
            if n is even, square x and reduce n by a factor of 2

        why do we square x, because x^n = (x^2)^(n//2)
        and we will eventually get to a situation where n == 1 so we will multiply the
        res by the value of x

        if n < 0
            set n = -1*n
            x = 1/
        Can do iteratively or recusively. Will probably do it iteratively
        """

        res = 1
        while n != 0:
            if n < 0:
                n = -1 * n
                x = 1 / x

            if n % 2 == 1:
                res *= x
                n -= 1
            else:
                # binary exponentiation
                x = x**2
                # divide n by 2 since we are using x^n = (x^2)^(n//2)
                n = n // 2

        return res
