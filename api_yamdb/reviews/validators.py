def is_palindrome(line: str) -> bool:
    replacements = [(':', ''), (',', ''), (' ', ''), ('.', '')]
    for char, replacement in replacements:
        line = line.replace(char, replacement)
    return line == line[::-1]

print(is_palindrome('A man, a plan, a canal: Panama'))