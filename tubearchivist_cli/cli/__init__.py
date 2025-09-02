from sys import argv


def main():
    print("Welcome to the TubeArchivist CLI!")
    args = argv[1:]

    match args[0]:
        case "config":
            from tubearchivist_cli.cli.config import Config
            config = Config()
            getattr(config, args[1])()
        case "sync":
            from tubearchivist_cli.api.client import TubeArchivistAPI
            from tubearchivist_cli.cli.sync import Sync
            client = TubeArchivistAPI()
            if client.test_connection():
                sync = Sync()
                getattr(sync, args[1])()
            else:
                raise ConnectionError("Failed to connect to the API.")
        case "help":
            print("Available commands:")
            print("  config set   - Set the configuration")
            print("  config get   - Get the configuration")
            print("  sync video   - Sync videos from TubeArchivist")
            print("  sync playlist - Sync playlists from TubeArchivist")
            print("  sync channel - Sync channels from TubeArchivist")
            print("  sync all     - Sync all data from TubeArchivist")
        case _:
            print("Invalid command.")


if __name__ == "__main__":
    main()
