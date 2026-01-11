from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QTextEdit, QComboBox
)

class AccountForm(QWidget):
    def __init__(self, categories=None):
        super().__init__()
        self.categories = categories or [] 
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)

        # Style - DÜZELTİLDİ
        self.setStyleSheet("""
            QLabel {
                color: #374151;
                font-weight: 700;
                font-size: 13px;
                margin-bottom: 4px;
            }
            QLineEdit, QComboBox, QTextEdit {
                background-color: #F9FAFB;
                border: 1px solid #E5E7EB;
                border-radius: 10px;
                padding: 8px 12px; /* Padding azaltıldı, yazı sığsın */
                font-size: 14px;
                color: #1F2937;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border: 2px solid #4F46E5;
                background-color: white;
            }
            
            /* ComboBox Açılır Menü Düzeltmesi */
            QComboBox::drop-down {
                border: 0px;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: #1F2937;
                selection-background-color: #4F46E5;
                selection-color: white;
                border: 1px solid #E5E7EB;
                outline: none;
            }
        """)

        # Fields
        layout.addWidget(QLabel("Website / Service"))
        self.site_input = QLineEdit()
        self.site_input.setPlaceholderText("e.g. Netflix")
        self.site_input.setFixedHeight(42) # Yükseklik biraz kısıldı
        layout.addWidget(self.site_input)

        layout.addWidget(QLabel("Username / Email"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("e.g. hello@example.com")
        self.username_input.setFixedHeight(42)
        layout.addWidget(self.username_input)

        layout.addWidget(QLabel("Password"))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("••••••••")
        self.password_input.setFixedHeight(42)
        layout.addWidget(self.password_input)

        layout.addWidget(QLabel("Category"))
        self.category_box = QComboBox()
        self.category_box.setFixedHeight(42)
        
        # Kategorileri Ekle
        if self.categories:
            for cat_id, cat_name in self.categories:
                self.category_box.addItem(cat_name, cat_id)
        
        layout.addWidget(self.category_box)

        layout.addWidget(QLabel("Notes (Optional)"))
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Additional details...")
        self.notes_input.setFixedHeight(80)
        layout.addWidget(self.notes_input)

        layout.addStretch()

    def get_data(self):
        return {
            "site": self.site_input.text().strip(),
            "username": self.username_input.text().strip(),
            "password": self.password_input.text(),
            "category_id": self.category_box.currentData(),
            "notes": self.notes_input.toPlainText().strip()
        }