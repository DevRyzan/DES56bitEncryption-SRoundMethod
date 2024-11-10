import random
from Factories.KeyGenerator import generate_key

import random

class KeyProp:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(KeyProp, cls).__new__(cls)
            cls._instance.key = cls._generate_key()
        return cls._instance

    @staticmethod
    def _generate_key():
        return random.getrandbits(56)

    def get_key(self):
        return self.key

    def __str__(self):
        return str(self.key)



key_generator = KeyProp()
key1 = key_generator.key   
print("Key 1:", key1)

key2 = key_generator.key
print("Key 2:", key2)
 
print("Equal? :", key1 == key2)  