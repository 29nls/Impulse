# Import modules
from base64 import b64encode, b64decode


def xor(text: str, key: str) -> str:
    """XOR encrypt/decrypt text with key.
    
    Args:
        text: Text to encrypt/decrypt
        key: Encryption key
        
    Returns:
        XOR result string
    """
    key_len = len(key)
    result = bytearray()
    for i, char in enumerate(text):
        result.append(ord(char) ^ ord(key[i % key_len]))
    return result.decode("latin-1")


def encode(text: str, key: str) -> str:
    """Encode: text => XOR => base64.
    
    Args:
        text: Plain text
        key: Encryption key
        
    Returns:
        Base64 encoded XOR encrypted string
    """
    return b64encode(xor(text, key).encode("latin-1")).decode("utf-8")


def decode(text: str, key: str) -> str:
    """Decode: base64 => XOR => text.
    
    Args:
        text: Base64 encoded XOR encrypted string
        key: Encryption key
        
    Returns:
        Decrypted plain text
        
    Raises:
        ValueError: If input is not valid base64
    """
    try:
        decoded = b64decode(text).decode("latin-1")
    except Exception as e:
        raise ValueError(f"Invalid base64 input: {e}")
    return xor(decoded, key)
