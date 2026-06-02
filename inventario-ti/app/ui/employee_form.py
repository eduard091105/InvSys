from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from app.services.employee_service import LICENSE_STATUSES
from app.services.reference_data_service import ReferenceDataService


class EmployeeFormDialog(QDialog):
    def __init__(self, parent=None, employee=None):
        super().__init__(parent)
        self.employee = employee or {}
        self.reference_service = ReferenceDataService()
        self.setWindowTitle("Editar funcionario" if employee else "Adicionar funcionario")
        self.setMinimumWidth(460)
        self.setModal(True)
        self._build_ui()
        self._fill_fields()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 18, 18, 18)
        main_layout.setSpacing(14)

        title = QLabel("Dados do funcionario")
        title.setObjectName("TitleLabel")
        main_layout.addWidget(title)

        form_frame = QFrame()
        form_frame.setObjectName("FormFrame")
        form_layout = QFormLayout(form_frame)
        form_layout.setContentsMargins(18, 18, 18, 18)
        form_layout.setSpacing(12)
        form_layout.setLabelAlignment(Qt.AlignRight)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ex.: Ana Martins")

        self.sector_input = self._create_reference_combo("setores")

        self.role_input = QLineEdit()
        self.role_input.setPlaceholderText("Ex.: Analista de Suporte")

        self.license_input = self._create_reference_combo("licencas_ia")

        self.license_status_input = QComboBox()
        self.license_status_input.addItems(LICENSE_STATUSES)

        form_layout.addRow("Nome *", self.name_input)
        form_layout.addRow("Setor", self.sector_input)
        form_layout.addRow("Cargo", self.role_input)
        form_layout.addRow("Licenca de IA", self.license_input)
        form_layout.addRow("Status da licenca", self.license_status_input)

        main_layout.addWidget(form_frame)

        button_layout = QHBoxLayout()
        button_layout.addStretch()

        cancel_button = QPushButton("Cancelar")
        cancel_button.setObjectName("SecondaryButton")
        cancel_button.clicked.connect(self.reject)

        save_button = QPushButton("Salvar")
        save_button.clicked.connect(self._accept_if_valid)

        button_layout.addWidget(cancel_button)
        button_layout.addWidget(save_button)
        main_layout.addLayout(button_layout)

    def _fill_fields(self):
        self.name_input.setText(self.employee.get("nome", ""))
        self._set_combo_text(self.sector_input, self.employee.get("setor", "") or "")
        self.role_input.setText(self.employee.get("cargo", "") or "")
        self._set_combo_text(self.license_input, self.employee.get("licenca_ia", "") or "")

        status = self.employee.get("status_licenca", LICENSE_STATUSES[0])
        index = self.license_status_input.findText(status)
        self.license_status_input.setCurrentIndex(index if index >= 0 else 0)

    def get_data(self):
        return {
            "nome": self.name_input.text().strip(),
            "setor": self.sector_input.currentText().strip(),
            "cargo": self.role_input.text().strip(),
            "licenca_ia": self.license_input.currentText().strip(),
            "status_licenca": self.license_status_input.currentText(),
        }

    def _accept_if_valid(self):
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Campos obrigatorios", "Preencha o nome do funcionario.")
            return

        self.accept()

    def _create_reference_combo(self, reference_type):
        combo = QComboBox()
        combo.setEditable(True)
        combo.addItem("")
        combo.addItems(self.reference_service.list_names(reference_type))
        return combo

    def _set_combo_text(self, combo, value):
        if not value:
            combo.setCurrentIndex(0)
            return

        index = combo.findText(value)
        if index < 0:
            combo.addItem(value)
            index = combo.findText(value)

        combo.setCurrentIndex(index)
