"""PySide6 configuration window for Cyclone."""
import sys
import time

from . import anti_afk, backend


def run_gui():
    try:
        from PySide6.QtCore import QTimer, Qt
        from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox,
            QFormLayout, QGridLayout, QHBoxLayout, QHeaderView, QLabel, QLineEdit, QListWidget,
            QListWidgetItem,
            QFrame, QMainWindow, QMessageBox, QPushButton, QSpinBox, QTableWidget, QTableWidgetItem,
            QTabWidget, QVBoxLayout, QWidget)
    except Exception as error:
        print("PySide6 not available or failed to start GUI:", error)
        print("Install requirements (see README.md) to run the GUI.")
        return

    themes = {
        "Oppression": """
            QMainWindow { background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #0b0c0e, stop: 0.55 #22262b, stop: 1 #8b9298); color: #f0f2f3; }
            QLabel#appTitle { color: #e2e5e7; font-size: 24px; font-weight: 700; }
            QLabel#appSubtitle, QLabel#cardTitle { color: #b8bec3; font-size: 12px; }
            QLabel#statusLabel { color: #e2e5e7; font-weight: 700; padding: 8px 12px; }
            QFrame#card { background: #1b1e22; border: 1px solid #555d64; border-radius: 8px; }
            QLabel#cardValue { color: #f0f2f3; font-size: 22px; font-weight: 700; }
            QLabel#cardDetail, QLabel#emptyState { color: #b8bec3; }
            QTabWidget::pane { border: 1px solid #555d64; background: #292e33; }
            QTabBar::tab { background: #1b1e22; border: 1px solid transparent; border-radius: 6px; margin: 4px 3px 0; padding: 9px 16px; color: #b8bec3; }
            QTabBar::tab:hover { background: #454c52; color: #ffffff; }
            QTabBar::tab:selected { background: #707980; color: #ffffff; border: 1px solid #b7bec3; }
            QListWidget, QTableWidget, QLineEdit, QComboBox { background: #111316; color: #f0f2f3; border: 1px solid #555d64; padding: 6px; }
            QPushButton { background: #626b72; color: white; border: 0; border-radius: 6px; padding: 8px 14px; }
            QPushButton:hover { background: #7f8991; }
            QPushButton:pressed { background: #464d53; }
            QPushButton:disabled { background: #41474c; color: #9ca3a8; }
            QHeaderView::section { background: #454c52; color: #edf0f2; padding: 6px; }
        """,
        "Dreammetric": """
            QMainWindow { background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #f2cbd8, stop: 0.55 #d99fb8, stop: 1 #52627f); color: #312b3b; }
            QLabel#appTitle { color: #fff5fa; font-size: 24px; font-weight: 700; }
            QLabel#appSubtitle, QLabel#cardTitle { color: #5e5068; font-size: 12px; }
            QLabel#statusLabel { color: #eef4ff; font-weight: 700; padding: 8px 12px; }
            QFrame#card { background: rgba(255, 240, 247, 225); border: 1px solid #c18aa5; border-radius: 8px; }
            QLabel#cardValue { color: #3e4261; font-size: 22px; font-weight: 700; }
            QLabel#cardDetail, QLabel#emptyState { color: #685b72; }
            QTabWidget::pane { border: 1px solid #a97898; background: rgba(247, 218, 231, 205); }
            QTabBar::tab { background: rgba(115, 86, 117, 190); border: 1px solid transparent; border-radius: 6px; margin: 4px 3px 0; padding: 9px 16px; color: #f8eaf1; }
            QTabBar::tab:hover { background: #536582; color: #ffffff; }
            QTabBar::tab:selected { background: #4f5f80; color: #ffffff; border: 1px solid #91a5c9; }
            QListWidget, QTableWidget, QLineEdit, QComboBox { background: #3e405d; color: #fff2f8; border: 1px solid #9b7b9a; padding: 6px; }
            QComboBox QAbstractItemView { background: #30344f; color: #fff2f8; selection-background-color: #536582; selection-color: #ffffff; }
            QPushButton { background: #52627f; color: white; border: 0; border-radius: 6px; padding: 8px 14px; }
            QPushButton:hover { background: #6d7fa2; }
            QPushButton:pressed { background: #3d4b68; }
            QPushButton:disabled { background: #9b9caf; color: #f1eaf0; }
            QHeaderView::section { background: #7b6684; color: #fff1f7; padding: 6px; }
        """,
        "Oblivion": """
            QMainWindow { background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #130d24, stop: 0.6 #302052, stop: 1 #81749a); color: #f4f0ff; }
            QLabel#appTitle { color: #eee7ff; font-size: 24px; font-weight: 700; }
            QLabel#appSubtitle, QLabel#cardTitle { color: #c3b9da; font-size: 12px; }
            QLabel#statusLabel { color: #f2edff; font-weight: 700; padding: 8px 12px; }
            QFrame#card { background: rgba(30, 21, 53, 225); border: 1px solid #655a80; border-radius: 8px; }
            QLabel#cardValue { color: #f7f3ff; font-size: 22px; font-weight: 700; }
            QLabel#cardDetail, QLabel#emptyState { color: #bdb2d3; }
            QTabWidget::pane { border: 1px solid #655a80; background: rgba(48, 35, 78, 220); }
            QTabBar::tab { background: rgba(38, 27, 65, 225); border: 1px solid transparent; border-radius: 6px; margin: 4px 3px 0; padding: 9px 16px; color: #c8bfdd; }
            QTabBar::tab:hover { background: #584b78; color: #ffffff; }
            QTabBar::tab:selected { background: #77669e; color: #ffffff; border: 1px solid #bdb2d3; }
            QListWidget, QTableWidget, QLineEdit, QComboBox { background: rgba(19, 14, 34, 235); color: #f4f0ff; border: 1px solid #655a80; padding: 6px; }
            QPushButton { background: #6d5a98; color: white; border: 0; border-radius: 6px; padding: 8px 14px; }
            QPushButton:hover { background: #8975bb; }
            QPushButton:pressed { background: #514375; }
            QPushButton:disabled { background: #514b62; color: #b9b1c9; }
            QHeaderView::section { background: #584b78; color: #f0eaff; padding: 6px; }
        """,
        "Obsidian": """
            QMainWindow { background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #101820, stop: 1 #17343a); color: #e8f0f2; }
            QLabel#appTitle { color: #7fe0c2; font-size: 24px; font-weight: 700; }
            QLabel#appSubtitle { color: #8da7ad; font-size: 12px; }
            QLabel#statusLabel { color: #7fe0c2; font-weight: 700; padding: 8px 12px; }
            QFrame#card { background: #141e24; border: 1px solid #2c4148; border-radius: 10px; }
            QLabel#cardTitle { color: #8da7ad; font-size: 11px; font-weight: 700; }
            QLabel#cardValue { color: #7fe0c2; font-size: 22px; font-weight: 700; }
            QLabel#cardDetail, QLabel#emptyState { color: #8da7ad; }
            QTabWidget::pane { border: 1px solid #2c4148; background: #14232a; }
            QTabBar::tab { background: #14242b; border: 1px solid transparent; border-radius: 6px; margin: 4px 3px 0; padding: 9px 16px; color: #9eb5bb; }
            QTabBar::tab:hover { background: #1b3439; color: #d8efeb; }
            QTabBar::tab:selected { background: #1d7467; color: #ffffff; border: 1px solid #2a9887; }
            QListWidget, QTableWidget, QLineEdit, QComboBox { background: #0d171c; color: #e8f0f2; border: 1px solid #2c4148; padding: 6px; }
            QPushButton { background: #1d7467; color: white; border: 0; border-radius: 6px; padding: 8px 14px; }
            QPushButton:hover { background: #2a9887; }
            QPushButton:pressed { background: #14594f; }
            QPushButton:disabled { background: #36504e; color: #9eb5bb; }
            QHeaderView::section { background: #1b3038; color: #cde0e3; padding: 6px; }
        """,
        "Slate": """
            QMainWindow { background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #20252b, stop: 1 #3a3025); color: #f1f4f5; }
            QLabel#appTitle { color: #f3c969; font-size: 24px; font-weight: 700; }
            QLabel#appSubtitle { color: #aeb8be; font-size: 12px; }
            QLabel#statusLabel { color: #f3c969; font-weight: 700; padding: 8px 12px; }
            QFrame#card { background: #292f35; border: 1px solid #48545d; border-radius: 10px; }
            QLabel#cardTitle { color: #aeb8be; font-size: 11px; font-weight: 700; }
            QLabel#cardValue { color: #f3c969; font-size: 22px; font-weight: 700; }
            QLabel#cardDetail, QLabel#emptyState { color: #aeb8be; }
            QTabWidget::pane { border: 1px solid #48545d; background: #2b3239; }
            QTabBar::tab { background: #292f35; border: 1px solid transparent; border-radius: 6px; margin: 4px 3px 0; padding: 9px 16px; color: #aeb8be; }
            QTabBar::tab:hover { background: #3a4248; color: #ffffff; }
            QTabBar::tab:selected { background: #b27925; color: #ffffff; border: 1px solid #d09632; }
            QListWidget, QTableWidget, QLineEdit, QComboBox { background: #1b2025; color: #f1f4f5; border: 1px solid #48545d; padding: 6px; }
            QPushButton { background: #b27925; color: white; border: 0; border-radius: 6px; padding: 8px 14px; }
            QPushButton:hover { background: #d09632; }
            QPushButton:pressed { background: #805317; }
            QPushButton:disabled { background: #5a5144; color: #aeb8be; }
            QHeaderView::section { background: #39434b; color: #e8edef; padding: 6px; }
        """,
        "Ember": """
            QMainWindow { background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #241b1b, stop: 1 #4a2b24); color: #fff3e8; }
            QLabel#appTitle { color: #ffb86b; font-size: 24px; font-weight: 700; }
            QLabel#appSubtitle, QLabel#cardTitle { color: #d5aaa0; font-size: 12px; }
            QLabel#statusLabel { color: #ffb86b; font-weight: 700; padding: 8px 12px; }
            QFrame#card { background: #302020; border: 1px solid #674039; border-radius: 8px; }
            QLabel#cardValue { color: #ffb86b; font-size: 22px; font-weight: 700; }
            QLabel#cardDetail, QLabel#emptyState { color: #d5aaa0; }
            QTabWidget::pane { border: 1px solid #674039; background: #382421; }
            QTabBar::tab { background: #302020; border: 1px solid transparent; border-radius: 6px; margin: 4px 3px 0; padding: 9px 16px; color: #d5aaa0; }
            QTabBar::tab:hover { background: #523029; color: #fff3e8; }
            QTabBar::tab:selected { background: #c65d3b; color: #ffffff; border: 1px solid #e0784f; }
            QListWidget, QTableWidget, QLineEdit, QComboBox { background: #211718; color: #fff3e8; border: 1px solid #674039; padding: 6px; }
            QPushButton { background: #c65d3b; color: white; border: 0; border-radius: 6px; padding: 8px 14px; }
            QPushButton:hover { background: #e0784f; }
            QPushButton:pressed { background: #95432b; }
            QPushButton:disabled { background: #63483f; color: #c6aaa2; }
            QHeaderView::section { background: #57332c; color: #ffe2d0; padding: 6px; }
        """,
        "Lagoon": """
            QMainWindow { background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #102a35, stop: 1 #1d4d55); color: #e9fbf7; }
            QLabel#appTitle { color: #78e0d0; font-size: 24px; font-weight: 700; }
            QLabel#appSubtitle, QLabel#cardTitle { color: #9bc8c8; font-size: 12px; }
            QLabel#statusLabel { color: #78e0d0; font-weight: 700; padding: 8px 12px; }
            QFrame#card { background: #173944; border: 1px solid #36717a; border-radius: 8px; }
            QLabel#cardValue { color: #78e0d0; font-size: 22px; font-weight: 700; }
            QLabel#cardDetail, QLabel#emptyState { color: #9bc8c8; }
            QTabWidget::pane { border: 1px solid #36717a; background: #19424a; }
            QTabBar::tab { background: #173944; border: 1px solid transparent; border-radius: 6px; margin: 4px 3px 0; padding: 9px 16px; color: #9bc8c8; }
            QTabBar::tab:hover { background: #255861; color: #e9fbf7; }
            QTabBar::tab:selected { background: #167d78; color: #ffffff; border: 1px solid #20a39a; }
            QListWidget, QTableWidget, QLineEdit, QComboBox { background: #0d252e; color: #e9fbf7; border: 1px solid #36717a; padding: 6px; }
            QPushButton { background: #167d78; color: white; border: 0; border-radius: 6px; padding: 8px 14px; }
            QPushButton:hover { background: #20a39a; }
            QPushButton:pressed { background: #105d5a; }
            QPushButton:disabled { background: #3a6668; color: #a8c4c2; }
            QHeaderView::section { background: #255861; color: #d8f5ef; padding: 6px; }
        """,
        "Deep Ocean": """
            QMainWindow { background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #091a24, stop: 1 #173b4a); color: #e4f4f5; }
            QLabel#appTitle { color: #73d0dc; font-size: 24px; font-weight: 700; }
            QLabel#appSubtitle, QLabel#cardTitle { color: #8eb7c0; font-size: 12px; }
            QLabel#statusLabel { color: #73d0dc; font-weight: 700; padding: 8px 12px; }
            QFrame#card { background: #102b37; border: 1px solid #2b5c6b; border-radius: 8px; }
            QLabel#cardValue { color: #73d0dc; font-size: 22px; font-weight: 700; }
            QLabel#cardDetail, QLabel#emptyState { color: #8eb7c0; }
            QTabWidget::pane { border: 1px solid #2b5c6b; background: #143440; }
            QTabBar::tab { background: #102b37; border: 1px solid transparent; border-radius: 6px; margin: 4px 3px 0; padding: 9px 16px; color: #8eb7c0; }
            QTabBar::tab:hover { background: #205264; color: #e4f4f5; }
            QTabBar::tab:selected { background: #267d88; color: #ffffff; border: 1px solid #4db3bd; }
            QListWidget, QTableWidget, QLineEdit, QComboBox { background: #0b202a; color: #e4f4f5; border: 1px solid #2b5c6b; padding: 6px; }
            QPushButton { background: #267d88; color: white; border: 0; border-radius: 6px; padding: 8px 14px; }
            QPushButton:hover { background: #389eaa; }
            QPushButton:pressed { background: #1b5d65; }
            QPushButton:disabled { background: #365963; color: #9bb9be; }
            QHeaderView::section { background: #205264; color: #d8f2f4; padding: 6px; }
        """,
        "Wine": """
            QMainWindow { background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #21151c, stop: 1 #42252e); color: #f7e9ed; }
            QLabel#appTitle { color: #e89aaf; font-size: 24px; font-weight: 700; }
            QLabel#appSubtitle, QLabel#cardTitle { color: #c59da9; font-size: 12px; }
            QLabel#statusLabel { color: #e89aaf; font-weight: 700; padding: 8px 12px; }
            QFrame#card { background: #2d1d25; border: 1px solid #65404e; border-radius: 8px; }
            QLabel#cardValue { color: #e89aaf; font-size: 22px; font-weight: 700; }
            QLabel#cardDetail, QLabel#emptyState { color: #c59da9; }
            QTabWidget::pane { border: 1px solid #65404e; background: #38232c; }
            QTabBar::tab { background: #2d1d25; border: 1px solid transparent; border-radius: 6px; margin: 4px 3px 0; padding: 9px 16px; color: #c59da9; }
            QTabBar::tab:hover { background: #583545; color: #f7e9ed; }
            QTabBar::tab:selected { background: #a64d68; color: #ffffff; border: 1px solid #d47791; }
            QListWidget, QTableWidget, QLineEdit, QComboBox { background: #21161c; color: #f7e9ed; border: 1px solid #65404e; padding: 6px; }
            QPushButton { background: #a64d68; color: white; border: 0; border-radius: 6px; padding: 8px 14px; }
            QPushButton:hover { background: #c66882; }
            QPushButton:pressed { background: #79384e; }
            QPushButton:disabled { background: #654453; color: #c3aab3; }
            QHeaderView::section { background: #583545; color: #f4dce3; padding: 6px; }
        """,
        "Graphite": """
            QMainWindow { background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #151719, stop: 1 #30363a); color: #edf0f1; }
            QLabel#appTitle { color: #a9d1d2; font-size: 24px; font-weight: 700; }
            QLabel#appSubtitle, QLabel#cardTitle { color: #a7afb2; font-size: 12px; }
            QLabel#statusLabel { color: #a9d1d2; font-weight: 700; padding: 8px 12px; }
            QFrame#card { background: #22272a; border: 1px solid #515b60; border-radius: 8px; }
            QLabel#cardValue { color: #a9d1d2; font-size: 22px; font-weight: 700; }
            QLabel#cardDetail, QLabel#emptyState { color: #a7afb2; }
            QTabWidget::pane { border: 1px solid #515b60; background: #2a3033; }
            QTabBar::tab { background: #22272a; border: 1px solid transparent; border-radius: 6px; margin: 4px 3px 0; padding: 9px 16px; color: #a7afb2; }
            QTabBar::tab:hover { background: #414a4f; color: #edf0f1; }
            QTabBar::tab:selected { background: #557b7e; color: #ffffff; border: 1px solid #7da7a9; }
            QListWidget, QTableWidget, QLineEdit, QComboBox { background: #181b1d; color: #edf0f1; border: 1px solid #515b60; padding: 6px; }
            QPushButton { background: #557b7e; color: white; border: 0; border-radius: 6px; padding: 8px 14px; }
            QPushButton:hover { background: #6b999b; }
            QPushButton:pressed { background: #3f5e61; }
            QPushButton:disabled { background: #465255; color: #aeb8ba; }
            QHeaderView::section { background: #414a4f; color: #e2eaeb; padding: 6px; }
        """,
    }

    class CycloneWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.config = backend.load_config()
            self.accounts = backend.load_accounts()
            self.biomes = backend.load_biomes()
            self.setWindowTitle(self.config.get("macro_name", "Cyclone"))
            self.resize(760, 540)
            self.setMinimumSize(700, 500)
            self.backend_running = backend.is_backend_running()
            self._apply_theme(self.config.get("theme", "Obsidian"))
            self._build_ui()

        def _apply_theme(self, name):
            self.setStyleSheet(themes.get(name, themes["Obsidian"]))

        def _build_ui(self):
            root = QWidget()
            root_layout = QVBoxLayout(root)
            root_layout.setContentsMargins(22, 20, 22, 20)
            root_layout.setSpacing(16)
            header = QHBoxLayout()
            title = QLabel("CYCLONE")
            title.setObjectName("appTitle")
            subtitle = QLabel("Sol's RNG Multi-Instance Tracker")
            subtitle.setObjectName("appSubtitle")
            title_block = QVBoxLayout()
            title_block.setSpacing(2)
            title_block.addWidget(title)
            title_block.addWidget(subtitle)
            header.addLayout(title_block)
            header.addStretch()
            self.status_label = QLabel()
            self.status_label.setObjectName("statusLabel")
            self.start_button = QPushButton("Start tracking")
            self.stop_button = QPushButton("Stop")
            self.start_button.clicked.connect(self._start_tracking)
            self.stop_button.clicked.connect(self._stop_tracking)
            header.addWidget(self.status_label)
            header.addWidget(self.start_button)
            header.addWidget(self.stop_button)
            root_layout.addLayout(header)
            tabs = QTabWidget()
            tabs.addTab(self._dashboard_tab(), "Dashboard")
            tabs.addTab(self._instances_tab(), "Instances")
            tabs.addTab(self._accounts_tab(), "Accounts")
            tabs.addTab(self._biomes_tab(), "Biomes")
            tabs.addTab(self._anti_afk_tab(), "Anti-AFK")
            tabs.addTab(self._settings_tab(), "Settings")
            root_layout.addWidget(tabs)
            footer = QLabel("Made by linchev | Version 1.0.0")
            footer.setObjectName("appSubtitle")
            footer.setAlignment(Qt.AlignmentFlag.AlignLeft)
            root_layout.addWidget(footer)
            self.setCentralWidget(root)
            self.dashboard_timer = QTimer(self)
            self.dashboard_timer.timeout.connect(self._refresh_dashboard)
            self.dashboard_timer.start(1000)
            self._update_tracking_controls()

        def _dashboard_tab(self):
            page = QWidget()
            layout = QVBoxLayout(page)
            layout.setContentsMargins(18, 18, 18, 18)
            layout.setSpacing(14)
            overview = QGridLayout()
            overview.setSpacing(12)
            self.dashboard_status = self._dashboard_card("TRACKING STATUS", "PAUSED", "")
            self.dashboard_time = self._dashboard_card("MACRO TIME", "00:00:00", "Session duration")
            self.dashboard_logs = self._dashboard_card("ACTIVE LOGS", "0", "Configured instances")
            self.dashboard_biomes = self._dashboard_card("WEBHOOKS", "0", "Configured destinations")
            self.dashboard_ram = self._dashboard_card("RAM TRIMMER", "READY", "Periodic Windows cleanup")
            overview.addWidget(self.dashboard_status, 0, 0)
            overview.addWidget(self.dashboard_time, 0, 1)
            overview.addWidget(self.dashboard_logs, 1, 0)
            overview.addWidget(self.dashboard_biomes, 1, 1)
            overview.addWidget(self.dashboard_ram, 2, 0, 1, 2)
            layout.addLayout(overview)
            activity = QFrame()
            activity.setObjectName("card")
            activity_layout = QVBoxLayout(activity)
            activity_title = QLabel("ACTIVE LOGS")
            activity_title.setObjectName("cardTitle")
            activity_layout.addWidget(activity_title)
            self.dashboard_activity = QLabel("No active logs")
            self.dashboard_activity.setObjectName("emptyState")
            self.dashboard_activity.setAlignment(Qt.AlignmentFlag.AlignCenter)
            activity_layout.addWidget(self.dashboard_activity, 1)
            layout.addWidget(activity, 1)
            self._refresh_dashboard()
            return page

        def _dashboard_card(self, title, value, detail):
            card = QFrame()
            card.setObjectName("card")
            card_layout = QVBoxLayout(card)
            heading = QLabel(title)
            heading.setObjectName("cardTitle")
            value_label = QLabel(value)
            value_label.setObjectName("cardValue")
            detail_label = QLabel(detail)
            detail_label.setObjectName("cardDetail")
            card_layout.addWidget(heading)
            card_layout.addWidget(value_label)
            card_layout.addWidget(detail_label)
            card.value_label = value_label
            return card

        def _update_tracking_controls(self):
            self._refresh_dashboard()

        def _refresh_dashboard(self):
            status = backend.get_backend_status()
            self.backend_running = status["running"]
            if hasattr(self, "anti_afk_status") and anti_afk.is_running():
                self.anti_afk_status.setText(anti_afk.get_status()["status"])
            self.status_label.setText("●  TRACKING" if self.backend_running else "●  PAUSED")
            self.start_button.setEnabled(not self.backend_running)
            self.stop_button.setEnabled(self.backend_running)
            if hasattr(self, "dashboard_status"):
                self.dashboard_status.value_label.setText("TRACKING" if self.backend_running else "PAUSED")
                elapsed = 0
                if status["started_at"]:
                    elapsed = max(0, int(time.time() - status["started_at"]))
                self.dashboard_time.value_label.setText(
                    f"{elapsed // 3600:02d}:{elapsed % 3600 // 60:02d}:{elapsed % 60:02d}"
                )
                self.dashboard_logs.value_label.setText(str(status["active_logs"]))
                webhook_count = sum(
                    bool(instance.get("webhook_url") or self.config.get("webhook_url"))
                    for instance in self.config.get("instances", [])
                )
                self.dashboard_biomes.value_label.setText(str(webhook_count))
                self.dashboard_ram.value_label.setText(
                    "ENABLED" if self.config.get("ram_trim_enabled", True) else "DISABLED"
                )
                self.dashboard_activity.setText(
                    "Active: " + ", ".join(status["active_log_names"])
                    if self.backend_running else
                    "No active logs"
                )

        def _start_tracking(self):
            self.backend_running = backend.start_backend_async() or backend.is_backend_running()
            if self.anti_afk_enabled.isChecked():
                self._start_anti_afk()
            self._update_tracking_controls()

        def _stop_tracking(self):
            backend.stop_backend()
            anti_afk.stop()
            self.backend_running = False
            self._update_tracking_controls()

        def _anti_afk_tab(self):
            page = QWidget()
            layout = QVBoxLayout(page)
            self.anti_afk_enabled = QCheckBox("Enable Anti-AFK while Cyclone is running")
            self.anti_afk_enabled.setChecked(self.config.get("anti_afk_enabled", False))
            self.anti_afk_enabled.stateChanged.connect(self._toggle_anti_afk)
            layout.addWidget(self.anti_afk_enabled)
            form = QFormLayout()
            self.anti_afk_mode = QComboBox()
            self.anti_afk_mode.addItem("Single instance", "single")
            self.anti_afk_mode.addItem("Multiple instances", "multi")
            self.anti_afk_mode.setCurrentIndex(1 if self.config.get("anti_afk_mode", "single") == "multi" else 0)
            self.anti_afk_interval = QSpinBox()
            self.anti_afk_interval.setRange(60, 86400)
            self.anti_afk_interval.setSingleStep(60)
            self.anti_afk_interval.setSuffix(" seconds")
            self.anti_afk_interval.setValue(max(60, int(self.config.get("anti_afk_interval", 600))))
            form.addRow("Mode", self.anti_afk_mode)
            form.addRow("Press Space every", self.anti_afk_interval)
            layout.addLayout(form)
            self.anti_afk_status = QLabel("Ready")
            layout.addWidget(self.anti_afk_status)
            save = QPushButton("Save Anti-AFK settings")
            save.clicked.connect(self._save_anti_afk)
            layout.addWidget(save)
            return page

        def _save_anti_afk(self):
            self.config["anti_afk_enabled"] = self.anti_afk_enabled.isChecked()
            self.config["anti_afk_mode"] = self.anti_afk_mode.currentData()
            self.config["anti_afk_interval"] = self.anti_afk_interval.value()
            backend.save_config(self.config)
            self.anti_afk_status.setText("Settings saved")

        def _start_anti_afk(self):
            self._save_anti_afk()
            if not self.anti_afk_enabled.isChecked():
                anti_afk.stop()
                self.anti_afk_status.setText("Enable Anti-AFK first")
                return
            anti_afk.start(self.accounts, self.anti_afk_mode.currentData(), self.anti_afk_interval.value(), backend.find_log_for_accounts)
            self.anti_afk_status.setText("Running; targeting Roblox window(s)")

        def _toggle_anti_afk(self, state):
            if backend.is_backend_running():
                self._start_anti_afk() if state else anti_afk.stop()

        def _instances_tab(self):
            page = QWidget()
            layout = QVBoxLayout(page)
            self.instance_list = QListWidget()
            self.instance_list.currentRowChanged.connect(self._load_instance)
            layout.addWidget(self.instance_list)
            form = QFormLayout()
            self.instance_name = QLineEdit()
            self.auto_log = QCheckBox("Auto-detect by Roblox user ID")
            self.auto_log.setChecked(True)
            self.webhook_url = QLineEdit()
            self.webhook_url.setEchoMode(QLineEdit.EchoMode.Password)
            self.account_picker = QListWidget()
            self.account_picker.setMaximumHeight(110)
            form.addRow("Name", self.instance_name)
            form.addRow("Automatic log detection", self.auto_log)
            form.addRow("Discord webhook destination", self.webhook_url)
            form.addRow("Accounts for this webhook", self.account_picker)
            layout.addLayout(form)
            buttons = QHBoxLayout()
            add = QPushButton("Add instance")
            remove = QPushButton("Remove")
            save = QPushButton("Save instance")
            add.clicked.connect(self._add_instance)
            remove.clicked.connect(self._remove_instance)
            save.clicked.connect(self._save_instance)
            buttons.addWidget(add)
            buttons.addWidget(remove)
            buttons.addStretch()
            buttons.addWidget(save)
            layout.addLayout(buttons)
            self._refresh_account_picker()
            self._refresh_instances()
            return page

        def _accounts_tab(self):
            page = QWidget()
            layout = QVBoxLayout(page)
            self.account_list = QListWidget()
            self.account_list.currentRowChanged.connect(self._load_account)
            layout.addWidget(self.account_list)
            form = QFormLayout()
            self.account_username = QLineEdit()
            self.account_user_id = QLineEdit()
            self.account_user_id.setPlaceholderText("Numeric Roblox user ID")
            self.account_link = QLineEdit()
            form.addRow("Username", self.account_username)
            form.addRow("Roblox user ID", self.account_user_id)
            form.addRow("Private link", self.account_link)
            layout.addLayout(form)
            buttons = QHBoxLayout()
            add = QPushButton("Add account")
            remove = QPushButton("Remove")
            save = QPushButton("Save account")
            add.clicked.connect(self._add_account)
            remove.clicked.connect(self._remove_account)
            save.clicked.connect(self._save_account)
            buttons.addWidget(add)
            buttons.addWidget(remove)
            buttons.addStretch()
            buttons.addWidget(save)
            layout.addLayout(buttons)
            self._refresh_accounts_list()
            return page

        def _biomes_tab(self):
            page = QWidget()
            layout = QVBoxLayout(page)
            self.biome_list = QTableWidget(0, 4)
            self.biome_list.setHorizontalHeaderLabels(["Biome", "Track", "Send message", "Ping everyone"])
            self.biome_list.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            self.biome_list.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
            self.biome_list.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
            self.biome_list.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
            self.biome_list.verticalHeader().setVisible(False)
            self.biome_list.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            for biome in self.biomes:
                row = self.biome_list.rowCount()
                self.biome_list.insertRow(row)
                self.biome_list.setItem(row, 0, QTableWidgetItem(biome.get("name", "Unnamed")))
                self._add_biome_checkbox(row, 1, biome.get("track", biome.get("enabled", True)))
                self._add_biome_checkbox(row, 2, biome.get("send_message", True))
                self._add_biome_checkbox(row, 3, biome.get("ping_everyone", biome.get("ping", False)))
            layout.addWidget(self.biome_list)
            save = QPushButton("Save biome settings")
            save.clicked.connect(self._save_biomes)
            layout.addWidget(save)
            return page

        def _settings_tab(self):
            page = QWidget()
            layout = QVBoxLayout(page)
            form = QFormLayout()
            macro_name = QLabel(self.config.get("macro_name", "Cyclone"))
            version = QLabel(self.config.get("version", "1.0.0"))
            self.global_webhook = QLineEdit(self.config.get("webhook_url", ""))
            self.global_webhook.setEchoMode(QLineEdit.EchoMode.Password)
            self.trim_interval = QLineEdit(str(self.config.get("trim_interval", 60)))
            self.ram_trim_enabled = QCheckBox("Enable periodic Windows RAM trimming")
            self.ram_trim_enabled.setChecked(self.config.get("ram_trim_enabled", True))
            self.theme_picker = QComboBox()
            self.theme_picker.addItems(list(themes))
            self.theme_picker.setCurrentText(self.config.get("theme", "Obsidian"))
            self.theme_picker.currentTextChanged.connect(self._apply_theme)
            form.addRow("Macro name", macro_name)
            form.addRow("Version", version)
            form.addRow("Fallback webhook", self.global_webhook)
            form.addRow("RAM trim interval (seconds)", self.trim_interval)
            form.addRow("RAM trimmer", self.ram_trim_enabled)
            form.addRow("Theme", self.theme_picker)
            layout.addLayout(form)
            save = QPushButton("Save settings")
            save.clicked.connect(self._save_settings)
            layout.addWidget(save)
            trim_now = QPushButton("Trim memory now")
            trim_now.clicked.connect(self._trim_memory_now)
            layout.addWidget(trim_now)
            layout.addStretch()
            return page

        def _add_biome_checkbox(self, row, column, checked):
            checkbox = QCheckBox()
            checkbox.setChecked(bool(checked))
            wrapper = QWidget()
            box_layout = QHBoxLayout(wrapper)
            box_layout.setContentsMargins(0, 0, 0, 0)
            box_layout.addStretch()
            box_layout.addWidget(checkbox)
            box_layout.addStretch()
            self.biome_list.setCellWidget(row, column, wrapper)

        def _refresh_instances(self):
            self.instance_list.clear()
            for instance in self.config.get("instances", []):
                self.instance_list.addItem(instance.get("name", instance.get("log_path", "Instance")))
            if self.instance_list.count():
                self.instance_list.setCurrentRow(0)

        def _load_instance(self, row):
            instances = self.config.get("instances", [])
            if 0 <= row < len(instances):
                instance = instances[row]
                self.instance_name.setText(instance.get("name", ""))
                self.auto_log.setChecked(instance.get("auto_log", False))
                self.webhook_url.setText(instance.get("webhook_url", self.config.get("webhook_url", "")))
                selected = instance.get("account_indices", [instance.get("account_index", 0)])
                for index in range(self.account_picker.count()):
                    self.account_picker.item(index).setCheckState(
                        Qt.CheckState.Checked if index in selected else Qt.CheckState.Unchecked
                    )

        def _add_instance(self):
            instance_number = len(self.config.get("instances", [])) + 1
            self.config.setdefault("instances", []).append({
                "name": f"Instance {instance_number}",
                "log_path": "",
                "webhook_url": "",
                "account_indices": [],
                "auto_log": True,
            })
            self._refresh_instances()
            self.instance_list.setCurrentRow(self.instance_list.count() - 1)

        def _remove_instance(self):
            row = self.instance_list.currentRow()
            if row >= 0:
                self.config["instances"].pop(row)
                backend.save_config(self.config)
                self._refresh_instances()

        def _save_instance(self):
            row = self.instance_list.currentRow()
            if row < 0:
                return
            account_indices = [
                index for index in range(self.account_picker.count())
                if self.account_picker.item(index).checkState() == Qt.CheckState.Checked
            ]
            self.config["instances"][row] = {
                "name": self.instance_name.text().strip(),
                "log_path": self.config["instances"][row].get("log_path", ""),
                "webhook_url": self.webhook_url.text().strip(),
                "account_indices": account_indices,
                "auto_log": self.auto_log.isChecked(),
            }
            backend.save_config(self.config)
            self._refresh_instances()
            self.instance_list.setCurrentRow(row)

        def _refresh_account_picker(self):
            self.account_picker.clear()
            for account in self.accounts:
                item = QListWidgetItem(account.get("username", "Unnamed"))
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                item.setCheckState(Qt.CheckState.Unchecked)
                self.account_picker.addItem(item)

        def _refresh_accounts_list(self):
            self.account_list.clear()
            for account in self.accounts:
                self.account_list.addItem(account.get("username", "Unnamed"))
            if self.account_list.count():
                self.account_list.setCurrentRow(0)

        def _load_account(self, row):
            if 0 <= row < len(self.accounts):
                self.account_username.setText(self.accounts[row].get("username", ""))
                self.account_user_id.setText(self.accounts[row].get("roblox_user_id", self.accounts[row].get("user_id", "")))
                self.account_link.setText(self.accounts[row].get("private_link", ""))

        def _add_account(self):
            self.accounts.append({"username": "New account", "roblox_user_id": "", "private_link": ""})
            self._refresh_accounts_list()
            self._refresh_account_picker()
            self.account_list.setCurrentRow(self.account_list.count() - 1)

        def _remove_account(self):
            row = self.account_list.currentRow()
            if row >= 0:
                self.accounts.pop(row)
                backend.save_accounts(self.accounts)
                self._refresh_accounts_list()
                self._refresh_account_picker()

        def _save_account(self):
            row = self.account_list.currentRow()
            if row < 0:
                return
            self.accounts[row] = {
                "username": self.account_username.text().strip(),
                "roblox_user_id": self.account_user_id.text().strip(),
                "private_link": self.account_link.text().strip(),
            }
            backend.save_accounts(self.accounts)
            self._refresh_accounts_list()
            self._refresh_account_picker()
            self.account_list.setCurrentRow(row)

        def _save_biomes(self):
            for index, biome in enumerate(self.biomes):
                track_box = self.biome_list.cellWidget(index, 1).findChild(QCheckBox)
                message_box = self.biome_list.cellWidget(index, 2).findChild(QCheckBox)
                everyone_box = self.biome_list.cellWidget(index, 3).findChild(QCheckBox)
                biome["track"] = track_box.isChecked()
                biome["send_message"] = message_box.isChecked()
                biome["ping_everyone"] = everyone_box.isChecked()
            backend._save_json("biomes.json", self.biomes)
            QMessageBox.information(self, "Cyclone", "Biome settings saved.")

        def _save_settings(self):
            try:
                trim_interval = max(10, int(self.trim_interval.text()))
            except ValueError:
                QMessageBox.warning(self, "Cyclone", "RAM trim interval must be a whole number.")
                return
            self.config.update({
                "webhook_url": self.global_webhook.text().strip(),
                "trim_interval": trim_interval,
                "ram_trim_enabled": self.ram_trim_enabled.isChecked(),
                "theme": self.theme_picker.currentText(),
            })
            backend.save_config(self.config)
            self.setWindowTitle(self.config["macro_name"])
            QMessageBox.information(self, "Cyclone", "Settings saved.")

        def _trim_memory_now(self):
            if backend.trim_working_set():
                QMessageBox.information(self, "Cyclone", "Windows working memory was trimmed.")
            else:
                QMessageBox.information(self, "Cyclone", "RAM trimming is unavailable on this system.")

        def closeEvent(self, event):
            backend.stop_backend()
            anti_afk.stop()
            event.accept()

    app = QApplication.instance() or QApplication(sys.argv)
    window = CycloneWindow()
    window.show()
    app.exec()
