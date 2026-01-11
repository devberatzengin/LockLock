from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal

class CategoryCard(QFrame):
    clicked = pyqtSignal(int)  # Kategori ID'sini döner

    def __init__(self, category_id: int, name: str, count: int = 0):
        super().__init__()
        self.category_id = category_id
        self.name = name
        self.count = count
        self.is_active = False
        self._build()

    def _build(self):
        self.setFixedHeight(50)
        self.setCursor(Qt.PointingHandCursor)
        self.update_style()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)

        # Kategori İsmi
        self.name_label = QLabel(self.name)
        self.name_label.setStyleSheet("background: transparent; border: none; font-weight: 500;")

        # Sayı Badge'i
        self.count_label = QLabel(str(self.count))
        self.count_label.setAlignment(Qt.AlignCenter)
        self.count_label.setFixedSize(26, 26)
        self.count_label.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            border-radius: 13px;
            font-size: 12px;
            font-weight: bold;
        """)

        layout.addWidget(self.name_label)
        layout.addStretch()
        layout.addWidget(self.count_label)

    def set_active(self, active: bool):
        self.is_active = active
        self.update_style()

    def update_style(self):
        if self.is_active:
            # Seçili Durum
            bg = "#3B82F6" # Parlak Mavi
            text_color = "white"
            border = "1px solid #3B82F6"
        else:
            # Normal Durum
            bg = "#374151" # Koyu Gri
            text_color = "#E5E7EB" # Açık Gri
            border = "1px solid transparent"

        self.setStyleSheet(f"""
            QFrame {{
                background-color: {bg};
                border-radius: 10px;
                border: {border};
            }}
            QFrame:hover {{
                background-color: #4B5563; /* Hover rengi */
                border: 1px solid #6B7280;
            }}
            QLabel {{
                color: {text_color};
                background: transparent;
                border: none;
            }}
        """)
        
        # Seçiliyse hover rengini bozma
        if self.is_active:
             self.setStyleSheet(f"""
                QFrame {{
                    background-color: {bg};
                    border-radius: 10px;
                }}
                QLabel {{ color: white; background: transparent; }}
             """)

    def mousePressEvent(self, event):
        self.clicked.emit(self.category_id)