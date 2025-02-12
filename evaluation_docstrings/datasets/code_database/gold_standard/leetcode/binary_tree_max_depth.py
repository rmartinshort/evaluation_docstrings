class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        self.maxdepth = 0

        def recurse(root, current_depth):
            if not root:
                self.maxdepth = max(self.maxdepth, current_depth)
                return

            recurse(root.left, current_depth + 1)
            recurse(root.right, current_depth + 1)

        recurse(root, 0)
        return self.maxdepth
