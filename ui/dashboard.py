from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QLineEdit,
    QFrame, QScrollArea, QApplication,
    QSizePolicy, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, pyqtSignal
from ui.category_card import CategoryCard

class Dashboard(QWidget):
    add_account_clicked = pyqtSignal()
    search_changed = pyqtSignal(str)
    category_selected = pyqtSignal(int)
    delete_account_requested = pyqtSignal(int)
    copy_password_requested = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("LockLock Dashboard")
        self.resize(1200, 800)
        self.setStyleSheet("""
            QWidget {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            }
            /* Global Scrollbar Stili */
            QScrollBar:vertical {
                border: none;
                background: #F3F4F6;
                width: 10px;
                margin: 0px 0px 0px 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #CBD5E1;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #94A3B8;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        self.category_widgets = []
        self._build_ui()

    def _build_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ================= SIDEBAR =================
        sidebar = QFrame()
        sidebar.setFixedWidth(280)
        sidebar.setStyleSheet("background-color: #111827;") # Çok koyu lacivert/siyah
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 40, 20, 30)
        sidebar_layout.setSpacing(10)

        # Logo Alanı
        logo_layout = QHBoxLayout()
        logo_icon = QLabel("🔒") # Basit ikon (resim yerine)
        logo_icon.setStyleSheet("font-size: 24px;")
        logo_text = QLabel("LockLock")
        logo_text.setStyleSheet("color: white; font-size: 22px; font-weight: 800; letter-spacing: 0.5px;")
        
        logo_layout.addWidget(logo_icon)
        logo_layout.addWidget(logo_text)
        logo_layout.addStretch()
        
        sidebar_layout.addLayout(logo_layout)
        sidebar_layout.addSpacing(30) # Logo ile liste arası boşluk

        # Kategori Başlığı
        cat_label = QLabel("VAULTS")
        cat_label.setStyleSheet("color: #6B7280; font-size: 11px; font-weight: 700; letter-spacing: 1px;")
        sidebar_layout.addWidget(cat_label)

        # Scroll Area (Kategoriler için)
        cat_scroll = QScrollArea()
        cat_scroll.setWidgetResizable(True)
        cat_scroll.setFrameShape(QFrame.NoFrame)
        cat_scroll.setStyleSheet("background: transparent; border: none;")
        
        self.cat_container = QWidget()
        self.cat_container.setStyleSheet("background: transparent;")
        self.cat_layout = QVBoxLayout(self.cat_container)
        self.cat_layout.setContentsMargins(0, 0, 0, 0)
        self.cat_layout.setSpacing(8)
        self.cat_layout.addStretch()

        cat_scroll.setWidget(self.cat_container)
        sidebar_layout.addWidget(cat_scroll)
        
        # Alt Bilgi
        version = QLabel("v1.0.0 • Secured")
        version.setStyleSheet("color: #4B5563; font-size: 12px; font-weight: 500;")
        version.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(version)

        # ================= CONTENT =================
        content = QFrame()
        content.setStyleSheet("background-color: #F3F4F6;") # Açık Gri
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(50, 50, 50, 50)
        content_layout.setSpacing(25)

        # --- Header ---
        header = QHBoxLayout()
        
        # Search
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search accounts...")
        self.search_input.setFixedHeight(50)
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
                padding: 0 20px;
                font-size: 15px;
                color: #1E293B;
                selection-background-color: #4F46E5;
            }
            QLineEdit:focus {
                border: 2px solid #4F46E5;
            }
        """)
        self.search_input.textChanged.connect(self.search_changed.emit)

        # Add Button
        self.add_btn = QPushButton("  +  New Account  ")
        self.add_btn.setFixedHeight(50)
        self.add_btn.setCursor(Qt.PointingHandCursor)
        self.add_btn.clicked.connect(self.add_account_clicked.emit)
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #4F46E5;
                color: white;
                border-radius: 12px;
                font-weight: 700;
                font-size: 14px;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #4338CA;
            }
        """)

        header.addWidget(self.search_input)
        header.addSpacing(20)
        header.addWidget(self.add_btn)

        # --- List Area ---
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setStyleSheet("background: transparent; border: none;")

        self.cards_container = QWidget()
        self.cards_container.setStyleSheet("background: transparent;")
        self.cards_layout = QVBoxLayout(self.cards_container)
        self.cards_layout.setSpacing(15)
        self.cards_layout.setContentsMargins(0, 0, 15, 0) # Sağdan boşluk (Scrollbar için)
        self.cards_layout.addStretch()

        self.scroll_area.setWidget(self.cards_container)

        content_layout.addLayout(header)
        content_layout.addWidget(self.scroll_area)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)

    def update_categories(self, categories: list, total_count: int):
        while self.cat_layout.count():
            item = self.cat_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        self.category_widgets = []

        all_card = CategoryCard(0, "All Accounts", total_count)
        all_card.clicked.connect(self.handle_category_click)
        all_card.set_active(True)
        self.cat_layout.addWidget(all_card)
        self.category_widgets.append(all_card)

        for cat in categories:
            count = getattr(cat, 'count', 0) 
            card = CategoryCard(cat.id, cat.name, count) 
            card.clicked.connect(self.handle_category_click)
            self.cat_layout.addWidget(card)
            self.category_widgets.append(card)

        self.cat_layout.addStretch()

    def update_account_list(self, accounts: list):
        while self.cards_layout.count() > 1:
            item = self.cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not accounts:
            lbl = QLabel("No accounts found.")
            lbl.setStyleSheet("color: #9CA3AF; font-size: 16px; margin-top: 30px; font-weight: 500;")
            lbl.setAlignment(Qt.AlignCenter)
            self.cards_layout.insertWidget(0, lbl)
            return

        for acc in accounts:
            card = self._create_account_card(acc)
            self.cards_layout.insertWidget(self.cards_layout.count() - 1, card)

    def _create_account_card(self, account):
        card = QFrame()
        card.setFixedHeight(90)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E2E8F0;
                border-radius: 16px;
            }
            QFrame:hover {
                border: 1px solid #4F46E5;
                background-color: #F8FAFC;
            }
        """)

        layout = QHBoxLayout(card)
        layout.setContentsMargins(25, 0, 25, 0)
        layout.setSpacing(20)

        # Sol taraf: İkon ve Bilgiler
        icon_lbl = QLabel(account.site[0].upper() if account.site else "?")
        icon_lbl.setFixedSize(45, 45)
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setStyleSheet("""
            background-color: #EEF2FF;
            color: #4F46E5;
            font-size: 20px;
            font-weight: 800;
            border-radius: 22px;
            border: none;
        """)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        info_layout.setAlignment(Qt.AlignVCenter)
        
        site_lbl = QLabel(account.site)
        site_lbl.setStyleSheet("border: none; background: transparent; font-size: 17px; font-weight: 700; color: #1E293B;")
        
        user_lbl = QLabel(account.username)
        user_lbl.setStyleSheet("border: none; background: transparent; font-size: 14px; font-weight: 500; color: #64748B;")

        info_layout.addWidget(site_lbl)
        info_layout.addWidget(user_lbl)

        # Sağ taraf: Butonlar
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        copy_btn = QPushButton("Copy Password")
        copy_btn.setFixedSize(120, 36)
        copy_btn.setCursor(Qt.PointingHandCursor)
        copy_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #4F46E5;
                border: 1px solid #E0E7FF;
                border-radius: 8px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #EEF2FF;
                border: 1px solid #C7D2FE;
            }
        """)
        copy_btn.clicked.connect(lambda: self.copy_password_requested.emit(account.encrypted_password))

        del_btn = QPushButton("Delete")
        del_btn.setFixedSize(80, 36)
        del_btn.setCursor(Qt.PointingHandCursor)
        del_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #EF4444;
                border: 1px solid #FEE2E2;
                border-radius: 8px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #FEF2F2;
                border: 1px solid #FECACA;
            }
        """)
        del_btn.clicked.connect(lambda: self.delete_account_requested.emit(account.id))

        btn_layout.addWidget(copy_btn)
        btn_layout.addWidget(del_btn)

        layout.addWidget(icon_lbl)
        layout.addLayout(info_layout)
        layout.addStretch()
        layout.addLayout(btn_layout)

        return card

    def handle_category_click(self, cat_id):
        for widget in self.category_widgets:
            widget.set_active(widget.category_id == cat_id)
        self.category_selected.emit(cat_id)