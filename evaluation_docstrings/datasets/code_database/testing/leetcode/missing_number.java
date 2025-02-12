class Solution {
    public int missingNumber(int[] arr) {
        int n = arr.length;

        // Get the difference `difference`.
        int difference = (arr[arr.length - 1] - arr[0]) / n;

        // The expected element equals the starting element.
        int expected = arr[0];

        for (int val : arr) {
            // Return the expected value that doesn't match val.
            if (val != expected) return expected;

            // Next element will be expected element + `difference`.
            expected += difference;
        }
        return expected;
    }
}