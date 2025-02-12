class Solution:
    def reverseVowels(self, s: str) -> str:
        vowels = set(["a", "e", "i", "o", "u"])
        start = 0
        end = len(s) - 1
        size = len(s)
        slist = [c for c in s]

        while start < end:
            while start < len(s) and s[start].lower() not in vowels:
                start += 1
            while end >= 0 and s[end].lower() not in vowels:
                end -= 1
            if start < end:
                slist[end], slist[start] = slist[start], slist[end]
                start += 1
                end -= 1

        return "".join(slist)
