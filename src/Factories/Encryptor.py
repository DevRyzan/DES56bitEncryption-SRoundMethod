


class Encryptor:
    def __init__(self, key):
        if isinstance(key, int):
            self.key = key
        else:
            raise TypeError("Key should be an integer.")

    def feistel_function(self, right, key):
        return right ^ key  

    def encrypt(self, plaintext):
        left, right = self.split_into_halves(plaintext)

        for round in range(16):  
            round_key = self.generate_round_key(round)
            right_new = self.feistel_function(right, round_key)
            
            new_left = left ^ right_new
            
            left = right
            right = new_left

        return self.combine_halves(left, right)

    def split_into_halves(self, data):
        data = int.from_bytes(data.encode(), 'big')
        left = (data >> 32) & 0xFFFFFFFF
        right = data & 0xFFFFFFFF
        return left, right

    def combine_halves(self, left, right):
        combined = (left << 32) | right
        return combined.to_bytes(8, 'big').hex()

    def generate_round_key(self, round):
        
        shifted_key = (self.key >> round) & 0xFFFFFFFF
        return shifted_key
    