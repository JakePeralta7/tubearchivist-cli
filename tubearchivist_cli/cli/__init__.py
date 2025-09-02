from sys import argv


def main():
    print("Welcome to the TubeArchivist CLI!")
    args = argv[1:]
    
    if not args:
        from tubearchivist_cli.cli.help import Help
        Help().show()
        return

    command = args[0]
    action = args[1] if len(args) > 1 else None

    match command:
        case "config":
            from tubearchivist_cli.cli.config import Config
            config = Config()
            if action:
                if hasattr(config, action):
                    getattr(config, action)()
                else:
                    print(f"Invalid config action: {action}")
            else:
                from tubearchivist_cli.cli.help import Help
                Help().show_command("config")
                
        case "sync":
            from tubearchivist_cli.api.client import TubeArchivistAPI
            from tubearchivist_cli.cli.sync import Sync
            try:
                client = TubeArchivistAPI()
                if client.test_connection():
                    sync = Sync()
                    if action:
                        if hasattr(sync, action):
                            getattr(sync, action)()
                        else:
                            print(f"Invalid sync action: {action}")
                    else:
                        from tubearchivist_cli.cli.help import Help
                        Help().show_command("sync")
                else:
                    raise ConnectionError("Failed to connect to the API.")
            except ValueError as e:
                print(f"Configuration error: {e}")
                print("Please run 'config set' to configure the API connection.")
        
        case "stats":
            from tubearchivist_cli.cli.stats import Stats
            stats = Stats()
            if action:
                if hasattr(stats, action):
                    getattr(stats, action)()
                else:
                    print(f"Invalid stats action: {action}")
            else:
                stats.overview()
                
        case "help":
            from tubearchivist_cli.cli.help import Help
            help_system = Help()
            if action:
                help_system.show_command(action)
            else:
                help_system.show()
                
        case _:
            print(f"Invalid command: {command}")
            from tubearchivist_cli.cli.help import Help
            Help().show()


if __name__ == "__main__":
    main()
