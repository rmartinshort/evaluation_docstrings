# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution(object):
    def maximumAverageSubtree(self, root):
        def traverse(node):
            if not node:
                return (0, 0, 0)

            left_count, left_sum, left_avg = traverse(node.left)
            right_count, right_sum, right_avg = traverse(node.right)

            total_count = float(left_count + right_count + 1)
            total_sum = float(left_sum + right_sum + node.val)
            max_avg = max(total_sum / total_count, max(left_avg, right_avg))

            return (total_count, total_sum, max_avg)

        res = traverse(root)
        return res[-1]
