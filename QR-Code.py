import sys
import io
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QFileDialog, QMessageBox
)
from PyQt5.QtGui import QPixmap, QImage


class GenerateTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Giriş alanı: Metin veya URL
        self.input_label = QLabel("QR Kod için metin veya URL:")
        self.input_text = QLineEdit()
        layout.addWidget(self.input_label)
        layout.addWidget(self.input_text)

        # Kaydedilecek dosya adı için alan
        self.filename_label = QLabel("Kaydedilecek dosya adı (örn: qrcode.png):")
        self.filename_edit = QLineEdit()
        layout.addWidget(self.filename_label)
        layout.addWidget(self.filename_edit)

        # QR kod oluşturma butonu
        self.generate_button = QPushButton("QR Kod Oluştur")
        layout.addWidget(self.generate_button)
        self.generate_button.clicked.connect(self.generate_qr)

        # Oluşturulan QR kodun gösterileceği etiket
        self.image_label = QLabel()
        self.image_label.setFixedSize(220, 220)
        self.image_label.setStyleSheet("border: 1px solid gray;")
        layout.addWidget(self.image_label)

        self.setLayout(layout)

    def generate_qr(self):
        data = self.input_text.text().strip()
        filename = self.filename_edit.text().strip()

        if not data:
            QMessageBox.warning(self, "Uyarı", "Lütfen metin veya URL giriniz!")
            return
        if not filename:
            QMessageBox.warning(self, "Uyarı", "Lütfen kaydedilecek dosya adını giriniz!")
            return

        # QR kod oluşturuluyor
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Dosyaya kaydetme
        try:
            img.save(filename)
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Dosya kaydedilemedi: {e}")
            return

        QMessageBox.information(self, "Başarılı", f"QR Kod başarıyla '{filename}' olarak kaydedildi.")

        # PIL Image'dan QPixmap'e çevirme
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        qimg = QImage.fromData(buf.read(), 'PNG')
        pixmap = QPixmap.fromImage(qimg)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.width(),
                                                   self.image_label.height()))


class ReadTab(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_file = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Dosya seçme butonu ve seçilen dosyanın yolu
        self.select_file_button = QPushButton("Dosya Seç")
        self.file_label = QLabel("Seçilen dosya: Yok")
        layout.addWidget(self.select_file_button)
        layout.addWidget(self.file_label)
        self.select_file_button.clicked.connect(self.select_file)

        # QR kod okuma butonu
        self.decode_button = QPushButton("QR Kod Oku")
        layout.addWidget(self.decode_button)
        self.decode_button.clicked.connect(self.decode_qr)

        # Okunan QR kod içeriğinin gösterileceği etiket
        self.result_label = QLabel("QR kod içeriği:")
        self.result_label.setWordWrap(True)
        layout.addWidget(self.result_label)

        # Seçilen resmin gösterileceği alan
        self.image_label = QLabel()
        self.image_label.setFixedSize(220, 220)
        self.image_label.setStyleSheet("border: 1px solid gray;")
        layout.addWidget(self.image_label)

        self.setLayout(layout)

    def select_file(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "QR Kod Resmi Seç",
            "",
            "Image Files (*.png *.jpg *.bmp);;All Files (*)",
            options=options
        )
        if filename:
            self.selected_file = filename
            self.file_label.setText(f"Seçilen dosya: {filename}")
            pixmap = QPixmap(filename)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.width(),
                                                     self.image_label.height()))

    def decode_qr(self):
        if not self.selected_file:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir dosya seçiniz!")
            return

        try:
            img = Image.open(self.selected_file)
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Resim dosyası açılamadı: {e}")
            return

        decoded_objects = decode(img)
        if not decoded_objects:
            QMessageBox.warning(self, "Uyarı", "QR kod bulunamadı veya okunamadı!")
            self.result_label.setText("QR kod içeriği:")
        else:
            # Birden fazla QR kod varsa hepsini listeleyebiliriz
            texts = [obj.data.decode("utf-8") for obj in decoded_objects]
            result_text = "\n".join(texts)
            self.result_label.setText("QR kod içeriği:\n" + result_text)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Kod Üretici ve Okuyucu")
        self.setGeometry(100, 100, 400, 550)
        self.init_ui()

    def init_ui(self):
        # QTabWidget ile iki sekme oluşturuluyor: QR Kod Oluştur ve QR Kod Oku
        self.tabs = QTabWidget()
        self.generate_tab = GenerateTab()
        self.read_tab = ReadTab()

        self.tabs.addTab(self.generate_tab, "QR Kod Oluştur")
        self.tabs.addTab(self.read_tab, "QR Kod Oku")

        self.setCentralWidget(self.tabs)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
