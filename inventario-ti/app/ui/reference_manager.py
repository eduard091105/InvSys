from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QInputDialog,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.services.reference_data_service import ReferenceDataService


class ReferenceManagerWidget(QWidget):
    data_changed = pyqtSignal()

    def __init__(self, title, reference_type, parent=None):
        super().__init__(parent)
        self.title = title
        self.reference_type = reference_type
        self.reference_service = ReferenceDataService()
        self._build_ui()
        self.load_items()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.list_widget.itemDoubleClicked.connect(self.edit_item)
        layout.addWidget(self.list_widget)

        button_layout = QHBoxLayout()
        button_layout.addStretch()

        add_button = QPushButton("Adicionar")
        add_button.clicked.connect(self.add_item)

        edit_button = QPushButton("Editar")
        edit_button.setObjectName("SecondaryButton")
        edit_button.clicked.connect(self.edit_item)

        delete_button = QPushButton("Excluir")
        delete_button.setObjectName("DangerButton")
        delete_button.clicked.connect(self.delete_item)

        button_layout.addWidget(add_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        layout.addLayout(button_layout)

    def load_items(self):
        self.list_widget.clear()
        for item in self.reference_service.list_items(self.reference_type):
            list_item = QListWidgetItem(item["nome"])
            list_item.setData(Qt.UserRole, item["id"])
            self.list_widget.addItem(list_item)

    def add_item(self):
        name, accepted = QInputDialog.getText(self, f"Adicionar {self.title}", "Nome:")
        if not accepted:
            return

        try:
            self.reference_service.create_item(self.reference_type, name)
            self.load_items()
            self.data_changed.emit()
        except ValueError as error:
            QMessageBox.warning(self, "Dados inválidos", str(error))
        except Exception as error:
            QMessageBox.critical(self, "Erro ao cadastrar", str(error))

    def edit_item(self):
        selected_item = self.list_widget.currentItem()
        if not selected_item:
            QMessageBox.information(self, "Seleção necessária", "Selecione um item para editar.")
            return

        name, accepted = QInputDialog.getText(
            self,
            f"Editar {self.title}",
            "Nome:",
            text=selected_item.text(),
        )
        if not accepted:
            return

        try:
            self.reference_service.update_item(
                self.reference_type,
                selected_item.data(Qt.UserRole),
                name,
            )
            self.load_items()
            self.data_changed.emit()
        except ValueError as error:
            QMessageBox.warning(self, "Dados inválidos", str(error))
        except Exception as error:
            QMessageBox.critical(self, "Erro ao editar", str(error))

    def delete_item(self):
        selected_item = self.list_widget.currentItem()
        if not selected_item:
            QMessageBox.information(self, "Seleção necessária", "Selecione um item para excluir.")
            return

        confirmation = QMessageBox.question(
            self,
            "Confirmar exclusão",
            f"Deseja excluir '{selected_item.text()}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if confirmation != QMessageBox.Yes:
            return

        try:
            self.reference_service.delete_item(self.reference_type, selected_item.data(Qt.UserRole))
            self.load_items()
            self.data_changed.emit()
        except Exception as error:
            QMessageBox.critical(self, "Erro ao excluir", str(error))
