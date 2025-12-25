from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QLabel, QGridLayout, QGroupBox, QVBoxLayout,
    QFrame, QGraphicsDropShadowEffect, QSizePolicy
)
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ADAS Monitoring")

        central = QWidget()
        self.setCentralWidget(central)
        central.setStyleSheet("background:#0b0f12;")

        grid = QGridLayout(central)
        grid.setContentsMargins(16, 16, 16, 16)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(12)

        title = QLabel("ADAS Monitoring Console")
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        title.setStyleSheet("font-size: 18px; font-weight: 700; color:#cbd5e1;")

        # Sidebar (Indicators)
        sidebar = QGroupBox("Indicators")
        sidebar.setStyleSheet("""
        QGroupBox {
            color:#cbd5e1; font-weight:600; border:none;
            margin-top:8px;
        }
        """)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(8, 8, 8, 8)
        sidebar_layout.setSpacing(12)

        title_line = QFrame()
        title_line.setFrameShape(QFrame.HLine)
        title_line.setStyleSheet("color:#2a2e33;")

        sidebar_layout.addWidget(title_line)
        sidebar_layout.addWidget(self.make_indicator_card("Lamp", "💡"))
        sidebar_layout.addWidget(self.make_indicator_card("Speaker", "🔊"))
        sidebar_layout.addWidget(self.make_indicator_card("Buzzer", "🔔"))
        sidebar_layout.addStretch(1)
        sidebar.setMinimumWidth(220)

        # Videos
        video = QLabel("VIDEO AREA 1")
        video.setAlignment(Qt.AlignCenter)
        video.setStyleSheet("background:#222; color:#ddd; border-radius: 10px; padding:10px;")

        video2 = QLabel("VIDEO AREA 2")
        video2.setAlignment(Qt.AlignCenter)
        video2.setStyleSheet("background:#222; color:#ddd; border-radius: 10px; padding:10px;")

        video3 = QLabel("VIDEO AREA 3")
        video3.setAlignment(Qt.AlignCenter)
        video3.setStyleSheet("background:#222; color:#ddd; border-radius: 10px; padding:10px;")

        # Grid placement
        grid.addWidget(title,    0, 0, 1, 3)
        grid.addWidget(sidebar,  1, 0, 4, 1)
        grid.addWidget(video,    1, 1, 2, 1)
        grid.addWidget(video2,   1, 2, 2, 1)
        grid.addWidget(video3,   3, 1, 2, 2)

        # Proportions
        grid.setColumnStretch(0, 1)  # sidebar
        grid.setColumnStretch(1, 2)  # main
        grid.setColumnStretch(2, 2)  # main
        grid.setRowStretch(1, 1)
        grid.setRowStretch(2, 1)
        grid.setRowStretch(3, 1)
        grid.setRowStretch(4, 1)

        self.showMaximized()

    def make_indicator_card(self, name, emoji):
        card = QFrame()
        card.setObjectName("indicatorCard")
        card.setStyleSheet("""
        QFrame#indicatorCard {
            background-color: #0b0f12;
            border: 2px solid #00e6ff;
            border-radius: 18px;
        }
        """)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        card.setMinimumHeight(90)

        v = QVBoxLayout(card)
        v.setContentsMargins(12, 12, 12, 12)
        v.setSpacing(6)

        icon = QLabel(emoji)
        icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet("color:#00e6ff; font-size:22px;")

        text = QLabel(name)
        text.setAlignment(Qt.AlignCenter)
        text.setStyleSheet("color:#c8faff; font-weight:600;")

        v.addWidget(icon)
        v.addWidget(text)

        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(24)
        glow.setOffset(0, 0)
        glow.setColor(QColor("#00e6ff"))
        card.setGraphicsEffect(glow)

        return card


app = QApplication([])
w = MainWindow()
app.exec()
