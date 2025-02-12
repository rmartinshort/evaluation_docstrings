from collections import deque


class Solution:
    def romanToInt(self, s):
        """
        :type s: str
        :rtype: int
        """

        Q = deque([char for char in s])
        to_sum = []

        lookup = {
            "I": 1,
            "V": 5,
            "IV": 4,
            "X": 10,
            "IX": 9,
            "L": 50,
            "C": 100,
            "XL": 40,
            "XC": 90,
            "D": 500,
            "CD": 400,
            "CM": 900,
            "M": 1000,
        }

        while Q:
            latest = Q.popleft()
            if Q:
                head_of_Q = Q[0]

                if (
                    (latest == "I" and head_of_Q in ["V", "X"])
                    or (latest == "X" and head_of_Q in ["L", "C"])
                    or (latest == "C" and head_of_Q in ["D", "M"])
                ):
                    latest_2 = Q.popleft()
                    latest = latest + latest_2

            to_sum.append(lookup[latest])

        return sum(to_sum)
