import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTextEdit, QLineEdit

# Tự động nhận diện file UI nằm cùng thư mục vigenere
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from vigenere_ui import Ui_MainWindow

class VigenereApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Kết nối nút bấm theo đúng tên trong Object Inspector của ông
        if hasattr(self.ui, 'btnEncrypt'):
            self.ui.btnEncrypt.clicked.connect(self.handle_encrypt)
        elif hasattr(self.ui, 'Encrypt'):
            self.ui.Encrypt.clicked.connect(self.handle_encrypt)
            
        if hasattr(self.ui, 'btnDecrypt'):
            self.ui.btnDecrypt.clicked.connect(self.handle_decrypt)
        elif hasattr(self.ui, 'Decrypt'):
            self.ui.Decrypt.clicked.connect(self.handle_decrypt)

    # --- THUẬT TOÁN VIGENERE XỬ LÝ TRỰC TIẾP ---
    def vigenere_encrypt(self, text, key):
        res = []
        key_idx = 0
        for char in text:
            if char.isalpha():
                shift = ord(key[key_idx % len(key)]) - ord('A')
                new_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                res.append(new_char)
                key_idx += 1
            else:
                res.append(char)
        return "".join(res)

    def vigenere_decrypt(self, text, key):
        res = []
        key_idx = 0
        for char in text:
            if char.isalpha():
                shift = ord(key[key_idx % len(key)]) - ord('A')
                new_char = chr((ord(char) - ord('A') - shift + 26) % 26 + ord('A'))
                res.append(new_char)
                key_idx += 1
            else:
                res.append(char)
        return "".join(res)
    # -------------------------------------------

    def get_fields(self):
        """Hàm quét thông minh để lấy đúng 3 ô nhập liệu bất kể đặt tên gì"""
        text_edits = self.findChildren(QTextEdit)
        line_edits = self.findChildren(QLineEdit)
        
        # Mặc định gán dựa theo thứ tự xuất hiện trên giao diện từ trên xuống
        txt_plain = text_edits[0] if len(text_edits) > 0 else None
        txt_key = line_edits[0] if len(line_edits) > 0 else None
        
        # Ô CipherText của ông tên là txtCipher, nếu có thì bốc chính xác nó
        txt_cipher = self.ui.txtCipher if hasattr(self.ui, 'txtCipher') else (text_edits[1] if len(text_edits) > 1 else None)
        
        return txt_plain, txt_key, txt_cipher

    def handle_encrypt(self):
        txt_plain, txt_key, txt_cipher = self.get_fields()
        
        if not txt_plain or not txt_key or not txt_cipher:
            QMessageBox.critical(self, "Lỗi Giao Diện", "Không tìm thấy cấu trúc ô nhập liệu phù hợp!")
            return
            
        plain_text = txt_plain.toPlainText().strip().upper()
        key = txt_key.text().strip().upper()
        
        if not key or not key.isalpha():
            QMessageBox.warning(self, "LỖI RÀNG BUỘC", "Khóa Vigenère phải hoàn toàn là chữ (không chứa số hoặc ký tự đặc biệt)!")
            return
            
        try:
            res = self.vigenere_encrypt(plain_text, key)
            txt_cipher.setPlainText(res)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Mã hóa thất bại: {str(e)}")

    def handle_decrypt(self):
        txt_plain, txt_key, txt_cipher = self.get_fields()
        
        if not txt_plain or not txt_key or not txt_cipher:
            QMessageBox.critical(self, "Lỗi Giao Diện", "Không tìm thấy cấu trúc ô nhập liệu phù hợp!")
            return
            
        cipher_text = txt_cipher.toPlainText().strip().upper()
        key = txt_key.text().strip().upper()
        
        if not key or not key.isalpha():
            QMessageBox.warning(self, "LỖI RÀNG BUỘC", "Khóa Vigenère phải hoàn toàn là chữ (không chứa số hoặc ký tự đặc biệt)!")
            return
            
        try:
            res = self.vigenere_decrypt(cipher_text, key)
            txt_plain.setPlainText(res)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Giải mã thất bại: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VigenereApp()
    window.show()
    sys.exit(app.exec_())