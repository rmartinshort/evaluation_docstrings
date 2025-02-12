class Solution:
    def maxArea(self, height: List[int]) -> int:
        """
        This is a two pointers problem
        Note that the area of the container will be min(A,B)*distance between them
        Bute force would be every combination of left and right, advancing from the
        left and going right
        """

        # brute force

        # res = 0
        # for i in range(len(height)):
        #     for j in range(i+1,len(height)):
        #         area = min(height[i],height[j])*(j-i)
        #         res = max(res,area)

        # return res

        # optimized
        # this will be a two pointers solution
        # lets start with the max width
        # we can shift pointers in a smart way so that we only shift the pointer to
        # the height that is smaller

        left = 0
        right = len(height) - 1
        area = min(height[left], height[right]) * (right - left)

        while right > left:
            if height[left] > height[right]:
                right -= 1
            else:
                left += 1

            area = max(area, min(height[left], height[right]) * (right - left))

        return area
