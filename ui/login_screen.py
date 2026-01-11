from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import pyqtSignal, Qt

class LoginScreen(QMainWindow):
    login_requested = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("LockLock - Secure Login")
        self.setFixedSize(400, 500)
        self.setStyleSheet("background-color: #F3F4F6;")  # Açık gri modern arka plan
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        
        # Ana Layout (Merkezleme için)
        main_layout = QVBoxLayout(central)
        main_layout.setAlignment(Qt.AlignCenter)

        # --- Kart Tasarımı ---
        card = QFrame()
        card.setFixedSize(340, 400)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 16px;
                border: 1px solid #E5E7EB;
            }
        """)
        
        # Kart Gölgesi
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(Qt.black) # type: ignore
        card.setGraphicsEffect(shadow)

        # Kart İçeriği
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 40, 30, 40)
        card_layout.setSpacing(20)

        # Logo / Başlık
        title = QLabel("LockLock")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            color: #111827;
            font-size: 26px;
            font-weight: 800;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        """)

        subtitle = QLabel("Master Password Required")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #6B7280; font-size: 14px; margin-bottom: 10px;")

        # Input Alanı
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your master key...")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(45)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #F9FAFB;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                padding: 0 12px;
                font-size: 14px;
                color: #1F2937;
            }
            QLineEdit:focus {
                border: 2px solid #2563EB;
                background-color: white;
            }
        """)
        self.password_input.returnPressed.connect(self._emit_login)

        # Buton
        self.login_button = QPushButton("Unlock Vault")
        self.login_button.setFixedHeight(45)
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.clicked.connect(self._emit_login)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                border-radius: 8px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
            QPushButton:pressed {
                background-color: #1E40AF;
            }
        """)

        # Hata Mesajı
        self.error_label = QLabel("")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setWordWrap(True)
        self.error_label.setStyleSheet("color: #DC2626; font-size: 13px; font-weight: 500;")
        self.error_label.hide()

        # Widgetları Ekleme
        card_layout.addStretch()
        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addWidget(self.password_input)
        card_layout.addWidget(self.login_button)
        card_layout.addWidget(self.error_label)
        card_layout.addStretch()

        main_layout.addWidget(card)

    def _emit_login(self):
        password = self.password_input.text().strip()
        if password:
            self.login_requested.emit(password)

    def show_error(self, message: str):
        self.error_label.setText(message)
        self.error_label.show()
        # Hata durumunda input'u salla veya temizle (opsiyonel)
        self.password_input.setFocus()
        self.password_input.selectAll()

    def clear(self):
        self.password_input.clear()
        self.error_label.hide()