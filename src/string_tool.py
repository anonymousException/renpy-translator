def remove_upprintable_chars(s):
    return ''.join(x for x in s if x.isprintable())

def split_strings(strings, max_length=5000):
    result = []
    current_string = []

    for string in strings:
        _len = 0
        for i in current_string:
            _len += len(i)
        if _len + len(string) <= max_length:
            current_string.append(string)
        else:
            result.append(current_string)
            current_string = [string]

    if current_string:
        result.append(current_string)
    return result
