class Solution:
    def trap(self, height: List[int]) -> int:
        max_left_arr = [0] * len(height)
        max_right_arr = [0] * len(height)

        max_left = 0
        for i in range(len(height)):
            max_left = max(height[i], max_left)
            max_left_arr[i] = max_left

        max_right = 0
        for i in range(len(height) - 1, -1, -1):
            max_right = max(height[i], max_right)
            max_right_arr[i] = max_right

        # now we have to find the min from both sides
        sum_water = 0
        for i in range(len(height)):
            sum_water += max(min(max_left_arr[i], max_right_arr[i]) - height[i], 0)

        return sum_water
