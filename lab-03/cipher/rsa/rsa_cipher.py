import os
import sys
import requests

# Khởi tạo đường dẫn plugin để tránh lỗi crash giao diện PyQt5
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = r"..\..\platforms"

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from rsa_ui import Ui_MainWindow  # Import file giao diện

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Kết nối sự kiện click của các nút chuẩn đét theo Qt Designer đã sửa
        self.ui.btn_gen_keys.clicked.connect(self.call_api_gen_keys)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)
        self.ui.btn_sign.clicked.connect(self.call_api_sign)
        self.ui.btn_verify.clicked.connect(self.call_api_verify)

    def call_api_gen_keys(self):
        url = "http://127.0.0.1:5000/api/rsa/generate_keys"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                QMessageBox.information(self, "Thành công", data["message"])
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Lỗi kết nối", str(e))

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/encrypt"
        payload = {
            "message": self.ui.txt_plain_text.toPlainText(),
            "key_type": "public"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_cipher_text.setText(data["encrypted_message"])
                QMessageBox.information(self, "Thành công", "Encrypted Successfully")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Lỗi kết nối", str(e))

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/decrypt"
        payload = {
            "ciphertext": self.ui.txt_cipher_text.toPlainText(),
            "key_type": "private"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_plain_text.setText(data["decrypted_message"])
                QMessageBox.information(self, "Thành công", "Decrypted Successfully")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Lỗi kết nối", str(e))

    def call_api_sign(self):
        url = "http://127.0.0.1:5000/api/rsa/sign"
        payload = {
            "message": self.ui.txt_info.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_sign.setText(data["signature"])
                QMessageBox.information(self, "Thành công", "Signed Successfully")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Lỗi kết nối", str(e))

    def call_api_verify(self):
        url = "http://127.0.0.1:5000/api/rsa/verify"
        payload = {
            "message": self.ui.txt_info.toPlainText(),
            "signature": self.ui.txt_sign.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                if data["is_verified"]:
                    QMessageBox.information(self, "Xác thực", "Verified Successfully")
                else:
                    QMessageBox.warning(self, "Xác thực", "Verified Fail")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Lỗi kết nối", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())