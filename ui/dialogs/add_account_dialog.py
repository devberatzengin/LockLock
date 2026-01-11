from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QTextEdit, QComboBox, QScrollArea,
    QWidget
)
from PyQt5.QtCore import Qt


class AddAccountDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Account")
        self.setFixedSize(420, 520)
        self._build_ui()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # ===== Scroll Area =====
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        title = QLabel("Add Account")
        title.setStyleSheet("font-size: 18px; font-weight: 600;")

        # -------- Inputs --------
        self.site_input = self._input("Website")
        self.username_input = self._input("Username / Email")
        self.password_input = self._input("Password", password=True)

        self.category_box = QComboBox()
        self.category_box.addItems(["Social", "Work", "Finance", "Other"])
        self.category_box.setFixedHeight(38)

        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Notes (optional)")
        self.notes_input.setFixedHeight(100)

        layout.addWidget(title)
        layout.addWidget(self.site_input)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(QLabel("Category"))
        layout.addWidget(self.category_box)
        layout.addWidget(QLabel("Notes"))
        layout.addWidget(self.notes_input)

        layout.addStretch()
        scroll.setWidget(content)

        # ===== Buttons =====
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(20, 10, 20, 20)
        btn_layout.setSpacing(10)

        cancel_btn = QPushButton("Cancel")
        save_btn = QPushButton("Save")

        for btn in (cancel_btn, save_btn):
            btn.setFixedHeight(36)
            btn.setStyleSheet("""
                QPushButton {
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #333333;
                }
            """)

        cancel_btn.clicked.connect(self.reject)
        save_btn.clicked.connect(self.accept)

        btn_layout.addStretch()
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)

        main_layout.addWidget(scroll)
        main_layout.addLayout(btn_layout)

    def _input(self, placeholder, password=False):
        inp = QLineEdit()
        inp.setPlaceholderText(placeholder)
        inp.setFixedHeight(38)
        if password:
            inp.setEchoMode(QLineEdit.Password)
        return inp

    # Controller ilerde buradan veriyi alacak
    def get_form_data(self):
        return {
            "site": self.site_input.text(),
            "username": self.username_input.text(),
            "password": self.password_input.text(),
            "category": self.category_box.currentText(),
            "notes": self.notes_input.toPlainText()
        }
