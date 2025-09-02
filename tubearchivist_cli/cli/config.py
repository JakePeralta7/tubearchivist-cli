from tubearchivist_cli.cache.config import ConfigTable


class Config:
    """Configuration management for TubeArchivist CLI"""
    
    def __init__(self):
        self.config_table = ConfigTable()

        if not self.is_configured():
            print("Configuration not set. Please run `config set` to configure.")
    
    def set(self):
        """Set TubeArchivist URL and API key configuration"""
        tubearchivist_url = input("Enter TubeArchivist URL: ")
        api_key = input("Enter API Key: ")
        self.config_table.set_config(tubearchivist_url, api_key)
        print("Configuration saved successfully.")
    
    def get(self):
        """Display current configuration settings"""
        config = self.config_table.get_config()
        if config:
            tubearchivist_url, api_key = config[0]
            print(f"TubeArchivist URL: {tubearchivist_url}")
            print(f"API Key: {api_key}")
        else:
            print("No configuration found.")
    
    def is_configured(self):
        config = self.config_table.get_config()
        return config is not None and len(config) > 0
