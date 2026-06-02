import os
import sqlite3
from pathlib import Path


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS computadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    ip TEXT NOT NULL,
    sistema_operacional TEXT NOT NULL,
    antivirus TEXT,
    responsavel TEXT,
    status_seguranca TEXT,
    setor TEXT
);
"""

REFERENCE_TABLES_SQL = (
    """
    CREATE TABLE IF NOT EXISTS sistemas_operacionais (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS antivirus_cadastrados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS setores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS licencas_ia (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS funcionarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        setor TEXT,
        cargo TEXT,
        licenca_ia TEXT,
        status_licenca TEXT
    );
    """,
)

DEFAULT_SISTEMAS_OPERACIONAIS = (
    "Windows 11 Pro",
    "Windows 10 Pro",
    "Windows Server 2022",
    "Windows Server 2019",
    "Ubuntu LTS",
    "Debian",
    "macOS",
)

DEFAULT_ANTIVIRUS = (
    "Microsoft Defender",
    "CrowdStrike Falcon",
    "Sophos Intercept X",
    "Kaspersky Endpoint Security",
    "ESET Endpoint Security",
    "Bitdefender GravityZone",
    "Trend Micro Apex One",
)

DEFAULT_SETORES = (
    "Suporte Tecnico",
    "Infraestrutura",
    "Desenvolvimento",
    "Seguranca da Informacao",
    "Comercial",
    "Financeiro",
    "RH",
    "Diretoria",
)

DEFAULT_LICENCAS_IA = (
    "Nenhuma",
    "ChatGPT Team",
    "GitHub Copilot Business",
    "Microsoft Copilot",
    "Gemini Business",
    "Claude Team",
)

DEFAULT_COMPUTADORES = (
    ("DEV-NB-001", "10.10.1.21", "Windows 11 Pro", "Microsoft Defender", "Ana Martins", "Seguro", "Desenvolvimento"),
    ("DEV-NB-002", "10.10.1.22", "Ubuntu LTS", "CrowdStrike Falcon", "Bruno Costa", "Seguro", "Desenvolvimento"),
    ("SUP-PC-001", "10.10.2.15", "Windows 10 Pro", "ESET Endpoint Security", "Carla Souza", "Em analise", "Suporte Tecnico"),
    ("INFRA-SRV-AD01", "10.10.0.10", "Windows Server 2022", "Microsoft Defender", "Diego Lima", "Seguro", "Infraestrutura"),
    ("INFRA-SRV-BKP01", "10.10.0.20", "Debian", "Sophos Intercept X", "Diego Lima", "Seguro", "Infraestrutura"),
    ("SEC-NB-001", "10.10.3.11", "Windows 11 Pro", "CrowdStrike Falcon", "Fernanda Rocha", "Seguro", "Seguranca da Informacao"),
    ("COM-PC-001", "10.10.4.18", "Windows 11 Pro", "Kaspersky Endpoint Security", "Gustavo Almeida", "Vulneravel", "Comercial"),
    ("FIN-PC-001", "10.10.5.31", "Windows 10 Pro", "Bitdefender GravityZone", "Helena Dias", "Em analise", "Financeiro"),
    ("RH-NB-001", "10.10.6.12", "Windows 11 Pro", "Trend Micro Apex One", "Juliana Pereira", "Seguro", "RH"),
    ("DIR-MAC-001", "10.10.7.8", "macOS", "Microsoft Defender", "Marcos Vieira", "Seguro", "Diretoria"),
)

DEFAULT_FUNCIONARIOS = (
    ("Ana Martins", "Desenvolvimento", "Desenvolvedora Python", "ChatGPT Team", "Ativa"),
    ("Bruno Costa", "Desenvolvimento", "Engenheiro DevOps", "GitHub Copilot Business", "Ativa"),
    ("Carla Souza", "Suporte Tecnico", "Analista de Suporte", "Microsoft Copilot", "Ativa"),
    ("Diego Lima", "Infraestrutura", "Administrador de Redes", "Nenhuma", "Nao possui"),
    ("Fernanda Rocha", "Seguranca da Informacao", "Analista de Seguranca", "ChatGPT Team", "Ativa"),
    ("Gustavo Almeida", "Comercial", "Executivo de Contas", "Gemini Business", "Pendente"),
    ("Helena Dias", "Financeiro", "Analista Financeira", "Microsoft Copilot", "Ativa"),
    ("Juliana Pereira", "RH", "Analista de RH", "Nenhuma", "Nao possui"),
)


class DatabaseManager:
    def __init__(self, database_path=None):
        self.database_path = database_path or self._default_database_path()
        self._ensure_database_directory()
        self.initialize_database()

    def _default_database_path(self):
        appdata = os.getenv("APPDATA")
        if appdata:
            return Path(appdata) / "InvSys" / "inventario.db"

        return Path(__file__).resolve().parents[2] / "data" / "inventario.db"

    def _ensure_database_directory(self):
        Path(self.database_path).parent.mkdir(parents=True, exist_ok=True)

    def get_connection(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def initialize_database(self):
        with self.get_connection() as connection:
            connection.execute(CREATE_TABLE_SQL)
            for table_sql in REFERENCE_TABLES_SQL:
                connection.execute(table_sql)
            self._ensure_computers_columns(connection)
            self._ensure_employees_columns(connection)
            self._seed_reference_tables(connection)
            self._seed_default_data(connection)
            connection.commit()

    def _ensure_computers_columns(self, connection):
        columns = {
            row["name"]
            for row in connection.execute("PRAGMA table_info(computadores)").fetchall()
        }

        if "setor" not in columns:
            connection.execute("ALTER TABLE computadores ADD COLUMN setor TEXT")

    def _ensure_employees_columns(self, connection):
        columns = {
            row["name"]
            for row in connection.execute("PRAGMA table_info(funcionarios)").fetchall()
        }

        required_columns = {
            "setor": "TEXT",
            "cargo": "TEXT",
            "licenca_ia": "TEXT",
            "status_licenca": "TEXT",
        }

        for column_name, column_type in required_columns.items():
            if column_name not in columns:
                connection.execute(
                    f"ALTER TABLE funcionarios ADD COLUMN {column_name} {column_type}"
                )

    def _seed_reference_tables(self, connection):
        connection.execute(
            """
            INSERT OR IGNORE INTO sistemas_operacionais (nome)
            SELECT DISTINCT sistema_operacional
            FROM computadores
            WHERE TRIM(COALESCE(sistema_operacional, '')) <> ''
            """
        )
        connection.execute(
            """
            INSERT OR IGNORE INTO antivirus_cadastrados (nome)
            SELECT DISTINCT antivirus
            FROM computadores
            WHERE TRIM(COALESCE(antivirus, '')) <> ''
            """
        )
        connection.execute(
            """
            INSERT OR IGNORE INTO setores (nome)
            SELECT DISTINCT setor
            FROM computadores
            WHERE TRIM(COALESCE(setor, '')) <> ''
            """
        )

    def _seed_default_data(self, connection):
        self._insert_names(connection, "sistemas_operacionais", DEFAULT_SISTEMAS_OPERACIONAIS)
        self._insert_names(connection, "antivirus_cadastrados", DEFAULT_ANTIVIRUS)
        self._insert_names(connection, "setores", DEFAULT_SETORES)
        self._insert_names(connection, "licencas_ia", DEFAULT_LICENCAS_IA)

        if self._is_table_empty(connection, "computadores"):
            connection.executemany(
                """
                INSERT INTO computadores (
                    nome, ip, sistema_operacional, antivirus, responsavel, status_seguranca, setor
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                DEFAULT_COMPUTADORES,
            )

        if self._is_table_empty(connection, "funcionarios"):
            connection.executemany(
                """
                INSERT INTO funcionarios (nome, setor, cargo, licenca_ia, status_licenca)
                VALUES (?, ?, ?, ?, ?)
                """,
                DEFAULT_FUNCIONARIOS,
            )

    def _insert_names(self, connection, table_name, names):
        connection.executemany(
            f"INSERT OR IGNORE INTO {table_name} (nome) VALUES (?)",
            [(name,) for name in names],
        )

    def _is_table_empty(self, connection, table_name):
        row = connection.execute(f"SELECT COUNT(*) AS total FROM {table_name}").fetchone()
        return row["total"] == 0
