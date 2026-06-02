from app.database.db_manager import DatabaseManager
from app.services.reference_data_service import ReferenceDataService


VALID_STATUSES = ("Seguro", "Vulnerável", "Em análise")


class ComputerService:
    def __init__(self, database_manager=None):
        self.database_manager = database_manager or DatabaseManager()
        self.reference_service = ReferenceDataService(self.database_manager)

    def list_computers(self, status_filter="Todos", sector_filter="Todos"):
        query = """
            SELECT id, nome, ip, sistema_operacional, antivirus, responsavel, status_seguranca, setor
            FROM computadores
        """
        filters = []
        parameters = []

        if status_filter != "Todos":
            filters.append("status_seguranca = ?")
            parameters.append(status_filter)

        if sector_filter != "Todos":
            filters.append("setor = ?")
            parameters.append(sector_filter)

        if filters:
            query += " WHERE " + " AND ".join(filters)

        query += " ORDER BY nome COLLATE NOCASE ASC"

        with self.database_manager.get_connection() as connection:
            rows = connection.execute(query, tuple(parameters)).fetchall()
            return [dict(row) for row in rows]

    def get_computer(self, computer_id):
        with self.database_manager.get_connection() as connection:
            row = connection.execute(
                """
                SELECT id, nome, ip, sistema_operacional, antivirus, responsavel, status_seguranca, setor
                FROM computadores
                WHERE id = ?
                """,
                (computer_id,),
            ).fetchone()
            return dict(row) if row else None

    def create_computer(self, data):
        self._validate(data)

        with self.database_manager.get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO computadores (
                    nome, ip, sistema_operacional, antivirus, responsavel, status_seguranca, setor
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    data["nome"],
                    data["ip"],
                    data["sistema_operacional"],
                    data.get("antivirus", ""),
                    data.get("responsavel", ""),
                    data["status_seguranca"],
                    data.get("setor", ""),
                ),
            )
            connection.commit()
            self._sync_reference_data(data)
            return cursor.lastrowid

    def update_computer(self, computer_id, data):
        self._validate(data)

        with self.database_manager.get_connection() as connection:
            connection.execute(
                """
                UPDATE computadores
                SET nome = ?,
                    ip = ?,
                    sistema_operacional = ?,
                    antivirus = ?,
                    responsavel = ?,
                    status_seguranca = ?,
                    setor = ?
                WHERE id = ?
                """,
                (
                    data["nome"],
                    data["ip"],
                    data["sistema_operacional"],
                    data.get("antivirus", ""),
                    data.get("responsavel", ""),
                    data["status_seguranca"],
                    data.get("setor", ""),
                    computer_id,
                ),
            )
            connection.commit()
            self._sync_reference_data(data)

    def delete_computer(self, computer_id):
        with self.database_manager.get_connection() as connection:
            connection.execute("DELETE FROM computadores WHERE id = ?", (computer_id,))
            connection.commit()

    def delete_computers(self, computer_ids):
        if not computer_ids:
            return

        placeholders = ",".join("?" for _ in computer_ids)
        with self.database_manager.get_connection() as connection:
            connection.execute(
                f"DELETE FROM computadores WHERE id IN ({placeholders})",
                tuple(computer_ids),
            )
            connection.commit()

    def _validate(self, data):
        required_fields = {
            "nome": "Nome da máquina",
            "ip": "IP",
            "sistema_operacional": "Sistema Operacional",
            "status_seguranca": "Status de segurança",
        }

        for field, label in required_fields.items():
            if not str(data.get(field, "")).strip():
                raise ValueError(f"O campo '{label}' é obrigatório.")

        if data["status_seguranca"] not in VALID_STATUSES:
            raise ValueError("Status de segurança inválido.")

    def _sync_reference_data(self, data):
        references = (
            ("sistemas_operacionais", data.get("sistema_operacional")),
            ("antivirus", data.get("antivirus")),
            ("setores", data.get("setor")),
        )

        for reference_type, value in references:
            if str(value or "").strip():
                self.reference_service.create_item(reference_type, value)
