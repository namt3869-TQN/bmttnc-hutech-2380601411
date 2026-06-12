import os
import sys
import unicodedata
import rsa  # Thêm thư viện rsa phục vụ Lab 03
from flask import Flask, render_template, request, jsonify

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

# Định nghĩa thư mục lưu file khóa keys của hệ thống Server RSA (Lab 03)
KEYS_DIR = os.path.join(current_dir, "..", "lab-03", "cipher", "rsa", "keys")
if not os.path.exists(KEYS_DIR):
    os.makedirs(KEYS_DIR)

def clean_text(text):
    if not text:
        return ""
    text = text.strip().upper()
    text = "".join(c for c in unicodedata.normalize('NFD', text)
                    if unicodedata.category(c) != 'Mn')
    return text.replace('Đ', 'D')

# HÀM QUÉT ĐỘNG VẠN NĂNG (Dành cho Lab 02)
def call_crypto_func(obj, action_type, text, key):
    methods = [
        method_name for method_name in dir(obj)
        if callable(getattr(obj, method_name))
        and not method_name.startswith("__")
    ]

    keywords = ["enc", "ma", "hoa"] if action_type == "encrypt" else ["dec", "giai", "gia"]

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

# --- ROUTE CHUYỂN TRANG (Lab 02) ---
@app.route("/caesar")
def caesar_page(): return render_template("caesar.html")

@app.route("/vigenere")
def vigenere_page(): return render_template("vigenere.html")

@app.route("/railfence")
def railfence_page(): return render_template("railfence.html")

@app.route("/playfair")
def playfair_page(): return render_template("playfair.html")


# ==========================================
# --- VALIDATION VÀ ROUTE XỬ LÝ (LAB 02) ---
# ==========================================

# --- CAESAR (Ràng buộc: Key phải là số nguyên thuần túy) ---
@app.route("/encrypt", methods=["POST"])
def encrypt_route():
    plain_text = clean_text(request.form.get("inputPlainText", ""))
    raw_key = request.form.get("inputKeyPlain", "").strip()
    
    # Kiểm tra rỗng hoặc chứa ký tự không phải số
    if not raw_key or not raw_key.isdigit():
        return render_template("caesar.html", encrypted_text="LỖI RÀNG BUỘC: Khóa Caesar phải là số nguyên thuần túy (không chứa chữ/ký tự)!", original_text=plain_text, key=raw_key)
        
    key = int(raw_key)
    res = call_crypto_func(CaesarCipher(), "encrypt", plain_text, key)
    return render_template("caesar.html", encrypted_text=res, original_text=plain_text, key=key)

@app.route("/decrypt", methods=["POST"])
def decrypt_route():
    cipher_text = clean_text(request.form.get("inputCipherText", ""))
    raw_key = request.form.get("inputKeyCipher", "").strip()
    
    if not raw_key or not raw_key.isdigit():
        return render_template("caesar.html", decrypted_text="LỖI RÀNG BUỘC: Khóa Caesar phải là số nguyên thuần túy (không chứa chữ/ký tự)!", original_text=cipher_text, key=raw_key)
        
    key = int(raw_key)
    res = call_crypto_func(CaesarCipher(), "decrypt", cipher_text, key)
    return render_template("caesar.html", decrypted_text=res, original_text=cipher_text, key=key)


# --- VIGENERE (Ràng buộc: Key phải hoàn toàn là chữ) ---
@app.route("/vigenere/encrypt", methods=["POST"])
def vigenere_enc():
    plain_text = clean_text(request.form.get("inputPlainText", ""))
    raw_key = request.form.get("inputKeyPlain", "").strip()
    
    if not raw_key or not raw_key.isalpha():
        return render_template("vigenere.html", encrypted_text="LỖI RÀNG BUỘC: Khóa Vigenère phải hoàn toàn là chữ (không chứa số hoặc ký tự đặc biệt)!", original_text=plain_text, key=raw_key)
        
    key = clean_text(raw_key)
    res = call_crypto_func(VigenereCipher(), "encrypt", plain_text, key)
    return render_template("vigenere.html", encrypted_text=res, original_text=plain_text, key=key)

@app.route("/vigenere/decrypt", methods=["POST"])
def vigenere_dec():
    cipher_text = clean_text(request.form.get("inputCipherText", ""))
    raw_key = request.form.get("inputKeyCipher", "").strip()
    
    if not raw_key or not raw_key.isalpha():
        return render_template("vigenere.html", decrypted_text="LỖI RÀNG BUỘC: Khóa Vigenère phải hoàn toàn là chữ (không chứa số hoặc ký tự đặc biệt)!", original_text=cipher_text, key=raw_key)
        
    key = clean_text(raw_key)
    res = call_crypto_func(VigenereCipher(), "decrypt", cipher_text, key)
    return render_template("vigenere.html", decrypted_text=res, original_text=cipher_text, key=key)


# --- RAIL FENCE (Ràng buộc: Key phải là số nguyên thuần túy) ---
@app.route("/railfence/encrypt", methods=["POST"])
def railfence_enc():
    plain_text = clean_text(request.form.get("inputPlainText", ""))
    raw_key = request.form.get("inputKeyPlain", "").strip()
    
    if not raw_key or not raw_key.isdigit():
        return render_template("railfence.html", encrypted_text="LỖI RÀNG BUỘC: Khóa Rail Fence phải là số nguyên thuần túy (không chứa chữ/ký tự)!", original_text=plain_text, key=raw_key)
        
    key = int(raw_key)
    cipher = RailFenceCipher()
    res = cipher.encrypt_rail_fence(plain_text, key)
    return render_template("railfence.html", encrypted_text=res, original_text=plain_text, key=key)

@app.route("/railfence/decrypt", methods=["POST"])
def railfence_dec():
    cipher_text = clean_text(request.form.get("inputCipherText", ""))
    raw_key = request.form.get("inputKeyCipher", "").strip()
    
    if not raw_key or not raw_key.isdigit():
        return render_template("railfence.html", decrypted_text="LỖI RÀNG BUỘC: Khóa Rail Fence phải là số nguyên thuần túy (không chứa chữ/ký tự)!", original_text=cipher_text, key=raw_key)
        
    key = int(raw_key)
    cipher = RailFenceCipher()
    res = cipher.decrypt_rail_fence(cipher_text, key)
    return render_template("railfence.html", decrypted_text=res, original_text=cipher_text, key=key)


# --- PLAYFAIR (Ràng buộc: Key phải hoàn toàn là chữ) ---
@app.route("/playfair/encrypt", methods=["POST"])
def playfair_enc():
    plain_text = clean_text(request.form.get("inputPlainText", ""))
    raw_key = request.form.get("inputKeyPlain", "").strip()
    
    if not raw_key or not raw_key.isalpha():
        return render_template("playfair.html", encrypted_text="LỖI RÀNG BUỘC: Khóa Playfair phải hoàn toàn là chữ (không chứa số hoặc ký tự đặc biệt)!", original_text=plain_text, key=raw_key)
        
    key = clean_text(raw_key)
    cipher = PlayfairCipher()
    res = cipher.encrypt_playfair(plain_text, key)
    return render_template("playfair.html", encrypted_text=res, original_text=plain_text, key=key)

@app.route("/playfair/decrypt", methods=["POST"])
def playfair_dec():
    cipher_text = clean_text(request.form.get("inputCipherText", ""))
    raw_key = request.form.get("inputKeyCipher", "").strip()
    
    if not raw_key or not raw_key.isalpha():
        return render_template("playfair.html", decrypted_text="LỖI RÀNG BUỘC: Khóa Playfair phải hoàn toàn là chữ (không chứa số hoặc ký tự đặc biệt)!", original_text=cipher_text, key=raw_key)
        
    key = clean_text(raw_key)
    cipher = PlayfairCipher()
    res = cipher.decrypt_playfair(cipher_text, key)
    return render_template("playfair.html", decrypted_text=res, original_text=cipher_text, key=key)


# ==========================================
# --- BỔ SUNG ROUTE API RSA (LAB 03) ---
# ==========================================

def load_server_keys():
    pub_path = os.path.join(KEYS_DIR, "publicKey.pem")
    priv_path = os.path.join(KEYS_DIR, "privateKey.pem")
    pub_key, priv_key = None, None
    if os.path.exists(pub_path):
        with open(pub_path, "rb") as f:
            pub_key = rsa.PublicKey.load_pkcs1(f.read())
    if os.path.exists(priv_path):
        with open(priv_path, "rb") as f:
            priv_key = rsa.PrivateKey.load_pkcs1(f.read())
    return priv_key, pub_key

@app.route('/api/rsa/generate_keys', methods=['GET'])
def rsa_generate_keys():
    public_key, private_key = rsa.newkeys(1024)
    with open(os.path.join(KEYS_DIR, "publicKey.pem"), "wb") as f:
        f.write(public_key.save_pkcs1())
    with open(os.path.join(KEYS_DIR, "privateKey.pem"), "wb") as f:
        f.write(private_key.save_pkcs1())
    return jsonify({'message': 'Keys generated successfully'})

@app.route("/api/rsa/encrypt", methods=["POST"])
def rsa_encrypt():
    data = request.json
    message = data['message']
    key_type = data['key_type']
    
    private_key, public_key = load_server_keys()
    key = public_key if key_type == 'public' else private_key
    if not key:
        return jsonify({'error': 'Key not found'}), 400
        
    encrypted_bytes = rsa.encrypt(message.encode('utf-8'), key)
    return jsonify({'encrypted_message': encrypted_bytes.hex()})

@app.route("/api/rsa/decrypt", methods=["POST"])
def rsa_decrypt():
    data = request.json
    ciphertext_hex = data['ciphertext']
    key_type = data['key_type']
    
    private_key, public_key = load_server_keys()
    key = public_key if key_type == 'public' else private_key
    if not key:
        return jsonify({'error': 'Key not found'}), 400
        
    try:
        ciphertext_bytes = bytes.fromhex(ciphertext_hex)
        decrypted_bytes = rsa.decrypt(ciphertext_bytes, key)
        return jsonify({'decrypted_message': decrypted_bytes.decode('utf-8')})
    except Exception:
        return jsonify({'error': 'Decryption failed'}), 400

@app.route('/api/rsa/sign', methods=['POST'])
def rsa_sign_message():
    data = request.json
    message = data['message']
    private_key, _ = load_server_keys()
    if not private_key:
        return jsonify({'error': 'Private key not found'}), 400
    signature_bytes = rsa.sign(message.encode('utf-8'), private_key, 'SHA-1')
    return jsonify({'signature': signature_bytes.hex()})

@app.route('/api/rsa/verify', methods=['POST'])
def rsa_verify_signature():
    data = request.json
    message = data['message']
    signature_hex = data['signature']
    _, public_key = load_server_keys()
    if not public_key:
        return jsonify({'error': 'Public key not found'}), 400
    try:
        signature_bytes = bytes.fromhex(signature_hex)
        rsa.verify(message.encode('utf-8'), signature_bytes, public_key)
        return jsonify({'is_verified': True})
    except rsa.VerificationError:
        return jsonify({'is_verified': False})


if __name__ == "__main__":
    app.run(debug=True, port=5000)