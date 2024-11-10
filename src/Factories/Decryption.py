class Decryptor:
    S_BOX = [
        [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7],
    ]

    PERMUTATION_TABLE = [1, 5, 2, 0, 3, 7, 4, 6]
    EXPANSION_TABLE = [0, 1, 2, 3, 2, 3, 4, 5]

    def __init__(self, key):
        if isinstance(key, int):
            self.key = key
        else:
            raise TypeError("Key should be an integer.")

    def feistel_function(self, right, round_key):
        expanded_right = self.expand(right)
        mixed = expanded_right ^ round_key
        s_box_output = self.apply_s_box(mixed)
        return self.permute(s_box_output)

    def expand(self, half_block):
        expanded = 0
        for i, pos in enumerate(self.EXPANSION_TABLE):
            if half_block & (1 << pos):
                expanded |= (1 << i)
        return expanded

    
    def apply_s_box(self, data):
        column = (data >> 1) & 0xF  # 4-bit column (0-15 arası)
    
        print(f"Debug: column={column}, data={data}")
        if column < 0 or column >= len(self.S_BOX[0]):
            raise IndexError(f"Calculated column {column} out of range for S_BOX entry")

        return self.S_BOX[0][column]
    

    def permute(self, data):
        permuted = 0
        for i, pos in enumerate(self.PERMUTATION_TABLE):
            if data & (1 << pos):
                permuted |= (1 << i)
        return permuted

    def decrypt(self, ciphertext):
        blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
        decrypted_blocks = [self.decrypt_block(block) for block in blocks]
        return ''.join(decrypted_blocks)

    def decrypt_block(self, block):
        left, right = self.split_into_halves_from_hex(block)
        for round in reversed(range(16)):  # Reverse rounds for decryption
            round_key = self.generate_round_key(round)
            left_new = right ^ self.feistel_function(left, round_key)
            right, left = left, left_new
        return self.combine_halves(left, right).decode().rstrip('\x00')

    def split_into_halves_from_hex(self, hex_data):
        data = int(hex_data, 16)  # Convert hex to integer
        left = (data >> 32) & 0xFFFFFFFF
        right = data & 0xFFFFFFFF
        return left, right

    def combine_halves(self, left, right):
        combined = (left << 32) | right
        return combined.to_bytes(8, 'big')

    def generate_round_key(self, round):
        shifted_key = (self.key >> round) & 0xFFFFFFFF
        return shifted_key