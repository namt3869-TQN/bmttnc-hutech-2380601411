import os
import sys
import rsa

# Khởi tạo đường dẫn plugin để tránh lỗi crash giao diện PyQt5
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = r"..\..\platforms"

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from rsa_ui import Ui_MainWindow  # Import file giao diện

class RSACipherWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Định nghĩa thư mục lưu file khóa keys
        self.keys_dir = os.path.join(os.path.dirname(__file__), "keys")
        if not os.path.exists(self.keys_dir):
            os.makedirs(self.keys_dir)

        # Kết nối sự kiện click của các nút đúng theo giao diện thực tế
        self.ui.btnGenerate.clicked.connect(self.generate_key_clicked)
        self.ui.btnEncrypt.clicked.connect(self.encrypt_clicked)
        self.ui.btnDecrypt.clicked.connect(self.decrypt_clicked)

    def generate_key_clicked(self):
        """Sinh cặp khóa RSA và lưu trực tiếp thành file pem trong thư mục keys"""
        try:
            (public_key, private_key) = rsa.newkeys(1024)

            # Lưu Public Key
            with open(os.path.join(self.keys_dir, "publicKey.pem"), "wb") as f:
                f.write(public_key.save_pkcs1())

            # Lưu Private Key
            with open(os.path.join(self.keys_dir, "privateKey.pem"), "wb") as f:
                f.write(private_key.save_pkcs1())

            QMessageBox.information(self, "Thành công", "Đã sinh cặp khóa và lưu vào thư mục keys!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể sinh khóa: {str(e)}")

    def encrypt_clicked(self):
        """Mã hóa văn bản bằng file publicKey.pem đã sinh"""
        plain_text = self.ui.txtPlain.toPlainText()
        pub_path = os.path.join(self.keys_dir, "publicKey.pem")

        if not os.path.exists(pub_path):
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng bấm Generate Keys trước!")
            return

        try:
            with open(pub_path, "rb") as f:
                pub_key = rsa.PublicKey.load_pkcs1(f.read())

            cipher_bytes = rsa.encrypt(plain_text.encode('utf-8'), pub_key)
            self.ui.txtCipher.setPlainText(cipher_bytes.hex())
        except Exception as e:
            QMessageBox.critical(self, "Lỗi mã hóa", str(e))

    def decrypt_clicked(self):
        """Giải mã văn bản bằng file privateKey.pem đã sinh"""
        cipher_hex = self.ui.txtCipher.toPlainText()
        priv_path = os.path.join(self.keys_dir, "privateKey.pem")

        if not os.path.exists(priv_path):
            QMessageBox.warning(self, "Cảnh báo", "Không tìm thấy file Private Key để giải mã!")
            return

        try:
            with open(priv_path, "rb") as f:
                priv_key = rsa.PrivateKey.load_pkcs1(f.read())

            cipher_bytes = bytes.fromhex(cipher_hex)
            decrypted_bytes = rsa.decrypt(cipher_bytes, priv_key)
            self.ui.txtPlain.setPlainText(decrypted_bytes.decode('utf-8'))
        except Exception as e:
            QMessageBox.critical(self, "Lỗi giải mã", "Giải mã thất bại!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RSACipherWindow()
    window.show()
    sys.exit(app.exec_())