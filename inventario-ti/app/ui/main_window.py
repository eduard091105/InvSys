from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.services.computer_service import VALID_STATUSES, ComputerService
from app.services.reference_data_service import ReferenceDataService
from app.ui.computer_form import ComputerFormDialog
from app.ui.employee_tab import EmployeeTab
from app.ui.reference_manager import ReferenceManagerWidget
from app.ui.styles import DEFAULT_THEME, THEMES, get_theme_style


class MainWindow(QMainWindow):
    TABLE_HEADERS = [
        "Nome",
        "IP",
        "Sistema Operacional",
        "Antivirus",
        "Setor",
        "Responsavel",
        "Status",
    ]

    def __init__(self):
        super().__init__()
        self.computer_service = ComputerService()
        self.reference_service = ReferenceDataService()
        self.current_computers = []
        self.setWindowTitle("InvSys - Inventario de Computadores")
        self.resize(1150, 700)
        self._build_ui()
        self.refresh_reference_filters()
        self.load_computers()

    def _build_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(24, 22, 24, 24)
        main_layout.setSpacing(16)

        header_layout = QVBoxLayout()
        title = QLabel("InvSys")
        title.setObjectName("TitleLabel")
        subtitle = QLabel("Gerencie computadores, setores e status de seguranca.")
        subtitle.setObjectName("SubtitleLabel")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addLayout(header_layout)

        self.tabs = QTabWidget()
        self.tabs.addTab(self._build_inventory_tab(), "Inventario")
        self.employee_tab = EmployeeTab()
        self.employee_tab.data_changed.connect(self.refresh_reference_filters)
        self.tabs.addTab(self.employee_tab, "Funcionarios")
        self.tabs.addTab(self._build_registrations_tab(), "Cadastros")
        main_layout.addWidget(self.tabs)

    def _build_inventory_tab(self):
        inventory_widget = QWidget()
        main_layout = QVBoxLayout(inventory_widget)
        main_layout.setContentsMargins(0, 12, 0, 0)
        main_layout.setSpacing(14)

        toolbar = QFrame()
        toolbar.setObjectName("ToolbarFrame")
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(14, 12, 14, 12)
        toolbar_layout.setSpacing(10)

        filter_label = QLabel("Status:")
        self.status_filter = QComboBox()
        self.status_filter.addItems(("Todos", *VALID_STATUSES))
        self.status_filter.currentTextChanged.connect(self.load_computers)

        sector_label = QLabel("Setor:")
        self.sector_filter = QComboBox()
        self.sector_filter.currentTextChanged.connect(self.load_computers)

        theme_label = QLabel("Tema:")
        self.theme_selector = QComboBox()
        self.theme_selector.addItems(THEMES.keys())
        self._load_theme_preference()
        self.theme_selector.currentTextChanged.connect(self.change_theme)

        add_button = QPushButton("Adicionar")
        add_button.clicked.connect(self.add_computer)

        self.selection_button = QPushButton("Selecionar")
        self.selection_button.setObjectName("SecondaryButton")
        self.selection_button.setCheckable(True)
        self.selection_button.toggled.connect(self.toggle_selection_mode)

        self.edit_button = QPushButton("Editar")
        self.edit_button.setObjectName("SecondaryButton")
        self.edit_button.clicked.connect(self.edit_computer)

        self.delete_button = QPushButton("Excluir")
        self.delete_button.setObjectName("DangerButton")
        self.delete_button.clicked.connect(self.delete_computer)

        toolbar_layout.addWidget(filter_label)
        toolbar_layout.addWidget(self.status_filter)
        toolbar_layout.addSpacing(10)
        toolbar_layout.addWidget(sector_label)
        toolbar_layout.addWidget(self.sector_filter)
        toolbar_layout.addSpacing(10)
        toolbar_layout.addWidget(theme_label)
        toolbar_layout.addWidget(self.theme_selector)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(add_button)
        toolbar_layout.addWidget(self.selection_button)
        toolbar_layout.addWidget(self.edit_button)
        toolbar_layout.addWidget(self.delete_button)
        main_layout.addWidget(toolbar)

        self.table = QTableWidget()
        self.table.setColumnCount(len(self.TABLE_HEADERS))
        self.table.setHorizontalHeaderLabels(self.TABLE_HEADERS)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.open_table_menu)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setHighlightSections(False)
        self.table.setAlternatingRowColors(True)
        self.table.doubleClicked.connect(self.edit_computer)
        main_layout.addWidget(self.table)

        return inventory_widget

    def _build_registrations_tab(self):
        registrations_tabs = QTabWidget()
        self.os_manager = ReferenceManagerWidget("Sistema Operacional", "sistemas_operacionais")
        self.antivirus_manager = ReferenceManagerWidget("Antivirus", "antivirus")
        self.sector_manager = ReferenceManagerWidget("Setor", "setores")
        self.ai_license_manager = ReferenceManagerWidget("Licenca de IA", "licencas_ia")

        self.os_manager.data_changed.connect(self.refresh_reference_filters)
        self.antivirus_manager.data_changed.connect(self.refresh_reference_filters)
        self.sector_manager.data_changed.connect(self.refresh_reference_filters)
        self.sector_manager.data_changed.connect(self.load_computers)
        self.sector_manager.data_changed.connect(self.employee_tab.refresh_filters)
        self.ai_license_manager.data_changed.connect(self.employee_tab.refresh_filters)

        registrations_tabs.addTab(self.os_manager, "Sistemas Operacionais")
        registrations_tabs.addTab(self.antivirus_manager, "Antivirus")
        registrations_tabs.addTab(self.sector_manager, "Setores")
        registrations_tabs.addTab(self.ai_license_manager, "Licencas de IA")
        return registrations_tabs

    def refresh_reference_filters(self):
        current_sector = self.sector_filter.currentText() if hasattr(self, "sector_filter") else "Todos"
        self.sector_filter.blockSignals(True)
        self.sector_filter.clear()
        self.sector_filter.addItem("Todos")
        self.sector_filter.addItems(self.reference_service.list_names("setores"))

        index = self.sector_filter.findText(current_sector)
        self.sector_filter.setCurrentIndex(index if index >= 0 else 0)
        self.sector_filter.blockSignals(False)

    def load_computers(self):
        status = self.status_filter.currentText()
        sector = self.sector_filter.currentText()
        self.current_computers = self.computer_service.list_computers(status, sector)

        self.table.setRowCount(len(self.current_computers))
        for row_index, computer in enumerate(self.current_computers):
            values = [
                computer["nome"],
                computer["ip"],
                computer["sistema_operacional"],
                computer.get("antivirus", "") or "",
                computer.get("setor", "") or "",
                computer.get("responsavel", "") or "",
                computer.get("status_seguranca", "") or "",
            ]

            for column_index, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setData(Qt.UserRole, computer["id"])
                if column_index == 6:
                    item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_index, column_index, item)

        self.table.resizeRowsToContents()

    def add_computer(self):
        dialog = ComputerFormDialog(self)
        if dialog.exec_():
            try:
                self.computer_service.create_computer(dialog.get_data())
                self.refresh_reference_filters()
                self.load_computers()
            except ValueError as error:
                QMessageBox.warning(self, "Dados invalidos", str(error))
            except Exception as error:
                QMessageBox.critical(self, "Erro ao cadastrar", str(error))

    def edit_computer(self):
        computer_ids = self._selected_computer_ids()
        if len(computer_ids) != 1:
            QMessageBox.information(self, "Selecao necessaria", "Selecione um computador para editar.")
            return

        computer_id = computer_ids[0]
        computer = self.computer_service.get_computer(computer_id)
        if not computer:
            QMessageBox.warning(self, "Registro nao encontrado", "O computador selecionado nao existe mais.")
            self.load_computers()
            return

        dialog = ComputerFormDialog(self, computer)
        if dialog.exec_():
            try:
                self.computer_service.update_computer(computer_id, dialog.get_data())
                self.refresh_reference_filters()
                self.load_computers()
            except ValueError as error:
                QMessageBox.warning(self, "Dados invalidos", str(error))
            except Exception as error:
                QMessageBox.critical(self, "Erro ao editar", str(error))

    def delete_computer(self):
        computer_ids = self._selected_computer_ids()
        if not computer_ids:
            QMessageBox.information(self, "Selecao necessaria", "Selecione um ou mais computadores para excluir.")
            return

        count = len(computer_ids)
        message = (
            "Deseja excluir o computador selecionado?"
            if count == 1
            else f"Deseja excluir {count} computadores selecionados?"
        )
        confirmation = QMessageBox.question(
            self,
            "Confirmar exclusao",
            message,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if confirmation == QMessageBox.Yes:
            try:
                self.computer_service.delete_computers(computer_ids)
                self.load_computers()
            except Exception as error:
                QMessageBox.critical(self, "Erro ao excluir", str(error))

    def open_table_menu(self, position):
        row = self.table.rowAt(position.y())
        if row < 0:
            return

        if not self.selection_button.isChecked():
            self.table.selectRow(row)

        menu = QMenu(self)
        edit_action = menu.addAction("Editar")
        delete_action = menu.addAction("Excluir")

        selected_action = menu.exec_(self.table.viewport().mapToGlobal(position))
        if selected_action == edit_action:
            self.edit_computer()
        elif selected_action == delete_action:
            self.delete_computer()

    def toggle_selection_mode(self, enabled):
        if enabled:
            self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
            self.selection_button.setText("Selecionando")
            self.edit_button.setEnabled(False)
        else:
            self.table.clearSelection()
            self.table.setSelectionMode(QAbstractItemView.SingleSelection)
            self.selection_button.setText("Selecionar")
            self.edit_button.setEnabled(True)

    def change_theme(self, theme_name):
        QApplication.instance().setStyleSheet(get_theme_style(theme_name))
        QSettings().setValue("theme", theme_name)

    def _load_theme_preference(self):
        selected_theme = QSettings().value("theme", DEFAULT_THEME)
        index = self.theme_selector.findText(selected_theme)
        self.theme_selector.setCurrentIndex(index if index >= 0 else 0)

    def _selected_computer_ids(self):
        computer_ids = []
        for row_index in sorted({item.row() for item in self.table.selectedItems()}):
            first_column_item = self.table.item(row_index, 0)
            if first_column_item:
                computer_ids.append(first_column_item.data(Qt.UserRole))

        return computer_ids
