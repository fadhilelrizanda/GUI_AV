"""
ADAS Monitoring System
A real-time monitoring application for Advanced Driver Assistance Systems
"""

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QGridLayout, 
    QGroupBox, QVBoxLayout, QFrame, QGraphicsDropShadowEffect, 
    QSizePolicy, QSplitter, QHBoxLayout, QPushButton
)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl, Qt, QTimer
from PySide6.QtGui import QColor
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtSvg import QSvgRenderer
import random
import os
import re


class StyleConstants:
    """Centralized style constants for consistent theming"""
    # Colors
    BG_DARK = "#0b0f12"
    BG_CARD = "#1a1e23"
    BG_FRAME = "#121418"
    BORDER_DARK = "#2a3541"
    BORDER_LIGHT = "#3a3e43"
    
    CYAN_BRIGHT = "#00e6ff"
    CYAN_LIGHT = "#c8faff"
    BLUE_PRIMARY = "#0ea5e9"
    BLUE_DARK = "#0284c7"
    
    GRAY_LIGHT = "#cbd5e1"
    GRAY_MED = "#94a3b8"
    GRAY_DARK = "#555a61"
    GRAY_DARKER = "#3a3e43"
    
    # Dimensions
    SIDEBAR_WIDTH = 150
    INDICATOR_HEIGHT = 90
    VIDEO_HEADER_HEIGHT = 36
    SEPARATOR_WIDTH = 1


class MainWindow(QMainWindow):
    """Main application window for ADAS Monitoring System"""
    
    def __init__(self):
        super().__init__()
        self._setup_window()
        self._create_ui()
        self._start_indicator_timer()
        
    def _setup_window(self):
        """Initialize window properties"""
        self.setWindowTitle("ADAS Monitoring System")
        central = QWidget()
        self.setCentralWidget(central)
        central.setStyleSheet(f"background:{StyleConstants.BG_DARK};")
        
        self.grid = QGridLayout(central)
        self.grid.setContentsMargins(16, 16, 16, 16)
        self.grid.setHorizontalSpacing(12)
        self.grid.setVerticalSpacing(12)
        
    def _create_ui(self):
        """Create all UI components"""
        self._create_title()
        self._create_sidebar()
        self._create_video_area()
        self._create_separator()
        self._layout_components()
        
    def _create_title(self):
        """Create application title bar"""
        self.title = QLabel("ADAS Monitoring System")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet(f"""
            background: {StyleConstants.BG_CARD};
            color: {StyleConstants.GRAY_LIGHT};
            font-size: 18px;
            font-weight: 700;
            padding: 12px 24px;
            border-radius: 8px;
            border: 1px solid {StyleConstants.BORDER_DARK};
        """)
        
    def _create_sidebar(self):
        """Create indicator sidebar"""
        self.sidebar = QGroupBox("Indicators")
        self.sidebar.setStyleSheet(f"""
            QGroupBox {{
                color:{StyleConstants.GRAY_LIGHT}; 
                font-weight:600; 
                border:none;
                margin-top:8px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 0px;
            }}
        """)
        
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(8, 8, 8, 8)
        sidebar_layout.setSpacing(12)
        
        # Create indicator cards
        self.lamp_card = self._make_indicator_card("Lamp", "./icons/lamp.svg")
        self.speaker_card = self._make_indicator_card("Speaker", "./icons/speaker.svg")
        self.buzzer_card = self._make_indicator_card("Buzzer", "./icons/buzzer.svg")
        
        sidebar_layout.insertStretch(0, 1)
        sidebar_layout.addWidget(self.lamp_card)
        sidebar_layout.addWidget(self.speaker_card)
        sidebar_layout.addWidget(self.buzzer_card)
        sidebar_layout.addStretch(1)
        
        self.sidebar.setFixedWidth(StyleConstants.SIDEBAR_WIDTH)
        self.sidebar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        
    def _create_video_area(self):
        """Create video display area with toggle controls"""
        # Create video cards
        self.video1 = self._make_video_card("Camera View", "./videos/Camera.mp4")
        self.video2 = self._make_video_card("Bird's Eyes View", "./videos/BEV.mp4")
        self.video3 = self._make_video_card("Driving Monitoring System", "./videos/DMS.mp4")
        
        # Right splitter (video2 + video3 vertical)
        self.right_split = QSplitter(Qt.Vertical)
        self.right_split.setHandleWidth(6)
        self.right_split.setChildrenCollapsible(True)
        self.right_split.addWidget(self.video2)
        self.right_split.addWidget(self.video3)
        self.right_split.setStretchFactor(0, 1)
        self.right_split.setStretchFactor(1, 1)
        
        # Main content splitter
        self.content_split = QSplitter(Qt.Horizontal)
        self.content_split.setHandleWidth(6)
        self.content_split.setChildrenCollapsible(True)
        self.content_split.addWidget(self.video1)
        self.content_split.addWidget(self.right_split)
        self.content_split.setStretchFactor(0, 2)
        self.content_split.setStretchFactor(1, 1)
        
        # Toggle controls
        control_bar = self._create_control_bar()
        
        # Container
        self.content_container = QWidget()
        cc = QVBoxLayout(self.content_container)
        cc.setContentsMargins(0, 0, 0, 0)
        cc.setSpacing(6)
        cc.addWidget(control_bar)
        cc.addWidget(self.content_split)
        cc.setStretch(0, 0)
        cc.setStretch(1, 1)
        
    def _create_control_bar(self):
        """Create video toggle control bar"""
        control_bar = QFrame()
        control_bar.setStyleSheet("background: transparent;")
        cb = QHBoxLayout(control_bar)
        cb.setContentsMargins(0, 0, 0, 8)
        cb.setSpacing(8)
        
        self.btn_v1 = self._make_toggle_button("Camera View")
        self.btn_v2 = self._make_toggle_button("Radar View")
        self.btn_v3 = self._make_toggle_button("DMS")
        
        cb.addStretch(1)
        cb.addWidget(self.btn_v1)
        cb.addWidget(self.btn_v2)
        cb.addWidget(self.btn_v3)
        
        # Wire signals
        self.btn_v1.toggled.connect(self._update_video_visibility)
        self.btn_v2.toggled.connect(self._update_video_visibility)
        self.btn_v3.toggled.connect(self._update_video_visibility)
        
        return control_bar
        
    def _create_separator(self):
        """Create vertical separator line"""
        self.separator_container = QWidget()
        separator_layout = QVBoxLayout(self.separator_container)
        separator_layout.setContentsMargins(0, 0, 0, 0)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setStyleSheet(f"""
            QFrame {{
                background-color: {StyleConstants.BORDER_LIGHT};
                max-width: {StyleConstants.SEPARATOR_WIDTH}px;
                min-width: {StyleConstants.SEPARATOR_WIDTH}px;
            }}
        """)
        
        separator_layout.addStretch(2)
        separator_layout.addWidget(separator, 95)
        separator_layout.addStretch(2)
        
    def _layout_components(self):
        """Arrange all components in grid layout"""
        self.grid.addWidget(self.title, 0, 0, 1, 4)
        self.grid.addWidget(self.sidebar, 1, 0, 4, 1)
        self.grid.addWidget(self.separator_container, 1, 1, 4, 1)
        self.grid.addWidget(self.content_container, 1, 2, 4, 2)
        
        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(1, 0)
        self.grid.setColumnStretch(2, 2)
        self.grid.setColumnStretch(3, 2)
        self.grid.setRowStretch(1, 1)
        self.grid.setRowStretch(2, 1)
        self.grid.setRowStretch(3, 1)
        self.grid.setRowStretch(4, 1)
        
        self._update_video_visibility()
        self.showMaximized()
        
    def _make_indicator_card(self, name: str, svg_path: str) -> QFrame:
        """Create an indicator card with icon and label"""
        card = QFrame()
        card.setObjectName("indicatorCard")
        card.setStyleSheet(f"""
            QFrame#indicatorCard {{
                background-color: {StyleConstants.BG_DARK};
                border: 4px solid {StyleConstants.CYAN_BRIGHT};
                border-radius: 18px;
            }}
        """)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        card.setMinimumHeight(StyleConstants.INDICATOR_HEIGHT)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(6)
        
        # Icon circle
        circle = self._create_icon_circle(svg_path)
        icon_container = QWidget()
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.addWidget(circle, 0, Qt.AlignCenter)
        
        # Label
        text = QLabel(name)
        text.setAlignment(Qt.AlignCenter)
        text.setStyleSheet(f"color:{StyleConstants.CYAN_LIGHT}; font-weight:600;")
        
        layout.addWidget(icon_container)
        layout.addWidget(text)
        
        # Glow effect
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(24)
        glow.setOffset(0, 0)
        glow.setColor(QColor(StyleConstants.CYAN_BRIGHT))
        card.setGraphicsEffect(glow)
        
        # Store references
        card.is_on = True
        card.icon_widget = circle.icon_widget
        card.circle_frame = circle
        card.text_label = text
        card.glow_effect = glow
        
        return card
        
    def _create_icon_circle(self, svg_path: str) -> QFrame:
        """Create circular frame with SVG icon"""
        circle = QFrame()
        circle.setObjectName("iconCircle")
        circle.setFixedSize(50, 50)
        circle.setStyleSheet(f"""
            QFrame#iconCircle {{
                background: transparent;
                border: 3px solid {StyleConstants.CYAN_BRIGHT};
                border-radius: 25px;
            }}
        """)
        
        icon = QSvgWidget(svg_path)
        icon.setFixedSize(30, 30)
        icon.setStyleSheet("background: transparent;")
        icon.original_svg_path = svg_path
        
        circle_layout = QVBoxLayout(circle)
        circle_layout.setContentsMargins(0, 0, 0, 0)
        circle_layout.addWidget(icon, 0, Qt.AlignCenter)
        
        circle.icon_widget = icon
        return circle
        
    def _make_video_card(self, title: str, video_path: str = None) -> QFrame:
        """Create a video display card"""
        card = QFrame()
        card.setObjectName("videoCard")
        card.setStyleSheet("QFrame#videoCard { background: transparent; border: none; }")
        card.setMinimumHeight(120)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = self._create_video_header(title)
        
        # Video body
        body = self._create_video_body(video_path, card)
        
        layout.addWidget(header)
        layout.addSpacing(8)
        layout.addWidget(body)
        layout.setStretch(0, 0)
        layout.setStretch(2, 1)
        
        return card
        
    def _create_video_header(self, title: str) -> QFrame:
        """Create video card header"""
        header = QFrame()
        header.setObjectName("videoHeader")
        header.setStyleSheet(f"""
            QFrame#videoHeader {{
                background: {StyleConstants.BLUE_PRIMARY};
                border: 1px solid {StyleConstants.BLUE_DARK};
                border-radius: 6px;
            }}
            QLabel {{
                color: #ffffff;
                font-weight: 600;
                font-size: 13px;
                background: transparent;
            }}
        """)
        header.setFixedHeight(StyleConstants.VIDEO_HEADER_HEIGHT)
        
        h_layout = QVBoxLayout(header)
        h_layout.setContentsMargins(16, 8, 16, 8)
        h_layout.setSpacing(0)
        
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        h_layout.addWidget(title_label)
        
        return header
        
    def _create_video_body(self, video_path: str, card: QFrame) -> QFrame:
        """Create video display body"""
        body = QFrame()
        body.setObjectName("videoBody")
        body.setStyleSheet("""
            QFrame#videoBody {
                background:#000000;
                border-radius:10px;
            }
        """)
        
        layout = QVBoxLayout(body)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        if video_path and os.path.exists(video_path):
            video_widget = self._create_video_player(video_path, card)
            layout.addWidget(video_widget)
        else:
            placeholder = QLabel("No video source")
            placeholder.setAlignment(Qt.AlignCenter)
            placeholder.setStyleSheet(f"color:{StyleConstants.GRAY_MED};")
            layout.addWidget(placeholder)
            
        return body
        
    def _create_video_player(self, video_path: str, card: QFrame) -> QVideoWidget:
        """Create and configure video player"""
        video_widget = QVideoWidget()
        video_widget.setStyleSheet("background:#000000;")
        
        player = QMediaPlayer()
        audio_output = QAudioOutput()
        player.setAudioOutput(audio_output)
        player.setVideoOutput(video_widget)
        player.setSource(QUrl.fromLocalFile(video_path))
        player.setLoops(QMediaPlayer.Loops.Infinite)
        player.play()
        
        # Store references to prevent garbage collection
        card.player = player
        card.audio_output = audio_output
        
        return video_widget
        
    def _make_toggle_button(self, text: str) -> QPushButton:
        """Create a checkable toggle button"""
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setChecked(True)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: {StyleConstants.BG_CARD};
                color: {StyleConstants.GRAY_MED};
                border: 1px solid {StyleConstants.BORDER_DARK};
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 600;
                font-size: 13px;
            }}
            QPushButton:checked {{
                background: {StyleConstants.BLUE_PRIMARY};
                color: #ffffff;
                border: 1px solid {StyleConstants.BLUE_DARK};
            }}
            QPushButton:hover {{
                background: #253240;
            }}
            QPushButton:checked:hover {{
                background: {StyleConstants.BLUE_DARK};
            }}
            QPushButton:pressed {{
                background: #1e293b;
            }}
        """)
        return btn
        
    def _update_video_visibility(self):
        """Update video panel visibility based on toggle states"""
        v1 = self.btn_v1.isChecked()
        v2 = self.btn_v2.isChecked()
        v3 = self.btn_v3.isChecked()
        
        self.video1.setVisible(v1)
        self.video2.setVisible(v2)
        self.video3.setVisible(v3)
        self.right_split.setVisible(v2 or v3)
        
        # Adjust splitter sizes
        if v1 and (v2 or v3):
            self.content_split.setSizes([2, 1])
        elif v1:
            self.content_split.setSizes([1, 0])
        elif v2 or v3:
            self.content_split.setSizes([0, 1])
        else:
            self.content_split.setSizes([1, 1])
            
        if v2 and v3:
            self.right_split.setSizes([1, 1])
        elif v2:
            self.right_split.setSizes([1, 0])
        elif v3:
            self.right_split.setSizes([0, 1])
            
    def _set_indicator_state(self, card: QFrame, is_on: bool):
        """Update indicator visual state"""
        card.is_on = is_on
        color = StyleConstants.CYAN_BRIGHT if is_on else StyleConstants.GRAY_DARKER
        text_color = StyleConstants.CYAN_LIGHT if is_on else StyleConstants.GRAY_DARK
        blur = 24 if is_on else 0
        
        card.setStyleSheet(f"""
            QFrame#indicatorCard {{
                background-color: {StyleConstants.BG_DARK};
                border: 4px solid {color};
                border-radius: 18px;
            }}
        """)
        
        card.circle_frame.setStyleSheet(f"""
            QFrame#iconCircle {{
                background: transparent;
                border: 3px solid {color};
                border-radius: 25px;
            }}
        """)
        
        self._recolor_svg(card.icon_widget, color)
        card.text_label.setStyleSheet(f"color:{text_color}; font-weight:600;")
        card.glow_effect.setColor(QColor(color if is_on else "#1a1e23"))
        card.glow_effect.setBlurRadius(blur)
        
    def _recolor_svg(self, svg_widget: QSvgWidget, color: str):
        """Dynamically recolor SVG icon"""
        if not hasattr(svg_widget, 'original_svg_path'):
            return
            
        svg_path = svg_widget.original_svg_path
        if not os.path.exists(svg_path):
            return
            
        with open(svg_path, 'r') as f:
            svg_content = f.read()
            
        svg_content = re.sub(r'fill="[^"]*"', f'fill="{color}"', svg_content)
        svg_content = re.sub(r'stroke="[^"]*"', f'stroke="{color}"', svg_content)
        svg_widget.load(svg_content.encode())
        
    def _update_indicator_states(self):
        """Randomly update indicator states (simulated)"""
        self._set_indicator_state(self.lamp_card, bool(random.randint(0, 1)))
        self._set_indicator_state(self.speaker_card, bool(random.randint(0, 1)))
        self._set_indicator_state(self.buzzer_card, bool(random.randint(0, 1)))
        
    def _start_indicator_timer(self):
        """Start periodic indicator updates"""
        self.indicator_timer = QTimer()
        self.indicator_timer.timeout.connect(self._update_indicator_states)
        self.indicator_timer.start(1000)


def main():
    """Application entry point"""
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
