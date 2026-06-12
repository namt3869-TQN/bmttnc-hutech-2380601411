import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTextEdit, QLineEdit

# Tự động nhận diện file UI nằm cùng thư mục playfair
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from playfair_ui import Ui_MainWindow

class PlayfairApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Kết nối nút bấm linh hoạt theo tên Object tương ứng
        if hasattr(self.ui, 'btnEncrypt'):
            self.ui.btnEncrypt.clicked.connect(self.handle_encrypt)
        elif hasattr(self.ui, 'Encrypt'):
            self.ui.Encrypt.clicked.connect(self.handle_encrypt)
            
        if hasattr(self.ui, 'btnDecrypt'):
            self.ui.btnDecrypt.clicked.connect(self.handle_decrypt)
        elif hasattr(self.ui, 'Decrypt'):
            self.ui.Decrypt.clicked.connect(self.handle_decrypt)

    # --- THUẬT TOÁN PLAYFAIR XỬ LÝ TRỰC TIẾP (BẢNG MÃ 5x5 BỎ J) ---
    def generate_matrix(self, key):
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

    def find_position(self, matrix, char):
        for r in range(5):
            for c in range(5):
                if matrix[r][c] == char:
                    return r, c
        return None

    def prepare_text(self, text):
        text = "".join([c for c in text.upper() if c.isalpha()]).replace('J', 'I')
        prepared = []
        i = 0
        while i < len(text):
            char1 = text[i]
            char2 = text[i+1] if (i + 1) < len(text) else 'X'
            if char1 == char2:
                prepared.append(char1 + 'X')
                i += 1
            else:
                prepared.append(char1 + char2)
                i += 2
        return prepared

    def playfair_encrypt(self, text, key):
        matrix = self.generate_matrix(key)
        pairs = self.prepare_text(text)
        res = []
        
        for p1, p2 in pairs:
            r1, c1 = self.find_position(matrix, p1)
            r2, c2 = self.find_position(matrix, p2)
            
            if r1 == r2:
                res.append(matrix[r1][(c1 + 1) % 5] + matrix[r2][(c2 + 1) % 5])
            elif c1 == c2:
                res.append(matrix[(r1 + 1) % 5][c1] + matrix[(r2 + 1) % 5][c2])
            else:
                res.append(matrix[r1][c2] + matrix[r2][c1])
        return "".join(res)

    def playfair_decrypt(self, cipher, key):
        matrix = self.generate_matrix(key)
        cipher = "".join([c for c in cipher.upper() if c.isalpha()])
        res = []
        
        for i in range(0, len(cipher), 2):
            if i + 1 >= len(cipher): break
            p1, p2 = cipher[i], cipher[i+1]
            r1, c1 = self.find_position(matrix, p1)
            r2, c2 = self.find_position(matrix, p2)
            
            if r1 == r2:
                res.append(matrix[r1][(c1 - 1 + 5) % 5] + matrix[r2][(c2 - 1 + 5) % 5])
            elif c1 == c2:
                res.append(matrix[(r1 - 1 + 5) % 5][c1] + matrix[(r2 - 1 + 5) % 5][c2])
            else:
                res.append(matrix[r1][c2] + matrix[r2][c1])
        return "".join(res)
    # -------------------------------------------------------------

    def get_fields(self):
        """Quét thông minh lấy đúng 3 ô nhập liệu trên form"""
        text_edits = self.findChildren(QTextEdit)
        line_edits = self.findChildren(QLineEdit)
        
        txt_plain = text_edits[0] if len(text_edits) > 0 else None
        txt_key = line_edits[0] if len(line_edits) > 0 else None
        txt_cipher = self.ui.txtCipher if hasattr(self.ui, 'txtCipher') else (text_edits[1] if len(text_edits) > 1 else None)
        
        return txt_plain, txt_key, txt_cipher

    def handle_encrypt(self):
        txt_plain, txt_key, txt_cipher = self.get_fields()
        if not txt_plain or not txt_key or not txt_cipher:
            QMessageBox.critical(self, "Lỗi Giao Diện", "Không tìm thấy cấu trúc ô nhập liệu!")
            return
            
        plain_text = txt_plain.toPlainText().strip()
        key = txt_key.text().strip()
        
        # RÀNG BUỘC: Khóa Playfair phải hoàn toàn là chữ
        if not key or not key.isalpha():
            QMessageBox.warning(self, "LỖI RÀNG BUỘC", "Khóa Playfair phải hoàn toàn là chữ (không chứa số hoặc ký tự đặc biệt)!")
            return
            
        try:
            res = self.playfair_encrypt(plain_text, key)
            txt_cipher.setPlainText(res)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Mã hóa thất bại: {str(e)}")

    def handle_decrypt(self):
        txt_plain, txt_key, txt_cipher = self.get_fields()
        if not txt_plain or not txt_key or not txt_cipher:
            QMessageBox.critical(self, "Lỗi Giao Diện", "Không tìm thấy cấu trúc ô nhập liệu!")
            return
            
        cipher_text = txt_cipher.toPlainText().strip()
        key = txt_key.text().strip()
        
        if not key or not key.isalpha():
            QMessageBox.warning(self, "LỖI RÀNG BUỘC", "Khóa Playfair phải hoàn toàn là chữ (không chứa số hoặc ký tự đặc biệt)!")
            return
            
        try:
            res = self.playfair_decrypt(cipher_text, key)
            txt_plain.setPlainText(res)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Giải mã thất bại: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlayfairApp()
    window.show()
    sys.exit(app.exec_())