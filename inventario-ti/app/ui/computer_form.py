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

from app.services.computer_service import VALID_STATUSES
from app.services.employee_service import EmployeeService
from app.services.reference_data_service import ReferenceDataService


class ComputerFormDialog(QDialog):
    def __init__(self, parent=None, computer=None):
        super().__init__(parent)
        self.computer = computer or {}
        self.reference_service = ReferenceDataService()
        self.employee_service = EmployeeService()
        self.setWindowTitle("Editar computador" if computer else "Adicionar computador")
        self.setMinimumWidth(460)
        self.setModal(True)
        self._build_ui()
        self._fill_fields()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 18, 18, 18)
        main_layout.setSpacing(14)

        title = QLabel("Dados do computador")
        title.setObjectName("TitleLabel")
        main_layout.addWidget(title)

        form_frame = QFrame()
        form_frame.setObjectName("FormFrame")
        form_layout = QFormLayout(form_frame)
        form_layout.setContentsMargins(18, 18, 18, 18)
        form_layout.setSpacing(12)
        form_layout.setLabelAlignment(Qt.AlignRight)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ex.: FINANCEIRO-01")

        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Ex.: 192.168.0.10")

        self.os_input = self._create_reference_combo("sistemas_operacionais")

        self.antivirus_input = self._create_reference_combo("antivirus")

        self.sector_input = self._create_reference_combo("setores")
        self.sector_input.currentTextChanged.connect(self._reload_responsible_options_for_sector_change)

        self.owner_input = QComboBox()
        self.owner_input.setEditable(True)

        self.status_input = QComboBox()
        self.status_input.addItems(VALID_STATUSES)

        form_layout.addRow("Nome da máquina *", self.name_input)
        form_layout.addRow("IP *", self.ip_input)
        form_layout.addRow("Sistema Operacional *", self.os_input)
        form_layout.addRow("Antivírus", self.antivirus_input)
        form_layout.addRow("Setor", self.sector_input)
        form_layout.addRow("Responsável", self.owner_input)
        form_layout.addRow("Status de segurança *", self.status_input)

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
        self.name_input.setText(self.computer.get("nome", ""))
        self.ip_input.setText(self.computer.get("ip", ""))
        self._set_combo_text(self.os_input, self.computer.get("sistema_operacional", ""))
        self._set_combo_text(self.antivirus_input, self.computer.get("antivirus", "") or "")
        self._set_combo_text(self.sector_input, self.computer.get("setor", "") or "")
        self._reload_responsible_options(self.sector_input.currentText())
        self._set_combo_text(self.owner_input, self.computer.get("responsavel", "") or "")

        status = self.computer.get("status_seguranca", VALID_STATUSES[0])
        index = self.status_input.findText(status)
        self.status_input.setCurrentIndex(index if index >= 0 else 0)

    def get_data(self):
        return {
            "nome": self.name_input.text().strip(),
            "ip": self.ip_input.text().strip(),
            "sistema_operacional": self.os_input.currentText().strip(),
            "antivirus": self.antivirus_input.currentText().strip(),
            "setor": self.sector_input.currentText().strip(),
            "responsavel": self.owner_input.currentText().strip(),
            "status_seguranca": self.status_input.currentText(),
        }

    def _accept_if_valid(self):
        data = self.get_data()
        if not data["nome"] or not data["ip"] or not data["sistema_operacional"]:
            QMessageBox.warning(
                self,
                "Campos obrigatórios",
                "Preencha Nome da máquina, IP e Sistema Operacional.",
            )
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

    def _reload_responsible_options(self, sector):
        current_responsible = self.owner_input.currentText().strip()
        names = self.employee_service.list_employee_names_by_sector(sector)

        self.owner_input.blockSignals(True)
        self.owner_input.clear()
        self.owner_input.addItem("")
        self.owner_input.addItems(names)

        if current_responsible:
            self._set_combo_text(self.owner_input, current_responsible)
        else:
            self.owner_input.setCurrentIndex(0)

        self.owner_input.blockSignals(False)

    def _reload_responsible_options_for_sector_change(self, sector):
        names = self.employee_service.list_employee_names_by_sector(sector)

        self.owner_input.blockSignals(True)
        self.owner_input.clear()
        self.owner_input.addItem("")
        self.owner_input.addItems(names)
        self.owner_input.setCurrentIndex(0)
        self.owner_input.blockSignals(False)
