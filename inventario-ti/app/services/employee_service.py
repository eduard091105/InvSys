from app.database.db_manager import DatabaseManager
from app.services.reference_data_service import ReferenceDataService


LICENSE_STATUSES = ("Ativa", "Pendente", "Expirada", "Nao possui")


class EmployeeService:
    def __init__(self, database_manager=None):
        self.database_manager = database_manager or DatabaseManager()
        self.reference_service = ReferenceDataService(self.database_manager)

    def list_employees(self, sector_filter="Todos", license_filter="Todos"):
        query = """
            SELECT id, nome, setor, cargo, licenca_ia, status_licenca
            FROM funcionarios
        """
        filters = []
        parameters = []

        if sector_filter != "Todos":
            filters.append("setor = ?")
            parameters.append(sector_filter)

        if license_filter != "Todos":
            filters.append("licenca_ia = ?")
            parameters.append(license_filter)

        if filters:
            query += " WHERE " + " AND ".join(filters)

        query += " ORDER BY nome COLLATE NOCASE ASC"

        with self.database_manager.get_connection() as connection:
            rows = connection.execute(query, tuple(parameters)).fetchall()
            return [dict(row) for row in rows]

    def get_employee(self, employee_id):
        with self.database_manager.get_connection() as connection:
            row = connection.execute(
                """
                SELECT id, nome, setor, cargo, licenca_ia, status_licenca
                FROM funcionarios
                WHERE id = ?
                """,
                (employee_id,),
            ).fetchone()
            return dict(row) if row else None

    def list_employee_names_by_sector(self, sector):
        if not str(sector or "").strip():
            return []

        with self.database_manager.get_connection() as connection:
            rows = connection.execute(
                """
                SELECT nome
                FROM funcionarios
                WHERE setor = ?
                ORDER BY nome COLLATE NOCASE ASC
                """,
                (sector,),
            ).fetchall()
            return [row["nome"] for row in rows]

    def create_employee(self, data):
        self._validate(data)

        with self.database_manager.get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO funcionarios (nome, setor, cargo, licenca_ia, status_licenca)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    data["nome"],
                    data.get("setor", ""),
                    data.get("cargo", ""),
                    data.get("licenca_ia", ""),
                    data.get("status_licenca", ""),
                ),
            )
            connection.commit()
            self._sync_reference_data(data)
            return cursor.lastrowid

    def update_employee(self, employee_id, data):
        self._validate(data)

        with self.database_manager.get_connection() as connection:
            connection.execute(
                """
                UPDATE funcionarios
                SET nome = ?,
                    setor = ?,
                    cargo = ?,
                    licenca_ia = ?,
                    status_licenca = ?
                WHERE id = ?
                """,
                (
                    data["nome"],
                    data.get("setor", ""),
                    data.get("cargo", ""),
                    data.get("licenca_ia", ""),
                    data.get("status_licenca", ""),
                    employee_id,
                ),
            )
            connection.commit()
            self._sync_reference_data(data)

    def delete_employee(self, employee_id):
        with self.database_manager.get_connection() as connection:
            connection.execute("DELETE FROM funcionarios WHERE id = ?", (employee_id,))
            connection.commit()

    def _validate(self, data):
        if not str(data.get("nome", "")).strip():
            raise ValueError("O campo 'Nome' e obrigatorio.")

        status = data.get("status_licenca", "")
        if status and status not in LICENSE_STATUSES:
            raise ValueError("Status da licenca invalido.")

    def _sync_reference_data(self, data):
        references = (
            ("setores", data.get("setor")),
            ("licencas_ia", data.get("licenca_ia")),
        )

        for reference_type, value in references:
            if str(value or "").strip():
                self.reference_service.create_item(reference_type, value)
