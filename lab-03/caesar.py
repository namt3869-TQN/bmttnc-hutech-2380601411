import os
import sys

# Giữ nguyên dòng cấu hình tránh lỗi plugin giao diện
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = r".\platforms"

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from caesar_ui import Ui_MainWindow  # Import giao diện từ file caesar_ui.py


class CaesarWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Kết nối sự kiện click chuột của nút bấm với hàm xử lý
        self.ui.btnEncrypt.clicked.connect(self.encrypt_clicked)
        self.ui.btnDecrypt.clicked.connect(self.decrypt_clicked)

    def caesar_cipher(self, text, key, mode="encrypt"):
        """Hàm xử lý thuật toán Caesar cho cả mã hóa và giải mã"""
        result = ""
        # Nếu là giải mã (decrypt), ta đảo ngược dấu của khóa key
        if mode == "decrypt":
            key = -key

        for char in text:
            if char.isalpha():  # Chỉ xử lý ký tự chữ cái
                start = ord("A") if char.isupper() else ord("a")
                # Công thức mã hóa dịch chuyển Caesar
                result += chr((ord(char) - start + key) % 26 + start)
            else:
                result += char  # Giữ nguyên ký tự đặc biệt, khoảng trắng, số
        return result

    def encrypt_clicked(self):
        """Xử lý khi nhấn nút Encrypt"""
        plain_text = self.ui.txtPlain.toPlainText()
        key_str = self.ui.txtKey.text()

        # Kiểm tra điều kiện đầu vào của khóa Key
        if not key_str.isdigit():
            QMessageBox.warning(
                self, "Lỗi nhập liệu", "Khóa dữ liệu (Key) phải là một số nguyên!"
            )
            return

        key = int(key_str)
        # Chạy thuật toán và hiển thị kết quả lên ô CipherText
        cipher_text = self.caesar_cipher(plain_text, key, mode="encrypt")
        self.ui.txtCipher.setPlainText(cipher_text)

    def decrypt_clicked(self):
        """Xử lý khi nhấn nút Decrypt"""
        cipher_text = self.ui.txtCipher.toPlainText()
        key_str = self.ui.txtKey.text()

        # Kiểm tra điều kiện đầu vào của khóa Key
        if not key_str.isdigit():
            QMessageBox.warning(
                self, "Lỗi nhập liệu", "Khóa dữ liệu (Key) phải là một số nguyên!"
            )
            return

        key = int(key_str)
        # Chạy thuật toán ngược và hiển thị kết quả về lại ô Plain Text
        plain_text = self.caesar_cipher(cipher_text, key, mode="decrypt")
        self.ui.txtPlain.setPlainText(plain_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CaesarWindow()
    window.show()
    sys.exit(app.exec_())