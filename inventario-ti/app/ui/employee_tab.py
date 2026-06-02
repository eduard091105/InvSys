from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMenu,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.services.employee_service import EmployeeService
from app.services.reference_data_service import ReferenceDataService
from app.ui.employee_form import EmployeeFormDialog


class EmployeeTab(QWidget):
    data_changed = pyqtSignal()

    TABLE_HEADERS = ["Nome", "Setor", "Cargo", "Licenca de IA", "Status"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.employee_service = EmployeeService()
        self.reference_service = ReferenceDataService()
        self._build_ui()
        self.refresh_filters()
        self.load_employees()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 12, 0, 0)
        layout.setSpacing(14)

        toolbar = QFrame()
        toolbar.setObjectName("ToolbarFrame")
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(14, 12, 14, 12)
        toolbar_layout.setSpacing(10)

        sector_label = QLabel("Setor:")
        self.sector_filter = QComboBox()
        self.sector_filter.currentTextChanged.connect(self.load_employees)

        license_label = QLabel("Licenca:")
        self.license_filter = QComboBox()
        self.license_filter.currentTextChanged.connect(self.load_employees)

        add_button = QPushButton("Adicionar")
        add_button.clicked.connect(self.add_employee)

        edit_button = QPushButton("Editar")
        edit_button.setObjectName("SecondaryButton")
        edit_button.clicked.connect(self.edit_employee)

        delete_button = QPushButton("Excluir")
        delete_button.setObjectName("DangerButton")
        delete_button.clicked.connect(self.delete_employee)

        toolbar_layout.addWidget(sector_label)
        toolbar_layout.addWidget(self.sector_filter)
        toolbar_layout.addSpacing(10)
        toolbar_layout.addWidget(license_label)
        toolbar_layout.addWidget(self.license_filter)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(add_button)
        toolbar_layout.addWidget(edit_button)
        toolbar_layout.addWidget(delete_button)
        layout.addWidget(toolbar)

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
        self.table.doubleClicked.connect(self.edit_employee)
        layout.addWidget(self.table)

    def refresh_filters(self):
        self._reload_filter(self.sector_filter, self.reference_service.list_names("setores"))
        self._reload_filter(self.license_filter, self.reference_service.list_names("licencas_ia"))

    def load_employees(self):
        sector = self.sector_filter.currentText()
        license_name = self.license_filter.currentText()
        employees = self.employee_service.list_employees(sector, license_name)

        self.table.setRowCount(len(employees))
        for row_index, employee in enumerate(employees):
            values = [
                employee["nome"],
                employee.get("setor", "") or "",
                employee.get("cargo", "") or "",
                employee.get("licenca_ia", "") or "",
                employee.get("status_licenca", "") or "",
            ]

            for column_index, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setData(Qt.UserRole, employee["id"])
                if column_index == 4:
                    item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_index, column_index, item)

        self.table.resizeRowsToContents()

    def add_employee(self):
        dialog = EmployeeFormDialog(self)
        if dialog.exec_():
            try:
                self.employee_service.create_employee(dialog.get_data())
                self.refresh_filters()
                self.load_employees()
                self.data_changed.emit()
            except ValueError as error:
                QMessageBox.warning(self, "Dados invalidos", str(error))
            except Exception as error:
                QMessageBox.critical(self, "Erro ao cadastrar", str(error))

    def edit_employee(self):
        employee_id = self._selected_employee_id()
        if employee_id is None:
            QMessageBox.information(self, "Selecao necessaria", "Selecione um funcionario para editar.")
            return

        employee = self.employee_service.get_employee(employee_id)
        if not employee:
            QMessageBox.warning(self, "Registro nao encontrado", "O funcionario selecionado nao existe mais.")
            self.load_employees()
            return

        dialog = EmployeeFormDialog(self, employee)
        if dialog.exec_():
            try:
                self.employee_service.update_employee(employee_id, dialog.get_data())
                self.refresh_filters()
                self.load_employees()
                self.data_changed.emit()
            except ValueError as error:
                QMessageBox.warning(self, "Dados invalidos", str(error))
            except Exception as error:
                QMessageBox.critical(self, "Erro ao editar", str(error))

    def delete_employee(self):
        employee_id = self._selected_employee_id()
        if employee_id is None:
            QMessageBox.information(self, "Selecao necessaria", "Selecione um funcionario para excluir.")
            return

        confirmation = QMessageBox.question(
            self,
            "Confirmar exclusao",
            "Deseja excluir o funcionario selecionado?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if confirmation == QMessageBox.Yes:
            try:
                self.employee_service.delete_employee(employee_id)
                self.load_employees()
            except Exception as error:
                QMessageBox.critical(self, "Erro ao excluir", str(error))

    def open_table_menu(self, position):
        row = self.table.rowAt(position.y())
        if row < 0:
            return

        self.table.selectRow(row)
        menu = QMenu(self)
        edit_action = menu.addAction("Editar")
        delete_action = menu.addAction("Excluir")

        selected_action = menu.exec_(self.table.viewport().mapToGlobal(position))
        if selected_action == edit_action:
            self.edit_employee()
        elif selected_action == delete_action:
            self.delete_employee()

    def _reload_filter(self, combo, values):
        current_value = combo.currentText() if combo.count() else "Todos"
        combo.blockSignals(True)
        combo.clear()
        combo.addItem("Todos")
        combo.addItems(values)
        index = combo.findText(current_value)
        combo.setCurrentIndex(index if index >= 0 else 0)
        combo.blockSignals(False)

    def _selected_employee_id(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return None

        first_column_item = self.table.item(selected_items[0].row(), 0)
        return first_column_item.data(Qt.UserRole)
