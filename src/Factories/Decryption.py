class Decryptor:
    def __init__(self, key):
        if isinstance(key, int):
            self.key = key
        else:
            raise TypeError("Key should be an integer.")

    def feistel_function(self, right, key):
        return right ^ key

    def decrypt(self, ciphertext):
        blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
        decrypted_blocks = [self.decrypt_block(block) for block in blocks]
        return ''.join(decrypted_blocks).rstrip('\x00')  

    def decrypt_block(self, hex_block):
        left, right = self.split_into_halves_from_hex(hex_block)
        for round in reversed(range(16)):
            round_key = self.generate_round_key(round)
            left_new = right ^ self.feistel_function(left, round_key)
            right = left
            left = left_new
        return self.combine_halves(left, right).decode()

    def split_into_halves_from_hex(self, hex_data):
        data = int(hex_data, 16)
        left = (data >> 32) & 0xFFFFFFFF
        right = data & 0xFFFFFFFF
        return left, right

    def combine_halves(self, left, right):
        combined = (left << 32) | right
        return combined.to_bytes(8, 'big')

    def generate_round_key(self, round):
        shifted_key = (self.key >> round) & 0xFFFFFFFF
        return shifted_key
