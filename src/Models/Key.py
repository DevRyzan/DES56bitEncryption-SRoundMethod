import random

class KeyProp:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(KeyProp, cls).__new__(cls)
            cls._instance.key = cls._instance._generate_key_with_parity()
        return cls._instance

    @staticmethod
    def _generate_key():
        
        return random.getrandbits(56)

    def _generate_key_with_parity(self):
        key = self._generate_key()
        
        key_with_parity = 0
        
        for i in range(7):
            byte = (key >> (i * 8)) & 0xFF  # 8-bit bayt
            parity_bit = bin(byte).count('1') % 2  
            byte_with_parity = (byte << 1) | parity_bit  
            key_with_parity = (key_with_parity << 9) | byte_with_parity  
            
        return key_with_parity

    def get_key(self):
        return self.key

    def __str__(self):
        return f"{self.key:016X}"


#Sİngelton
key_generator = KeyProp()
key1 = key_generator.get_key()
print(f"Key 1: {key1:016X}")

key2 = key_generator.get_key()
print(f"Key 2: {key2:016X}")

print("Equal? :", key1 == key2)  