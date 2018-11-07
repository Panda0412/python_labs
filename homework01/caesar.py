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
    # PUT YOUR CODE HERE
    slovo=[i for i in plaintext]
    ciphertext=''
    for i in range(len(slovo)):
        simbol=ord(slovo[i])
        if 65 <= simbol <= 87 or 97 <= simbol <= 119:
            slovo[i]=chr(simbol+3)
        elif 88 <= simbol <= 90 or 120 <= simbol <= 122:
            slovo[i]=chr(simbol-23)
        ciphertext+=slovo[i]
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
    # PUT YOUR CODE HERE
    slovo=[i for i in ciphertext]
    plaintext=''
    for i in range(len(slovo)):
        simbol=ord(slovo[i])
        if 68 <= simbol <= 90 or 100 <= simbol <= 122:
            slovo[i]=chr(simbol-3)
        elif 65 <= simbol <= 67 or 97 <= simbol <= 99:
            slovo[i]=chr(simbol+23)
        plaintext+=slovo[i]
    return plaintext
