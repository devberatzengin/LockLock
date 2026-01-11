from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QTextEdit, QComboBox
)

class AccountForm(QWidget):
    def __init__(self, categories=None):
        super().__init__()
        # Kategori listesini tuple listesi olarak bekliyoruz: [(id, name), (id, name)]
        self.categories = categories or [] 
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(0,0,0,0)

        # Style Sheets
        input_style = """
            QLineEdit, QComboBox, QTextEdit {
                background-color: #F9FAFB;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                color: #1F2937;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border: 2px solid #2563EB;
                background-color: white;
            }
        """
        self.setStyleSheet(input_style)
        
        # Label Stili
        label_style = "color: #374151; font-weight: 600; font-size: 13px;"

        # --- Fields ---
        
        # Website
        l1 = QLabel("Website / Application")
        l1.setStyleSheet(label_style)
        self.site_input = QLineEdit()
        self.site_input.setPlaceholderText("e.g. google.com")
        self.site_input.setFixedHeight(40)

        # Username
        l2 = QLabel("Username / Email")
        l2.setStyleSheet(label_style)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("e.g. user@example.com")
        self.username_input.setFixedHeight(40)

        # Password
        l3 = QLabel("Password")
        l3.setStyleSheet(label_style)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("••••••••")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(40)

        # Category
        l4 = QLabel("Category")
        l4.setStyleSheet(label_style)
        self.category_box = QComboBox()
        self.category_box.setFixedHeight(40)
        
        # Kategorileri ComboBox'a yükle (UserData: ID)
        if self.categories:
            for cat_id, cat_name in self.categories:
                self.category_box.addItem(cat_name, cat_id)

        # Notes
        l5 = QLabel("Notes (Optional)")
        l5.setStyleSheet(label_style)
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Any additional info...")
        self.notes_input.setFixedHeight(80)

        # Add widgets
        layout.addWidget(l1)
        layout.addWidget(self.site_input)
        layout.addWidget(l2)
        layout.addWidget(self.username_input)
        layout.addWidget(l3)
        layout.addWidget(self.password_input)
        layout.addWidget(l4)
        layout.addWidget(self.category_box)
        layout.addWidget(l5)
        layout.addWidget(self.notes_input)

    def get_data(self):
        # Seçili kategorinin ID'sini alıyoruz
        cat_id = self.category_box.currentData()
        
        return {
            "site": self.site_input.text().strip(),
            "username": self.username_input.text().strip(),
            "password": self.password_input.text(),
            "category_id": cat_id,
            "notes": self.notes_input.toPlainText().strip()
        }