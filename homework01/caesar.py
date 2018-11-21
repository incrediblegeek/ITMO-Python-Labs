def encrypt_caesar(plaintext: str) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ''
    for ch in plaintext:
        if 87 < ord(ch) < 91 or 119 < ord(ch) < 123:
            ciphertext += chr(ord(ch) - 23)
        elif 64 < ord(ch) < 88 or 96 < ord(ch) < 120:
            ciphertext += chr(ord(ch) + 3)
        else:
            ciphertext += ch
    return ciphertext

def decrypt_caesar(ciphertext: str) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ''
    for ch in ciphertext:
        if 64 < ord(ch) < 68 or 96 < ord(ch) < 100:
            plaintext += chr(ord(ch) + 23)
        elif 67 < ord(ch) < 91 or 99 < ord(ch) < 123:
            plaintext += chr(ord(ch) - 3)
        else: plaintext += ch
    return plaintext