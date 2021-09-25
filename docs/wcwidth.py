def wcswidth(s):
    return sum((1 if 0 <= ord(c) < 256 else 2) for c in s)
