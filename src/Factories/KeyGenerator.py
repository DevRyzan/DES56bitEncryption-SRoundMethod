import random

def generate_key():
    key = random.getrandbits(56)
    
    key_with_parity = 0
    for i in range(7):
        byte = (key >> (i * 8)) & 0xFF  
        parity_bit = bin(byte).count('1') % 2  
        byte_with_parity = (byte << 1) | parity_bit  
        key_with_parity = (key_with_parity << 9) | byte_with_parity  
    
    return key_with_parity

key = generate_key()