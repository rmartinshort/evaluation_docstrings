from collections import deque


class Solution(object):
    def nearestExit(self, maze, entrance):
        """
        :type maze: List[List[str]]
        :type entrance: List[int]
        :rtype: int
        """

        ## Approach
        # BFS: define a set seen() and an is_valid() function
        # do the BFS and stop whenever an edge cell is found,
        # store the number of steps in the BFD queue

        seen = set()
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        # starts with 0 steps
        Q = deque([(entrance[0], entrance[1], 0)])

        ln = len(maze)
        lm = len(maze[0])

        def is_valid(i, j):
            # gone outside the maze
            if (i < 0) or (i >= ln) or (j < 0) or (j >= lm):
                return False

            # wall
            elif maze[i][j] == "+":
                return False

            else:
                return True

        def is_exit(i, j):
            if (i == entrance[0]) and (j == entrance[1]):
                return False

            elif i == 0:
                return True

            elif i == ln - 1:
                return True

            elif j == 0:
                return True

            elif j == lm - 1:
                return True

            else:
                return False

        while Q:
            this_i, this_j, steps = Q.popleft()

            if is_exit(this_i, this_j):
                return steps

            for d in directions:
                candidate_i = this_i + d[0]
                candidate_j = this_j + d[1]
                if (candidate_i, candidate_j) not in seen:
                    seen.add((candidate_i, candidate_j))
                    if is_valid(candidate_i, candidate_j):
                        Q.append((candidate_i, candidate_j, steps + 1))

        return -1
