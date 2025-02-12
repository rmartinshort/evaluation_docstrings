int romanToInt(char *s) {
    int values[256];
    values['I'] = 1;
    values['V'] = 5;
    values['X'] = 10;
    values['L'] = 50;
    values['C'] = 100;
    values['D'] = 500;
    values['M'] = 1000;

    int sum = 0;
    int i = 0;
    while (i < strlen(s)) {
        char currentSymbol = s[i];
        int currentValue = values[currentSymbol];
        int nextValue = 0;
        if (i + 1 < strlen(s)) {
            char nextSymbol = s[i + 1];
            nextValue = values[nextSymbol];
        }
        if (currentValue < nextValue) {
            sum += (nextValue - currentValue);
            i += 2;
        } else {
            sum += currentValue;
            i += 1;
        }
    }
    return sum;
}