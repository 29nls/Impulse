# Import modules
from random import choice


def protect(message: str, salt: str) -> str:
    """Add salt to message.
    
    Args:
        message: Original message
        salt: Salt string
        
    Returns:
        Salted message
    """
    salt_list = list(salt)
    salt_chars = []
    
    # Collect unique characters from message
    for char in message:
        if char not in salt_chars:
            salt_chars.append(char)
    
    # Add salt to message
    result = []
    for index, secret_char in enumerate(message):
        for _ in range(int(salt_list[index])):
            result.append(choice(salt_chars))
        result.append(secret_char)
    
    return "".join(result)


def unprotect(message: str, salt: str) -> str:
    """Remove salt from message.
    
    Args:
        message: Salted message
        salt: Salt string
        
    Returns:
        Original message without salt
    """
    pos = 0
    result = []
    
    for secret_salt in salt:
        message = message[int(secret_salt) + pos:]
        if not message:
            break
        
        result.append(message[0])
        pos = 1
    
    return "".join(result)
