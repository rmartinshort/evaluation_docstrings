class Solution(object):
    def missingNumber(self, arr):
        expected_difference = (arr[-1] - arr[0]) // len(arr)

        left = 0
        right = len(arr) - 2

        while left <= right:
            mid = (left + right) // 2

            # if we have reached the solution
            if (arr[mid] + expected_difference) != arr[mid + 1]:
                return arr[mid] + expected_difference

            # if everything is good to the left, move right
            if arr[mid] == arr[0] + mid * expected_difference:
                left = mid + 1
            # if everything is good to the right, move left
            else:
                right = mid - 1

        return arr[mid] + expected_difference
