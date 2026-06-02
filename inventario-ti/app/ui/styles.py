LIGHT_STYLE = """
QMainWindow,
QDialog,
QMessageBox {
    background-color: #f4f6f8;
}

QWidget {
    color: #1f2937;
    font-family: Segoe UI, Arial, sans-serif;
    font-size: 10pt;
}

QLabel#TitleLabel {
    font-size: 20pt;
    font-weight: 700;
    color: #111827;
}

QLabel#SubtitleLabel {
    color: #6b7280;
}

QFrame#ToolbarFrame,
QFrame#FormFrame {
    background-color: #ffffff;
    border: 1px solid #d9e0e7;
    border-radius: 8px;
}

QTabWidget::pane {
    border: 1px solid #d9e0e7;
    border-radius: 8px;
    background-color: #ffffff;
}

QTabBar::tab {
    background-color: #e5e7eb;
    color: #374151;
    border: 1px solid #d9e0e7;
    border-bottom: none;
    padding: 9px 14px;
    margin-right: 3px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}

QTabBar::tab:selected {
    background-color: #ffffff;
    color: #111827;
}

QTableWidget {
    background-color: #ffffff;
    alternate-background-color: #f8fafc;
    border: 1px solid #d9e0e7;
    border-radius: 8px;
    gridline-color: #e5e7eb;
    selection-background-color: #dbeafe;
    selection-color: #111827;
}

QListWidget {
    background-color: #ffffff;
    alternate-background-color: #f8fafc;
    border: 1px solid #d9e0e7;
    border-radius: 8px;
    padding: 6px;
    selection-background-color: #dbeafe;
    selection-color: #111827;
}

QMenu {
    background-color: #ffffff;
    color: #1f2937;
    border: 1px solid #d9e0e7;
}

QMenu::item {
    padding: 8px 22px;
}

QMenu::item:selected {
    background-color: #dbeafe;
}

QHeaderView::section {
    background-color: #eef2f7;
    color: #374151;
    border: none;
    border-right: 1px solid #d9e0e7;
    padding: 9px;
    font-weight: 600;
}

QLineEdit,
QComboBox {
    background-color: #ffffff;
    color: #1f2937;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 8px 10px;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    color: #1f2937;
    selection-background-color: #dbeafe;
    selection-color: #111827;
}

QLineEdit:focus,
QComboBox:focus {
    border-color: #2563eb;
}

QPushButton {
    background-color: #2563eb;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 9px 14px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #1d4ed8;
}

QPushButton:pressed {
    background-color: #1e40af;
}

QPushButton#SecondaryButton {
    background-color: #e5e7eb;
    color: #111827;
}

QPushButton#SecondaryButton:hover {
    background-color: #d1d5db;
}

QPushButton#DangerButton {
    background-color: #dc2626;
}

QPushButton#DangerButton:hover {
    background-color: #b91c1c;
}
"""


DARK_STYLE = """
QMainWindow,
QDialog,
QMessageBox {
    background-color: #111827;
}

QWidget {
    color: #e5e7eb;
    font-family: Segoe UI, Arial, sans-serif;
    font-size: 10pt;
}

QLabel#TitleLabel {
    font-size: 20pt;
    font-weight: 700;
    color: #f9fafb;
}

QLabel#SubtitleLabel {
    color: #9ca3af;
}

QFrame#ToolbarFrame,
QFrame#FormFrame {
    background-color: #1f2937;
    border: 1px solid #374151;
    border-radius: 8px;
}

QTabWidget::pane {
    border: 1px solid #374151;
    border-radius: 8px;
    background-color: #1f2937;
}

QTabBar::tab {
    background-color: #111827;
    color: #d1d5db;
    border: 1px solid #374151;
    border-bottom: none;
    padding: 9px 14px;
    margin-right: 3px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}

QTabBar::tab:selected {
    background-color: #1f2937;
    color: #f9fafb;
}

QTableWidget {
    background-color: #1f2937;
    alternate-background-color: #243244;
    border: 1px solid #374151;
    border-radius: 8px;
    gridline-color: #374151;
    selection-background-color: #2563eb;
    selection-color: #ffffff;
}

QTableWidget::item {
    color: #e5e7eb;
}

QListWidget {
    background-color: #1f2937;
    alternate-background-color: #243244;
    border: 1px solid #374151;
    border-radius: 8px;
    padding: 6px;
    selection-background-color: #2563eb;
    selection-color: #ffffff;
}

QListWidget::item {
    color: #e5e7eb;
    padding: 6px;
}

QMenu {
    background-color: #1f2937;
    color: #f9fafb;
    border: 1px solid #374151;
}

QMenu::item {
    padding: 8px 22px;
}

QMenu::item:selected {
    background-color: #2563eb;
}

QHeaderView::section {
    background-color: #111827;
    color: #d1d5db;
    border: none;
    border-right: 1px solid #374151;
    padding: 9px;
    font-weight: 600;
}

QLineEdit,
QComboBox {
    background-color: #111827;
    color: #f9fafb;
    border: 1px solid #4b5563;
    border-radius: 6px;
    padding: 8px 10px;
}

QLineEdit:focus,
QComboBox:focus {
    border-color: #60a5fa;
}

QComboBox QAbstractItemView {
    background-color: #1f2937;
    color: #f9fafb;
    selection-background-color: #2563eb;
    selection-color: #ffffff;
    border: 1px solid #374151;
}

QLineEdit::placeholder {
    color: #9ca3af;
}

QFormLayout QLabel,
QMessageBox QLabel {
    color: #e5e7eb;
}

QPushButton {
    background-color: #2563eb;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 9px 14px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #1d4ed8;
}

QPushButton:pressed {
    background-color: #1e40af;
}

QPushButton#SecondaryButton {
    background-color: #374151;
    color: #f9fafb;
}

QPushButton#SecondaryButton:hover {
    background-color: #4b5563;
}

QPushButton#DangerButton {
    background-color: #dc2626;
}

QPushButton#DangerButton:hover {
    background-color: #b91c1c;
}
"""


THEMES = {
    "Claro": LIGHT_STYLE,
    "Escuro": DARK_STYLE,
}

DEFAULT_THEME = "Claro"


def get_theme_style(theme_name):
    return THEMES.get(theme_name, LIGHT_STYLE)
