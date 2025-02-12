def ngrams_chars(string, n=3):
    """Takes an input string, cleans it and converts to ngrams"""

    string = string.lower()  # lower case
    string = string.encode("ascii", errors="ignore").decode()
    chars_to_remove = [")", "(", ".", "|", "[", "]", "{", "}", "'", "-"]
    rx = "[" + re.escape("".join(chars_to_remove)) + "]"
    string = re.sub(rx, "", string)
    string = string.replace("&", "and")
    string = re.sub(" +", " ", string).strip()
    string = " " + string + " "

    ngrams = zip(*[string[i:] for i in range(n)])
    return ["".join(ngram) for ngram in ngrams]
