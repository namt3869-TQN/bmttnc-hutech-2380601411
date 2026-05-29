import os
import sys
import unicodedata
from flask import Flask, render_template, request

# Thêm thư mục ex01 vào hệ thống để nhận thư mục cipher
current_dir = os.path.dirname(os.path.abspath(__file__))
ex01_path = os.path.join(current_dir, 'ex01')
if ex01_path not in sys.path:
    sys.path.append(ex01_path)

from cipher.caesar.caesar_cipher import CaesarCipher
from cipher.vigenere.vigenere_cipher import VigenereCipher
from cipher.railfence.railfence_cipher import RailFenceCipher
from cipher.playfair.playfair_cipher import PlayfairCipher

app = Flask(__name__, template_folder=os.path.join(current_dir, 'ex01', 'templates'))

def clean_text(text):
    if not text:
        return ""
    text = text.strip().upper()
    text = "".join(c for c in unicodedata.normalize('NFD', text)
                    if unicodedata.category(c) != 'Mn')
    return text.replace('Đ', 'D')

# HÀM QUÉT ĐỘNG VẠN NĂNG
def call_crypto_func(obj, action_type, text, key):
    methods = [
        method_name for method_name in dir(obj)
        if callable(getattr(obj, method_name))
        and not method_name.startswith("__")
    ]

    keywords = ["enc", "ma", "hoa"] if action_type == "encrypt" else ["dec", "giai", "gia"]

    # Ưu tiên tìm đúng hàm theo keyword
    for method_name in methods:
        name_lower = method_name.lower()
        if any(kw in name_lower for kw in keywords):
            func = getattr(obj, method_name)
            try:
                return func(text, key)
            except TypeError:
                try:
                    return func(text)
                except:
                    continue

    # fallback
    for method_name in methods:
        if "alpha" not in method_name.lower():
            func = getattr(obj, method_name)
            try:
                return func(text, key)
            except TypeError:
                try:
                    return func(text)
                except:
                    continue

    raise AttributeError(f"Không tìm thấy hàm phù hợp trong {obj.__class__.__name__}")


@app.route("/")
def home():
    return render_template("index.html")

# --- ROUTE CHUYỂN TRANG ---
@app.route("/caesar")
def caesar_page(): return render_template("caesar.html")

@app.route("/vigenere")
def vigenere_page(): return render_template("vigenere.html")

@app.route("/railfence")
def railfence_page(): return render_template("railfence.html")

@app.route("/playfair")
def playfair_page(): return render_template("playfair.html")

# --- CAESAR ---
@app.route("/encrypt", methods=["POST"])
def encrypt_route():
    plain_text = clean_text(request.form.get("inputPlainText", ""))

    key = request.form.get("inputKeyPlain", "0")
    key = int(key) if key.isdigit() else 0

    res = call_crypto_func(CaesarCipher(), "encrypt", plain_text, key)
    return render_template("caesar.html", encrypted_text=res, original_text=plain_text, key=key)


@app.route("/decrypt", methods=["POST"])
def decrypt_route():
    cipher_text = clean_text(request.form.get("inputCipherText", ""))

    key = request.form.get("inputKeyCipher", "0")
    key = int(key) if key.isdigit() else 0

    res = call_crypto_func(CaesarCipher(), "decrypt", cipher_text, key)
    return render_template("caesar.html", decrypted_text=res, original_text=cipher_text, key=key)

# --- VIGENERE ---
@app.route("/vigenere/encrypt", methods=["POST"])
def vigenere_enc():
    plain_text = clean_text(request.form.get("inputPlainText", ""))
    key = clean_text(request.form.get("inputKeyPlain", ""))

    res = call_crypto_func(VigenereCipher(), "encrypt", plain_text, key)
    return render_template("vigenere.html", encrypted_text=res, original_text=plain_text, key=key)


@app.route("/vigenere/decrypt", methods=["POST"])
def vigenere_dec():
    cipher_text = clean_text(request.form.get("inputCipherText", ""))
    key = clean_text(request.form.get("inputKeyCipher", ""))

    res = call_crypto_func(VigenereCipher(), "decrypt", cipher_text, key)
    return render_template("vigenere.html", decrypted_text=res, original_text=cipher_text, key=key)

# --- RAIL FENCE (FIX QUAN TRỌNG) ---
@app.route("/railfence/encrypt", methods=["POST"])
def railfence_enc():
    plain_text = clean_text(request.form.get("inputPlainText", ""))

    key = request.form.get("inputKeyPlain", "0")
    key = int(key) if key.isdigit() else 0

    cipher = RailFenceCipher()
    res = cipher.encrypt_rail_fence(plain_text, key)

    return render_template("railfence.html",
                           encrypted_text=res,
                           original_text=plain_text,
                           key=key)


@app.route("/railfence/decrypt", methods=["POST"])
def railfence_dec():
    cipher_text = clean_text(request.form.get("inputCipherText", ""))

    key = request.form.get("inputKeyCipher", "0")
    key = int(key) if key.isdigit() else 0

    cipher = RailFenceCipher()
    res = cipher.decrypt_rail_fence(cipher_text, key)

    return render_template("railfence.html",
                           decrypted_text=res,
                           original_text=cipher_text,
                           key=key)

# --- PLAYFAIR ---
@app.route("/playfair/encrypt", methods=["POST"])
def playfair_enc():
    plain_text = clean_text(request.form.get("inputPlainText", ""))
    key = clean_text(request.form.get("inputKeyPlain", ""))

    cipher = PlayfairCipher()
    res = cipher.encrypt_playfair(plain_text, key)

    return render_template("playfair.html",
                           encrypted_text=res,
                           original_text=plain_text,
                           key=key)


@app.route("/playfair/decrypt", methods=["POST"])
def playfair_dec():
    cipher_text = clean_text(request.form.get("inputCipherText", ""))
    key = clean_text(request.form.get("inputKeyCipher", ""))

    cipher = PlayfairCipher()
    res = cipher.decrypt_playfair(cipher_text, key)

    return render_template("playfair.html",
                           decrypted_text=res,
                           original_text=cipher_text,
                           key=key)


if __name__ == "__main__":
    app.run(debug=True, port=5000)