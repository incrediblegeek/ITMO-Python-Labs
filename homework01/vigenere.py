def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ''
    alph_low = 'abcdefghijklmnopqrstuvwxyz'
    alph_up = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    key = []
    if len(keyword) < len(plaintext):
        keyword = keyword*int((len(plaintext)/len(keyword))+1)
    for ch in keyword:
        if 96 < ord(ch) < 123:
            key.append(alph_low.index(ch))
        else:
            key.append(alph_up.index(ch))
    for i in range(0, len(plaintext)):
        n = 0
        n = ord(plaintext[i]) + key[i]
        if (64 < ord(plaintext[i]) < 91 and n > 90) or (96 < ord(plaintext[i]) < 123 and n > 122):
            ciphertext += chr(n - 26)
        else:
            ciphertext += chr(n)
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword:str) -> str:
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ''
    alph_low = 'abcdefghijklmnopqrstuvwxyz'
    alph_up = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    key = []
    if len(keyword) < len(ciphertext):
        keyword = keyword*int((len(ciphertext)/len(keyword))+1)
    for ch in keyword:
        if 96 < ord(ch) < 123:
            key.append(alph_low.index(ch))
        else:
            key.append(alph_up.index(ch))
    for i in range(0, len(ciphertext)):
        n = 0
        n = ord(ciphertext[i]) - key[i]
        if (64 < ord(ciphertext[i]) < 91 and n < 65) or (96 < ord(ciphertext[i]) < 123 and n < 97):
            plaintext += chr(n + 26)
        else:
            plaintext += chr(n)
    return plaintext