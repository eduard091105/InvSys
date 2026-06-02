from app.database.db_manager import DatabaseManager


REFERENCE_TABLES = {
    "sistemas_operacionais": "sistemas_operacionais",
    "antivirus": "antivirus_cadastrados",
    "setores": "setores",
    "licencas_ia": "licencas_ia",
}


class ReferenceDataService:
    def __init__(self, database_manager=None):
        self.database_manager = database_manager or DatabaseManager()

    def list_items(self, reference_type):
        table_name = self._table_name(reference_type)
        with self.database_manager.get_connection() as connection:
            rows = connection.execute(
                f"SELECT id, nome FROM {table_name} ORDER BY nome COLLATE NOCASE ASC"
            ).fetchall()
            return [dict(row) for row in rows]

    def list_names(self, reference_type):
        return [item["nome"] for item in self.list_items(reference_type)]

    def create_item(self, reference_type, name):
        table_name = self._table_name(reference_type)
        clean_name = self._clean_name(name)

        with self.database_manager.get_connection() as connection:
            connection.execute(
                f"INSERT OR IGNORE INTO {table_name} (nome) VALUES (?)",
                (clean_name,),
            )
            connection.commit()

    def update_item(self, reference_type, item_id, name):
        table_name = self._table_name(reference_type)
        clean_name = self._clean_name(name)

        with self.database_manager.get_connection() as connection:
            connection.execute(
                f"UPDATE {table_name} SET nome = ? WHERE id = ?",
                (clean_name, item_id),
            )
            connection.commit()

    def delete_item(self, reference_type, item_id):
        table_name = self._table_name(reference_type)
        with self.database_manager.get_connection() as connection:
            connection.execute(f"DELETE FROM {table_name} WHERE id = ?", (item_id,))
            connection.commit()

    def _table_name(self, reference_type):
        if reference_type not in REFERENCE_TABLES:
            raise ValueError("Tipo de cadastro inválido.")

        return REFERENCE_TABLES[reference_type]

    def _clean_name(self, name):
        clean_name = str(name).strip()
        if not clean_name:
            raise ValueError("Informe um nome para cadastrar.")

        return clean_name
