from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal

class CategoryCard(QFrame):
    clicked = pyqtSignal(int)

    def __init__(self, category_id: int, name: str, count: int = 0):
        super().__init__()
        self.category_id = category_id
        self.name = name
        self.count = count
        self.is_active = False
        self._build()

    def _build(self):
        self.setFixedHeight(48)
        self.setCursor(Qt.PointingHandCursor)
        
        # Layout ve Widgetları ÖNCE oluşturuyoruz
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 15, 0)
        layout.setSpacing(10)

        # İsim
        self.name_label = QLabel(self.name)
        self.name_label.setStyleSheet("background: transparent; border: none; font-weight: 600; font-size: 14px;")

        # Sayı Badge
        self.count_label = QLabel(str(self.count))
        self.count_label.setAlignment(Qt.AlignCenter)
        self.count_label.setFixedSize(24, 24)
        
        layout.addWidget(self.name_label)
        layout.addStretch()
        layout.addWidget(self.count_label)

        # Stili EN SON uyguluyoruz (Artık count_label var olduğu için hata vermez)
        self.update_style()

    def set_active(self, active: bool):
        self.is_active = active
        self.update_style()

    def update_style(self):
        if self.is_active:
            # Seçili: Arka plan hafif açık, yazı beyaz, badge mavi
            bg = "rgba(255, 255, 255, 0.1)"
            text_color = "white"
            badge_bg = "#60A5FA" # Parlak mavi
            badge_text = "white"
            border = "border-left: 4px solid #60A5FA;" # Sol taraf çizgisi
        else:
            # Normal: Şeffaf
            bg = "transparent"
            text_color = "#9CA3AF" # Gri
            badge_bg = "#374151" # Koyu gri
            badge_text = "#D1D5DB"
            border = "border: none;"

        self.setStyleSheet(f"""
            QFrame {{
                background-color: {bg};
                border-radius: 6px;
                {border}
            }}
            QFrame:hover {{
                background-color: rgba(255, 255, 255, 0.05);
            }}
            QLabel {{
                color: {text_color};
                border: none;
                background: transparent; /* Label arka planı şeffaf olsun */
            }}
        """)
        
        # Badge stili özel olarak set edilmeli
        self.count_label.setStyleSheet(f"""
            background-color: {badge_bg};
            color: {badge_text};
            border-radius: 12px;
            font-size: 11px;
            font-weight: bold;
            border: none;
        """)

    def mousePressEvent(self, event):
        self.clicked.emit(self.category_id)