class RailFenceCipher:

    def encrypt_rail_fence(self, text, key):
        if key <= 1 or key >= len(text):
            return text

        rail = [['' for _ in range(len(text))] for _ in range(key)]

        row = 0
        direction = 1  # xuống

        for col in range(len(text)):
            rail[row][col] = text[col]

            if row == 0:
                direction = 1
            elif row == key - 1:
                direction = -1

            row += direction

        result = []

        for r in range(key):
            for c in range(len(text)):
                if rail[r][c]:
                    result.append(rail[r][c])

        return ''.join(result)

    def decrypt_rail_fence(self, cipher, key):
        if key <= 1 or key >= len(cipher):
            return cipher

        n = len(cipher)

        rail = [['' for _ in range(n)] for _ in range(key)]

        # Bước 1: đánh dấu đường zig-zag
        row = 0
        direction = 1

        for col in range(n):
            rail[row][col] = '*'

            if row == 0:
                direction = 1
            elif row == key - 1:
                direction = -1

            row += direction

        # Bước 2: điền ciphertext theo từng hàng
        idx = 0

        for r in range(key):
            for c in range(n):
                if rail[r][c] == '*':
                    rail[r][c] = cipher[idx]
                    idx += 1

        # Bước 3: đọc lại theo đường zig-zag
        result = []

        row = 0
        direction = 1

        for col in range(n):
            result.append(rail[row][col])

            if row == 0:
                direction = 1
            elif row == key - 1:
                direction = -1

            row += direction

        return ''.join(result)