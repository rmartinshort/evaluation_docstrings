class Solution:
    def asteroidCollision(self, asteroids: List[int]) -> List[int]:
        ans = []
        for new in asteroids:
            while ans and (new < 0) and (new < ans[-1]) and (0 < ans[-1]):
                if ans[-1] <= -new:
                    ans.pop()
                    # keep going
                    continue
                elif ans[-1] == -new:
                    ans.pop()
                break
            # else can be used with while! This is not very common
            else:
                ans.append(new)
        return ans
