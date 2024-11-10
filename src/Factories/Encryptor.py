class Encryptor:
    S_BOX = [
        [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7],
        [0xA, 0xC, 0x3, 0xF, 0x5, 0x1, 0xB, 0x0, 0x6, 0x7, 0x9, 0xD, 0x8, 0x4, 0x2, 0xE],
        [0x4, 0x9, 0xA, 0x6, 0x7, 0x1, 0x0, 0xD, 0xF, 0x8, 0xB, 0x3, 0xE, 0x2, 0xC, 0x5],
        [0xF, 0x7, 0xB, 0xD, 0x6, 0x4, 0xA, 0x9, 0x0, 0x3, 0xC, 0x2, 0x8, 0x1, 0x5, 0xE]
    ]
    
    EXPANSION_TABLE = [0, 1, 2, 3, 2, 3, 4, 5]
    PERMUTATION_TABLE = [7, 0, 3, 1, 6, 4, 2, 5]

    def __init__(self, key):
        self.key = key
    
    def feistel_function(self, right, round_key, sbox_index):
        expanded_right = self.expand(right)
        mixed = expanded_right ^ round_key
        s_box_output = self.apply_s_box(mixed, sbox_index)
        return self.permute(s_box_output)

    def expand(self, half_block):
        expanded = 0
        for i, pos in enumerate(self.EXPANSION_TABLE):
            if half_block & (1 << pos):
                expanded |= (1 << i)
        return expanded
    


    def apply_s_box(self, data, sbox_index):
        if sbox_index >= len(self.S_BOX):
            raise IndexError(f"S-Box index {sbox_index} is out of range.")
    
        row = ((data & 0x20) >> 4) | (data & 0x1)  # 2-bit row
        column = (data >> 1) & 0xF  # 4-bit column

        print(f"Debug: sbox_index={sbox_index}, row={row}, column={column}, data={data}")

        if row < 0 or row >= len(self.S_BOX) or column < 0 or column >= len(self.S_BOX[0]):
            raise IndexError(f"Calculated row {row} or column {column} out of range for S_BOX entry")

        return self.S_BOX[sbox_index][column]


    def permute(self, data):
        permuted = 0
        for i, pos in enumerate(self.PERMUTATION_TABLE):
            if data & (1 << pos):
                permuted |= (1 << i)
        return permuted
    
    def encrypt(self, plaintext):
        blocks = [plaintext[i:i+8].ljust(8, '\x00') for i in range(0, len(plaintext), 8)]
        print(f"Blocks to be encrypted: {blocks}")  
        encrypted_blocks = [self.encrypt_block(block) for block in blocks]
        return ''.join(encrypted_blocks)

    def encrypt_block(self, block):
        left, right = self.split_into_halves(block)
        for round in range(16):
            round_key = self.generate_round_key(round)
            sbox_index = round % len(self.S_BOX)  # Select S-Box based on round
            right_new = self.feistel_function(right, round_key, sbox_index)
            new_left = left ^ right_new
            left, right = right, new_left
        return self.combine_halves(left, right).hex()

    def split_into_halves(self, data):
        data = int.from_bytes(data.encode(), 'big')
        left = (data >> 32) & 0xFFFFFFFF
        right = data & 0xFFFFFFFF
        return left, right

    def combine_halves(self, left, right):
        combined = (left << 32) | right
        return combined.to_bytes(8, 'big')

    def generate_round_key(self, round):
        shifted_key = (self.key >> round) & 0xFFFFFFFF
        return shifted_key