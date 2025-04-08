import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt6.QtGui import QKeySequence, QShortcut
import re


class ValidationApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("Validation Form.ui", self)

        # Set default text untuk no hp
        self.LineEditNoHP.setText("+62 ")
        self.LineEditNoHP.textChanged.connect(self.format_phone_number)

        self.pushButton.clicked.connect(self.validate_and_save)
        self.pushButton_2.clicked.connect(self.clear_fields)

        shortcut_quit = QShortcut(QKeySequence("Q"), self)
        shortcut_quit.activated.connect(self.close)

    def format_phone_number(self):
        current_text = self.LineEditNoHP.text()

        if not current_text.startswith("+62"):
            current_text = "+62 " + current_text.lstrip("+62")

        numbers = re.sub(r"\D", "", current_text[4:])  # ambil hanya angka setelah '+62 '

        # Format jadi +62 xxx xxxx xxxx
        formatted = "+62"
        if numbers:
            parts = [numbers[:3], numbers[3:7], numbers[7:]]
            formatted_parts = [p for p in parts if p]
            formatted = "+62 " + " ".join(formatted_parts)

        self.LineEditNoHP.blockSignals(True)
        self.LineEditNoHP.setText(formatted)
        self.LineEditNoHP.blockSignals(False)

    def validate_and_save(self):
        age = self.LineEditAge.text().strip()
        phone = self.LineEditNoHP.text().strip()

        # Validasi khusus Age
        if not age.isdigit():
            self.show_warning("Umur harus berupa angka.")
            return

        if not age:
            self.show_warning("Form Umur tidak boleh kosong.")
            return

        # Validasi khusus No HP: minimal 11 digit setelah +62
        phone_digits = re.sub(r"\D", "", phone[3:])  # hanya angka setelah '+62'
        if len(phone_digits) < 11:
            self.show_warning("Nomor HP harus minimal 11 digit setelah +62.")
            return

        # Kalau semua validasi khusus lolos
        QMessageBox.information(self, "Sukses", "Data berhasil disimpan!")
        self.clear_fields()

    def clear_fields(self):
        self.LineEditName.clear()
        self.LineEditEmail.clear()
        self.LineEditAge.clear()
        self.LineEditNoHP.setText("+62 ")
        self.textEdit.clear()
        self.comboBox_2.setCurrentIndex(0)
        self.comboBox.setCurrentIndex(0)

    def show_warning(self, message):
        QMessageBox.warning(self, "Peringatan", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ValidationApp()
    window.show()
    sys.exit(app.exec())