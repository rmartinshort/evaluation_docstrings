class Solution:
    def jump(self, nums: List[int]) -> int:
        total_jumps = 0
        current_far, current_end = 0, 0

        for i in range(len(nums) - 1):
            # the farthest we can jump from the current spot
            # or the ith spot
            current_far = max(current_far, i + nums[i])

            # if we reached the limit of where we can jump from the
            # current spot, then we make another jump and update
            # current end to the current far (i.e. jump as far as possible)
            if i == current_end:
                # add another jump
                total_jumps += 1
                # extend the limit
                current_end = current_far

            # print(current_end, current_far, total_jumps)

        return total_jumps
