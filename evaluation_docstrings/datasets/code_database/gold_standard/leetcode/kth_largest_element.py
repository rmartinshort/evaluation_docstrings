import heapq


class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        """
        Approach

        This can be done with sorting and it would be easy
        we can also use heap. If we make use of a max heap we can just
        pop off the top k
        """

        # this is one way
        # use min heap and push each element
        # if the length becomes too long, then we pop the smallest element
        # so the first element if the heap will be the kth element
        heap = []
        heapq.heapify(heap)
        for element in nums:
            heapq.heappush(heap, element)
            if len(heap) > k:
                heapq.heappop(heap)

        return heap[0]
