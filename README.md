# TubeArchivist CLI

A command-line interface for [TubeArchivist](https://github.com/tubearchivist/tubearchivist) that provides offline access to your archived YouTube content.

## Quick Start

1. **Install:**
   ```bash
   git clone https://github.com/JakePeralta7/tubearchivist-cli.git
   cd tubearchivist-cli
   pip install requests
   ```

2. **Configure:**
   ```bash
   python tube.py config set
   ```

3. **Sync data:**
   ```bash
   python tube.py sync all
   ```

4. **View stats:**
   ```bash
   python tube.py stats
   ```

## Commands

- `config set` - Configure TubeArchivist connection
- `sync all` - Download all data to local cache
- `sync video/channel/playlist` - Sync specific data types
- `stats` - View overview statistics
- `stats videos/channels/playlists` - Detailed statistics
- `help` - Show all available commands

## License

GPL-3.0
