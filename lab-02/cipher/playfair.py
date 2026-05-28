class PlayfairCipher:
    def __init__(self):
        pass

    def _generate_matrix(self, key):
        key = key.upper().replace('J', 'I')
        matrix = []
        seen = set()
        for char in key:
            if char.isalpha() and char not in seen:
                seen.add(char)
                matrix.append(char)
        for i in range(26):
            char = chr(65 + i)
            if char != 'J' and char not in seen:
                seen.add(char)
                matrix.append(char)
        return [matrix[i:i+5] for i in range(0, 25, 5)]

    def _find_position(self, matrix, char):
        for r in range(5):
            for c in range(5):
                if matrix[r][c] == char:
                    return r, c
        return None

    def encrypt_playfair(self, text, key):
        matrix = self._generate_matrix(key)
        text = text.upper().replace('J', 'I').replace(" ", "")
        prepared_text = ""
        i = 0
        while i < len(text):
            prepared_text += text[i]
            if i + 1 < len(text):
                if text[i] == text[i+1]:
                    prepared_text += 'X'
                    i += 1
                else:
                    prepared_text += text[i+1]
                    i += 2
            else:
                prepared_text += 'X'
                i += 1
        result = ""
        for i in range(0, len(prepared_text), 2):
            r1, c1 = self._find_position(matrix, prepared_text[i])
            r2, c2 = self._find_position(matrix, prepared_text[i+1])
            if r1 == r2:
                result += matrix[r1][(c1 + 1) % 5] + matrix[r2][(c2 + 1) % 5]
            elif c1 == c2:
                result += matrix[(r1 + 1) % 5][c1] + matrix[(r2 + 1) % 5][c2]
            else:
                result += matrix[r1][c2] + matrix[r2][c1]
        return result

    def decrypt_playfair(self, cipher, key):
        matrix = self._generate_matrix(key)
        result = ""
        for i in range(0, len(cipher), 2):
            r1, c1 = self._find_position(matrix, cipher[i])
            r2, c2 = self._find_position(matrix, cipher[i+1])
            if r1 == r2:
                result += matrix[r1][(c1 - 1) % 5] + matrix[r2][(c2 - 1) % 5]
            elif c1 == c2:
                result += matrix[(r1 - 1) % 5][c1] + matrix[(r2 - 1) % 5][c2]
            else:
                result += matrix[r1][c2] + matrix[r2][c1]
        return result