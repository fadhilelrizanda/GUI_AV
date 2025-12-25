from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QLabel, QPushButton, QPlainTextEdit,
    QGridLayout, QGroupBox, QVBoxLayout, QHBoxLayout
)
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ADAS Monitoring (Grid)")

        central = QWidget()
        self.setCentralWidget(central)

        grid = QGridLayout(central)
        grid.setContentsMargins(16, 16, 16, 16)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(12)

        # --- Widgets ---
        title = QLabel("ADAS Monitoring Console")
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        title.setStyleSheet("font-size: 18px; font-weight: 700;")

        # Indicator
        sidebar = QGroupBox("Indicator")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.addWidget(log_box)
        sidebar_layout.addStretch(1)
        sidebar.setMinimumWidth(260)  # tweak to taste
        
        video = QLabel("VIDEO AREA 1")
        video.setAlignment(Qt.AlignCenter)
        video.setStyleSheet("background:#222; color:#ddd; border-radius: 10px; padding:10px;")
        # video.setMinimumHeight(400)
        
        video2 = QLabel("VIDEO AREA 2")
        video2.setAlignment(Qt.AlignCenter)
        video2.setStyleSheet("background:#222; color:#ddd; border-radius: 10px; padding:10px;")
        # video2.setMinimumHeight(400)
        
        video3 = QLabel("VIDEO AREA 3")
        video3.setAlignment(Qt.AlignCenter)
        video3.setStyleSheet("background:#222; color:#ddd; border-radius: 10px; padding:10px;")
        # video3.setMinimumHeight(400)

        status_box = QGroupBox("Status")
        status_layout = QVBoxLayout(status_box)
        status_layout.addWidget(QLabel("Speed: 0 km/h"))
        status_layout.addWidget(QLabel("FCW: OFF"))
        status_layout.addWidget(QLabel("AEB: OFF"))
        status_layout.addWidget(QLabel("LDW: OFF"))
        status_layout.addWidget(QLabel("DMS: OK"))
        status_layout.addStretch(1)

        log_box = QGroupBox("Event Log")
        log_layout = QVBoxLayout(log_box)
        log = QPlainTextEdit()
        log.setReadOnly(True)
        log.setPlainText("[INFO] System ready.")
        log_layout.addWidget(log)

        btn_start = QPushButton("Start")
        btn_stop = QPushButton("Stop")
        btn_exit = QPushButton("Exit")
        btn_exit.clicked.connect(self.close)

        controls = QHBoxLayout()
        controls.addWidget(btn_start)
        controls.addWidget(btn_stop)
        controls.addStretch(1)
        controls.addWidget(btn_exit)

        # --- Place into grid ---
        # (widget, row, col, rowSpan, colSpan)
        grid.addWidget(title,    0, 0, 1, 3)          # span sidebar + content
        grid.addWidget(sidebar,  1, 0, 4, 1)          # left sidebar
        grid.addWidget(video,    1, 1, 2, 1)          # top-left video
        grid.addWidget(video2,   1, 2, 2, 1)          # top-right video
        grid.addWidget(video3,   3, 1, 1, 2, Qt.AlignHCenter)  # centered under videos
        # grid.addLayout(controls, 4, 1, 1, 2)        # optional controls row

        # Proportions
        grid.setColumnStretch(0, 1)   # sidebar
        grid.setColumnStretch(1, 2)   # main
        grid.setColumnStretch(2, 2)   # main
        grid.setRowStretch(1, 1)
        grid.setRowStretch(2, 1)
        grid.setRowStretch(3, 1)

        self.showMaximized()


app = QApplication([])
w = MainWindow()
app.exec()
