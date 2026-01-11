from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel,
    QHBoxLayout, QPushButton
)
from PyQt5.QtCore import Qt


class ConfirmDialog(QDialog):
    def __init__(self, title="Confirm", message="Are you sure?"):
        super().__init__()
        self.setWindowTitle(title)
        self.setFixedSize(360, 180)
        self._build(message)

    def _build(self, message):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(20)

        msg = QLabel(message)
        msg.setAlignment(Qt.AlignCenter)
        msg.setWordWrap(True)
        msg.setStyleSheet("font-size: 14px;")

        btns = QHBoxLayout()
        btns.setSpacing(10)

        cancel = QPushButton("Cancel")
        ok = QPushButton("Confirm")

        cancel.clicked.connect(self.reject)
        ok.clicked.connect(self.accept)

        btns.addStretch()
        btns.addWidget(cancel)
        btns.addWidget(ok)

        layout.addWidget(msg)
        layout.addLayout(btns)
