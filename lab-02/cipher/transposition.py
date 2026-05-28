import math

class TranspositionCipher:
    def __init__(self):
        pass

    def encrypt_transposition(self, text, key):
        cipher = [''] * key
        for col in range(key):
            pointer = col
            while pointer < len(text):
                cipher[col] += text[pointer]
                pointer += key
        return "".join(cipher)

    def decrypt_transposition(self, cipher, key):
        num_cols = int(math.ceil(len(cipher) / float(key)))
        num_rows = key
        num_shaded_boxes = (num_cols * num_rows) - len(cipher)
        plaintext = [''] * num_cols
        row = 0
        col = 0
        for char in cipher:
            plaintext[col] += char
            col += 1
            if (col == num_cols) or (col == num_cols - 1 and row >= num_rows - num_shaded_boxes):
                col = 0
                row += 1
        return "".join(plaintext)