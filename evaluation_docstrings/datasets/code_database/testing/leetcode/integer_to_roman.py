class Solution(object):
    def intToRoman(self, num):
        mapping = {
            1000: "M",
            900: "CM",
            500: "D",
            400: "CD",
            100: "C",
            90: "XC",
            50: "L",
            40: "XL",
            10: "X",
            9: "IX",
            5: "V",
            4: "IV",
            1: "I",
        }

        test_order = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]

        output = ""
        for element in test_order:
            # the number of times the element fits into the number
            ntimes = num // element
            # print(num, ntimes, element)
            # the remainder
            # the remainder
            num = num % element
            output += str(ntimes * mapping[element])

        return output
