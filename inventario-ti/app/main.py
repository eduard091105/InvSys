import sys
import ctypes
from pathlib import Path

from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from app.ui.main_window import MainWindow
from app.ui.styles import DEFAULT_THEME, get_theme_style


def main():
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "InvSys.InventorySystem.1.0"
        )
    except Exception:
        pass

    application = QApplication(sys.argv)
    application.setOrganizationName("Empresa")
    application.setApplicationName("InvSys")
    application.setStyle("Fusion")

    icon_path = _resource_path("assets/app.ico")
    if icon_path.exists():
        icon = QIcon(str(icon_path))
        application.setWindowIcon(icon)

    settings = QSettings()
    selected_theme = settings.value("theme", DEFAULT_THEME)
    application.setStyleSheet(get_theme_style(selected_theme))

    window = MainWindow()

    if icon_path.exists():
        window.setWindowIcon(icon)

    window.show()

    sys.exit(application.exec_())


def _resource_path(relative_path):
    base_path = Path(
        getattr(
            sys,
            "_MEIPASS",
            Path(__file__).resolve().parents[1]
        )
    )
    return base_path / relative_path


if __name__ == "__main__":
    main()