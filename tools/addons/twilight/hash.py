# Import modules
from hashlib import md5
from string import ascii_letters


def getSaltByKey(key: str, message: str) -> str:
    """Generate salt from key hash matching message length.
    
    Args:
        key: Encryption key
        message: Message to match length
        
    Returns:
        Salt string with same length as message
    """
    salt = []
    kHash = md5(key.encode()).hexdigest()
    target_len = len(message)

    while len(salt) < target_len:
        for char in kHash:
            if len(salt) >= target_len:
                break
            if char not in ascii_letters:
                salt.append(char)

    return "".join(salt)
