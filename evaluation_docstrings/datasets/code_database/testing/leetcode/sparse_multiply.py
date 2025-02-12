class Solution:
    def multiply(self, mat1: List[List[int]], mat2: List[List[int]]) -> List[List[int]]:
        """ "
        convert sparse matrices to hash tables
        matrix multiplication: C[i,j] = SUM(A[i,k]*B[k,j])
        """

        def convert_to_lists(mat):
            ln, lm = len(mat), len(mat[0])
            compressed_matrix = [[] for _ in range(ln)]
            for i in range(ln):
                for j in range(lm):
                    if mat[i][j] != 0:
                        # row i, stores matrix at i,j at col j
                        # this will be useful because we will want to index into this array
                        # at col vals
                        compressed_matrix[i].append([mat[i][j], j])

            return compressed_matrix

        m1 = convert_to_lists(mat1)
        m2 = convert_to_lists(mat2)

        m3 = [[0] * len(mat2[0]) for _ in range(len(mat1))]
        ln = len(m3)

        # iterate over all rows
        for m1_row in range(ln):
            # for all non zero elements of the cols of that row
            for element1, m1_col in m1[m1_row]:
                # for all non zero elements of mat2 where row is equal to the col of current element in mat1
                for element2, m2_col in m2[m1_col]:
                    m3[m1_row][m2_col] += element1 * element2

        return m3
