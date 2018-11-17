def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """

    key=keyword*(len(plaintext)//len(keyword)+1)
    ciphertext=''
    for i in range(len(plaintext)):
        simbol=ord(plaintext[i])
        simkey=ord(key[i])
        if ord('A') <= simkey <= ord('Z'):
            simkey-=ord('A')
        elif ord('a') <= simkey <= ord('z'):
            simkey-=ord('a')
        if ord('A') <= simbol <= ord('Z')-simkey or ord('a') <= simbol <= ord('z')-simkey:
            ciphertext+=chr(simbol+simkey)
        elif ord('Z')-simkey < simbol <= ord('Z') or ord('z')-simkey < simbol <= ord('z'):
            ciphertext+=chr(simbol+simkey-26)
        else:
            ciphertext+=plaintext[i]
    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """

    key=keyword*(len(ciphertext)//len(keyword)+1)
    plaintext=''
    for i in range(len(ciphertext)):
        simbol=ord(ciphertext[i])
        simkey=ord(key[i])
        if ord('A') <= simkey <= ord('Z'):
            simkey-=ord('A')
        elif ord('a') <= simkey <= ord('z'):
            simkey-=ord('a')
        if ord('A')+simkey <= simbol <= ord('Z') or ord('a')+simkey <= simbol <= ord('z'):
            plaintext+=chr(simbol-simkey)
        elif ord('A') <= simbol < ord('A')+simkey or ord('a') <= simbol < ord('a')+simkey:
            plaintext+=chr(simbol-simkey+26)
        else:
            plaintext+=ciphertext[i]
    return plaintext
