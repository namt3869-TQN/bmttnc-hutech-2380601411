from flask import Flask, request, jsonify
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayfairCipher

app = Flask(__name__)

# CAESAR ROUTE
@app.route("/caesar", methods=["POST"])
def caesar_encrypt():
    data = request.json
    plain_text = data.get("plain_text")
    key = int(data.get("key"))
    cipher = CaesarCipher()
    encrypted_text = cipher.encrypt_text(plain_text, key)
    return jsonify({"encrypted_text": encrypted_text})

@app.route("/caesar/decrypt", methods=["POST"])
def caesar_decrypt():
    data = request.json
    cipher_text = data.get("cipher_text")
    key = int(data.get("key"))
    cipher = CaesarCipher()
    decrypted_text = cipher.decrypt_text(cipher_text, key)
    return jsonify({"decrypted_text": decrypted_text})

# VIGENERE ROUTE
@app.route("/vigenere", methods=["POST"])
def vigenere_encrypt():
    data = request.json
    plain_text = data.get("plain_text")
    key = data.get("key")
    cipher = VigenereCipher()
    encrypted_text = cipher.encrypt(plain_text, key)
    return jsonify({"encrypted_text": encrypted_text})

@app.route("/vigenere/decrypt", methods=["POST"])
def vigenere_decrypt():
    data = request.json
    cipher_text = data.get("cipher_text")
    key = data.get("key")
    cipher = VigenereCipher()
    decrypted_text = cipher.decrypt(cipher_text, key)
    return jsonify({"decrypted_text": decrypted_text})

# RAIL FENCE ROUTE
@app.route("/railfence", methods=["POST"])
def railfence_encrypt():
    data = request.json
    plain_text = data.get("plain_text")
    key = int(data.get("key"))
    cipher = RailFenceCipher()
    encrypted_text = cipher.encrypt_rail_fence(plain_text, key)
    return jsonify({"encrypted_text": encrypted_text})

@app.route("/railfence/decrypt", methods=["POST"])
def railfence_decrypt():
    data = request.json
    cipher_text = data.get("cipher_text")
    key = int(data.get("key"))
    cipher = RailFenceCipher()
    decrypted_text = cipher.decrypt_rail_fence(cipher_text, key)
    return jsonify({"decrypted_text": decrypted_text})

# PLAYFAIR ROUTE
@app.route("/playfair", methods=["POST"])
def playfair_encrypt():
    data = request.json
    plain_text = data.get("plain_text")
    key = data.get("key")
    cipher = PlayfairCipher()
    encrypted_text = cipher.encrypt_playfair(plain_text, key)
    return jsonify({"encrypted_text": encrypted_text})

@app.route("/playfair/decrypt", methods=["POST"])
def playfair_decrypt():
    data = request.json
    cipher_text = data.get("cipher_text")
    key = data.get("key")
    cipher = PlayfairCipher()
    decrypted_text = cipher.decrypt_playfair(cipher_text, key)
    return jsonify({"decrypted_text": decrypted_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)