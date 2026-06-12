import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTextEdit, QFileDialog, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from stego_ui import Ui_MainWindow

class StegoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        if hasattr(self.ui, 'btnEncrypt'):
            self.ui.btnEncrypt.clicked.connect(self.handle_encrypt)
        elif hasattr(self.ui, 'Encrypt'):
            self.ui.Encrypt.clicked.connect(self.handle_encrypt)
            
        if hasattr(self.ui, 'btnDecrypt'):
            self.ui.btnDecrypt.clicked.connect(self.handle_decrypt)
        elif hasattr(self.ui, 'Decrypt'):
            self.ui.Decrypt.clicked.connect(self.handle_decrypt)

    def get_fields(self):
        text_edits = self.findChildren(QTextEdit)
        txt_plain = text_edits[0] if len(text_edits) > 0 else None
        txt_cipher = self.ui.txtCipherText if hasattr(self.ui, 'txtCipherText') else (text_edits[1] if len(text_edits) > 1 else None)
        return txt_plain, txt_cipher

    def display_image_on_ui(self, file_path):
        """Hàm hỗ trợ hiển thị ảnh co giãn vừa khít khung lblImage trên giao diện"""
        lbl_img = self.findChild(QLabel, 'lblImage')
        if lbl_img:
            pixmap = QPixmap(file_path)
            # Tự động co giãn ảnh vừa khít với kích thước ô chứa trên giao diện
            scaled_pixmap = pixmap.scaled(lbl_img.width(), lbl_img.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            lbl_img.setPixmap(scaled_pixmap)

    def handle_encrypt(self):
        txt_plain, _ = self.get_fields()
        if not txt_plain: return
        
        message = txt_plain.toPlainText().strip()
        if not message:
            QMessageBox.warning(self, "Thông báo", "Vui lòng gõ văn bản muốn giấu vào ô Plain Text!")
            return
            
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn ảnh gốc (.png)", "", "Images (*.png)")
        if not file_path: return
        
        # HIỂN THỊ ẢNH GỐC LÊN FORM
        self.display_image_on_ui(file_path)
        
        try:
            img = Image.open(file_path).convert('RGB')
            encoded = img.copy()
            width, height = img.size
            
            message += "#####" 
            binary_msg = ''.join([format(ord(i), "08b") for i in message])
            data_idx = 0
            
            for y in range(height):
                for x in range(width):
                    r, g, b = img.getpixel((x, y))
                    if data_idx < len(binary_msg):
                        r = (r & ~1) | int(binary_msg[data_idx])
                        data_idx += 1
                    if data_idx < len(binary_msg):
                        g = (g & ~1) | int(binary_msg[data_idx])
                        data_idx += 1
                    if data_idx < len(binary_msg):
                        b = (b & ~1) | int(binary_msg[data_idx])
                        data_idx += 1
                    encoded.putpixel((x, y), (r, g, b))
                    if data_idx >= len(binary_msg): break
                if data_idx >= len(binary_msg): break
                
            save_path, _ = QFileDialog.getSaveFileName(self, "Lưu ảnh đã mã hóa giấu tin", "stego_encrypted.png", "Images (*.png)")
            if save_path:
                encoded.save(save_path)
                QMessageBox.information(self, "Thành công", f"Đã mã hóa thành công! Ảnh mới đã được lưu.")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Mã hóa thất bại: {str(e)}")

    def handle_decrypt(self):
        _, txt_cipher = self.get_fields()
        if not txt_cipher: return
        
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn ảnh cần giải mã (.png)", "", "Images (*.png)")
        if not file_path: return
        
        # HIỂN THỊ ẢNH CẦN GIẢI MÃ LÊN FORM
        self.display_image_on_ui(file_path)
        
        try:
            img = Image.open(file_path).convert('RGB')
            width, height = img.size
            binary_data = ""
            
            for y in range(height):
                for x in range(width):
                    r, g, b = img.getpixel((x, y))
                    binary_data += str(r & 1)
                    binary_data += str(g & 1)
                    binary_data += str(b & 1)
                    
            all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
            decoded_text = ""
            for byte in all_bytes:
                decoded_text += chr(int(byte, 2))
                if decoded_text.endswith("#####"):
                    decoded_text = decoded_text[:-5]
                    break
                    
            txt_cipher.setPlainText(decoded_text)
            QMessageBox.information(self, "Thành công", "Đã giải mã bóc tách tin nhắn từ ảnh thành công!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Giải mã thất bại: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StegoApp()
    window.show()
    sys.exit(app.exec_())