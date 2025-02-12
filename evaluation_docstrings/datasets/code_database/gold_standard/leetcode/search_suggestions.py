import bisect


class Solution(object):
    def suggestedProducts(self, products, searchWord):
        """
        :type products: List[str]
        :type searchWord: str
        :rtype: List[List[str]]
        """

        """
        Approach
        build up a dictionary that contains the three desired words for each letter of searchWord
        """

        # res = []
        # for i in range(1,len(searchWord)+1):
        #     segment = searchWord[:i]
        #     res.append(self.generate_matches(segment,products))

        # return res

        ## search approach that relies on the array being ordered
        products.sort()
        prefix = ""
        res = []
        i = 0
        for c in searchWord:
            prefix += c
            # find the index associated with the first word that contains prefix
            # this is the insertion point of prefic into the products list
            i = bisect.bisect_left(products, prefix, lo=i)

            # for everything up to 3 indices away, add it if it fits
            res.append([w for w in products[i : i + 3] if w[: len(prefix)] == prefix])
        return res
