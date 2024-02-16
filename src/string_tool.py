def remove_upprintable_chars(s):
    return ''.join(x for x in s if x.isprintable())