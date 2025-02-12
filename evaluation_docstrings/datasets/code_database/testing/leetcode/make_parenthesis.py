class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        stack = []
        res = []

        def backtrack(openN, closeN):
            if openN == closeN == n:
                res.append("".join(stack))
                return

            if openN < n:
                stack.append("(")
                # continue
                backtrack(openN + 1, closeN)
                stack.pop()

            # if we have more open than close, we can add a new close
            if closeN < openN:
                stack.append(")")
                backtrack(openN, closeN + 1)
                stack.pop()

        backtrack(0, 0)
        return res
