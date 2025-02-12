# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def lowestCommonAncestor(
        self, root: "TreeNode", p: "TreeNode", q: "TreeNode"
    ) -> "TreeNode":
        """
        DFS: Build paths from p and q back the root
        the first place these paths cross will be the LCA

        in the DFS, we return None if we reached the end or node if we got p or q
        then we look left and right. If we found a node that gives us p and q, that means
        we have the LCA
        """

        def LCA(node):
            if not node:
                return None
            elif node == p or node == q:
                return node

            left = LCA(node.left)
            right = LCA(node.right)

            if left and right:
                return node
            elif left:
                return left
            else:
                return right

        lca_node = LCA(root)

        return lca_node
