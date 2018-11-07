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
    # PUT YOUR CODE HERE
    s=[i for i in plaintext]
    key=[i for i in keyword*(len(plaintext)//len(keyword)+1)]
    ciphertext=''
    for i in range(len(s)):
        simbol=ord(s[i])
        simkey=ord(key[i])
        if 65 <= simkey <= 90:
            simkey-=65
        elif 97 <= simkey <= 122:
            simkey-=97
        if 65 <= simbol <= 90-simkey or 97 <= simbol <= 122-simkey:
            s[i]=chr(simbol+simkey)
        elif 90-simkey < simbol <= 90 or 122-simkey < simbol <= 122:
            s[i]=chr(simbol+simkey-26)
        ciphertext+=s[i]
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
    # PUT YOUR CODE HERE
    s=[i for i in ciphertext]
    key=[i for i in keyword*(len(ciphertext)//len(keyword)+1)]
    ciphertext=''
    for i in range(len(s)):
        simbol=ord(s[i])
        simkey=ord(key[i])
        if 65 <= simkey <= 90:
            simkey-=65
        elif 97 <= simkey <= 122:
            simkey-=97
        if 65+simkey <= simbol <= 90 or 97+simkey <= simbol <= 122:
            s[i]=chr(simbol-simkey)
        elif 65 <= simbol < 65+simkey or 97 <= simbol < 97+simkey:
            s[i]=chr(simbol-simkey+26)
        ciphertext+=s[i]
    return plaintext
