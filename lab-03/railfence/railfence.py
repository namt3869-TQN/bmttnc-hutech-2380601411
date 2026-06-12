import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTextEdit, QLineEdit

# Tự động nhận diện file UI nằm cùng thư mục railfence
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from railfence_ui import Ui_MainWindow

class RailFenceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Kết nối nút bấm linh hoạt theo tên Object
        if hasattr(self.ui, 'btnEncrypt'):
            self.ui.btnEncrypt.clicked.connect(self.handle_encrypt)
        elif hasattr(self.ui, 'Encrypt'):
            self.ui.Encrypt.clicked.connect(self.handle_encrypt)
            
        if hasattr(self.ui, 'btnDecrypt'):
            self.ui.btnDecrypt.clicked.connect(self.handle_decrypt)
        elif hasattr(self.ui, 'Decrypt'):
            self.ui.Decrypt.clicked.connect(self.handle_decrypt)

    # --- THUẬT TOÁN RAIL FENCE XỬ LÝ TRỰC TIẾP ---
    def rail_fence_encrypt(self, text, key):
        if key == 1: return text
        rail = [['\n' for _ in range(len(text))] for _ in range(key)]
        dir_down = False
        row, col = 0, 0
        
        for i in range(len(text)):
            if (row == 0) or (row == key - 1):
                dir_down = not dir_down
            rail[row][col] = text[i]
            col += 1
            row += 1 if dir_down else -1
            
        res = []
        for i in range(key):
            for j in range(len(text)):
                if rail[i][j] != '\n':
                    res.append(rail[i][j])
        return "".join(res)

    def rail_fence_decrypt(self, cipher, key):
        if key == 1: return cipher
        rail = [['\n' for _ in range(len(cipher))] for _ in range(key)]
        dir_down = None
        row, col = 0, 0
        
        for i in range(len(cipher)):
            if row == 0: dir_down = True
            if row == key - 1: dir_down = False
            rail[row][col] = '*'
            col += 1
            row += 1 if dir_down else -1
            
        index = 0
        for i in range(key):
            for j in range(len(cipher)):
                if (rail[i][j] == '*') and (index < len(cipher)):
                    rail[i][j] = cipher[index]
                    index += 1
                    
        res = []
        row, col = 0, 0
        for i in range(len(cipher)):
            if row == 0: dir_down = True
            if row == key - 1: dir_down = False
            if rail[row][col] != '*':
                res.append(rail[row][col])
                col += 1
            row += 1 if dir_down else -1
        return "".join(res)
    # -------------------------------------------

    def get_fields(self):
        """Quét thông minh lấy đúng 3 ô nhập liệu bất kể đặt tên gì"""
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
            
        plain_text = txt_plain.toPlainText().strip().upper()
        raw_key = txt_key.text().strip()
        
        # RÀNG BUỘC: Key phải là số nguyên thuần túy
        if not raw_key or not raw_key.isdigit():
            QMessageBox.warning(self, "LỖI RÀNG BUỘC", "Khóa Rail Fence phải là số nguyên thuần túy (không chứa chữ hoặc ký tự đặc biệt)!")
            return
            
        key = int(raw_key)
        try:
            res = self.rail_fence_encrypt(plain_text, key)
            txt_cipher.setPlainText(res)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Mã hóa thất bại: {str(e)}")

    def handle_decrypt(self):
        txt_plain, txt_key, txt_cipher = self.get_fields()
        
        if not txt_plain or not txt_key or not txt_cipher:
            QMessageBox.critical(self, "Lỗi Giao Diện", "Không tìm thấy cấu trúc ô nhập liệu!")
            return
            
        cipher_text = txt_cipher.toPlainText().strip().upper()
        raw_key = txt_key.text().strip()
        
        if not raw_key or not raw_key.isdigit():
            QMessageBox.warning(self, "LỖI RÀNG BUỘC", "Khóa Rail Fence phải là số nguyên thuần túy (không chứa chữ hoặc ký tự đặc biệt)!")
            return
            
        key = int(raw_key)
        try:
            res = self.rail_fence_decrypt(cipher_text, key)
            txt_plain.setPlainText(res)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Giải mã thất bại: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RailFenceApp()
    window.show()
    sys.exit(app.exec_())