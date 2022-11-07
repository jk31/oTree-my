import re


# Splits a string on instances of a delimiter character. Ignores quoted delimiters.
def splitc(s, delimiter, strip=False, discard_empty=False, maxsplit=-1):

    tokens, buf, expecting, escaped = [], [], None, False

    for index, char in enumerate(s):
        if expecting:
            buf.append(char)
            if char == expecting and not escaped:
                expecting = None
        else:
            if char == delimiter:
                tokens.append(''.join(buf))
                buf = []
                if len(tokens) == maxsplit:
                    buf.append(s[index+1:])
                    break
            else:
                buf.append(char)
                if char in ('"', "'"):
                    expecting = char
        escaped = not escaped if char == '\\' else False

    tokens.append(''.join(buf))

    if strip:
        tokens = [t.strip() for t in tokens]

    if discard_empty:
        tokens = [t for t in tokens if t]

    return tokens


# Splits a string using a list of regular expression patterns. Ignores quoted delimiter matches.
def splitre(s, delimiters, keepdels=False):

    tokens, buf = [], []
    end_last_match = 0

    pattern = r'''"(?:[^\\"]|\\.)*"|'(?:[^\\']|\\.)*'|%s'''
    pattern %= '|'.join(delimiters)

    for match in re.finditer(pattern, s):
        if match.group()[0] in ["'", '"']:
            buf.append(s[end_last_match:match.end()])
            end_last_match = match.end()
            continue
        buf.append(s[end_last_match:match.start()])
        tokens.append(''.join(buf))
        buf = []
        end_last_match = match.end()
        if keepdels:
            tokens.append(match.group())

    buf.append(s[end_last_match:])
    tokens.append(''.join(buf))

    return tokens
