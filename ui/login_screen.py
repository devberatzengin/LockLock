from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QColor  # <--- EKLENDİ: Renk sınıfı buradan gelir

class LoginScreen(QMainWindow):
    login_requested = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("LockLock")
        self.setFixedSize(400, 580)
        
        # Arka plana yumuşak degrade
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 #EEF2FF, stop:1 #E0E7FF);
            }
        """)
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        main_layout.setAlignment(Qt.AlignCenter)

        # --- Kart ---
        card = QFrame()
        card.setFixedSize(340, 440)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 24px;
                border: 1px solid #FFFFFF;
            }
        """)
        
        # Soft Gölge
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setXOffset(0)
        shadow.setYOffset(15)
        
        # HATA BURADAYDI, DÜZELTİLDİ: Qt.Color -> QColor
        shadow.setColor(QColor(0, 0, 0, 30)) 
        
        card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(35, 45, 35, 45)
        card_layout.setSpacing(25)

        # Başlık
        title = QLabel("LockLock")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            color: #111827;
            font-size: 32px;
            font-weight: 900;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            letter-spacing: -0.5px;
        """)

        subtitle = QLabel("Your digital vault")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            color: #6B7280;
            font-size: 15px;
            font-weight: 500;
            margin-bottom: 10px;
        """)

        # Input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Master Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(55)
        self.password_input.setAlignment(Qt.AlignCenter)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #F3F4F6;
                border: 2px solid transparent;
                border-radius: 16px;
                padding: 0 15px;
                font-size: 16px;
                color: #1F2937;
                font-weight: bold;
            }
            QLineEdit:focus {
                background-color: white;
                border: 2px solid #4F46E5; /* İndigo Rengi */
            }
        """)
        self.password_input.returnPressed.connect(self._emit_login)

        # Buton
        self.login_button = QPushButton("Unlock")
        self.login_button.setFixedHeight(55)
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.clicked.connect(self._emit_login)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #4F46E5;
                color: white;
                border-radius: 16px;
                font-weight: 700;
                font-size: 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #4338CA;
            }
            QPushButton:pressed {
                background-color: #3730A3;
                padding-top: 2px;
            }
        """)

        self.error_label = QLabel("")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setWordWrap(True)
        self.error_label.setStyleSheet("color: #EF4444; font-size: 13px; font-weight: 600; margin-top: 5px;")
        self.error_label.hide()

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
        self.password_input.setFocus()
        self.password_input.selectAll()
        self.password_input.setStyleSheet(self.password_input.styleSheet().replace("#4F46E5", "#EF4444"))

    def clear(self):
        self.password_input.clear()
        self.error_label.hide()
        self.password_input.setStyleSheet(self.password_input.styleSheet().replace("#EF4444", "#4F46E5"))