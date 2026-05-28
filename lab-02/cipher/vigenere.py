class VigenereCipher:
    def __init__(self):
        pass
    
    def encrypt(self, plaintext, key):
        encrypted_text = []
        key = key.upper()
        key_index = 0
        for char in plaintext:
            if char.isalpha():
                shift = ord(key[key_index % len(key)]) - 65
                if char.isupper():
                    encrypted_char = chr((ord(char) - 65 + shift) % 26 + 65)
                else:
                    encrypted_char = chr((ord(char) - 97 + shift) % 26 + 97)
                encrypted_text.append(encrypted_char)
                key_index += 1
            else:
                encrypted_text.append(char)
        return "".join(encrypted_text)

    def decrypt(self, ciphertext, key):
        decrypted_text = []
        key = key.upper()
        key_index = 0
        for char in ciphertext:
            if char.isalpha():
                shift = ord(key[key_index % len(key)]) - 65
                if char.isupper():
                    decrypted_char = chr((ord(char) - 65 - shift) % 26 + 65)
                else:
                    decrypted_char = chr((ord(char) - 97 - shift) % 26 + 97)
                decrypted_text.append(decrypted_char)
                key_index += 1
            else:
                decrypted_text.append(char)
        return "".join(decrypted_text)