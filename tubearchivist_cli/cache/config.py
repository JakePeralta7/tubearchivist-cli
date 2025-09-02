from tubearchivist_cli.cache.table import DatabaseTable


class ConfigTable(DatabaseTable):
    def __init__(self):
        super().__init__()
        self.database_name = "config"
        self.create_table()

    def create_table(self):
        self.execute(f"""
        CREATE TABLE IF NOT EXISTS {self.database_name} (
            tubearchivist_url TEXT PRIMARY KEY,
            api_key TEXT NOT NULL
        )
        """)
        self.commit()

    def set_config(self, tubearchivist_url, api_key):
        # Always keep only one row in the config table
        self.clear_table()
        self.execute(f"INSERT INTO {self.database_name} (tubearchivist_url, api_key) VALUES (?, ?)",
                     (tubearchivist_url, api_key))
        self.commit()

    def get_config(self):
        return self.execute(f"SELECT tubearchivist_url, api_key FROM {self.database_name}")
