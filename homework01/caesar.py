def encrypt_caesar(plaintext):
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

    ciphertext=''
    for i in range(len(plaintext)):
        simbol=ord(plaintext[i])
        if ord('A') <= simbol <= ord('Z')-3 or ord('a') <= simbol <= ord('z')-3:
            ciphertext+=chr(simbol+3)
        elif ord('Z')-2 <= simbol <= ord('Z') or ord('z')-2 <= simbol <= ord('z'):
            ciphertext+=chr(simbol-23)
        else:
            ciphertext+=plaintext[i]
    return ciphertext


def decrypt_caesar(ciphertext):
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

    plaintext=''
    for i in range(len(ciphertext)):
        simbol=ord(ciphertext[i])
        if ord('A')+3 <= simbol <= ord('Z') or ord('a')+3 <= simbol <= ord('z'):
            plaintext+=chr(simbol-3)
        elif ord('A') <= simbol <= ord('A')+2 or ord('a') <= simbol <= ord('a')+2:
            plaintext+=chr(simbol+23)
        else:
            plaintext+=ciphertext[i]
    return plaintext
